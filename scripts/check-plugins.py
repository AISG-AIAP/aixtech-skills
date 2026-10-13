#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
SOURCE = PLUGINS / "pstack"

PRINCIPLE_REF = re.compile(r"\*\*principle-([a-z-]+)\*\*|\*\*([a-z-]+)\*\* principle skill|\(the \*\*([a-z-]+)\*\* principle")
WORKFLOW_REF = re.compile(r"\*\*([a-z-]+)\*\* workflow")
SKILL_REF = re.compile(r"\*\*([a-z-]+)\*\* skill\b")
CODE_NAME = re.compile(r"`([a-z-]+)`")
CODE_PATH = re.compile(r"`((?:\.\./)?(?:references|scripts)/[A-Za-z0-9_./-]+)`")
PLAYBOOK_REF = re.compile(r"playbooks/([a-z-]+)\.md")
LINK = re.compile(r"\]\((\.{1,2}/[^)#]+)\)")


def kebab(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).strip().replace(" ", "-")


def section(text, heading):
    match = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1) if match else ""


def listed(body):
    names = []
    for title, rest in re.findall(r"^- \*\*([^*]+?)\.?\*\*(.*)$", body, re.M):
        override = re.search(r"\*\*principle-([a-z-]+)\*\*|File: `playbooks/([a-z-]+)\.md`", rest)
        names.append((override.group(1) or override.group(2)) if override else kebab(title))
    return names


def check(plugin, known):
    errors = []
    skills = plugin / "skills"
    entry = skills / "pstack" / "SKILL.md"
    if not entry.is_file():
        return [f"{plugin.name}: missing skills/pstack/SKILL.md"]
    text = entry.read_text()

    principles = {p.name.removeprefix("principle-") for p in skills.glob("principle-*") if (p / "SKILL.md").is_file()}
    playbooks = {p.stem for p in (skills / "pstack" / "playbooks").glob("*.md")}
    workflows = {kebab(w) for w in re.findall(r"^- \*\*([a-z-]+)\.\*\*", section(text, "Workflows"), re.M)}
    skill_dirs = {p.name for p in skills.iterdir() if (p / "SKILL.md").is_file()}

    listed_principles = set(listed(section(text, "Principles")))
    listed_playbooks = set(listed(section(text, "Playbooks")))
    for name in sorted(listed_principles - principles):
        errors.append(f"{plugin.name}: Principles lists {name} but skills/principle-{name} is missing")
    for name in sorted(principles - listed_principles):
        errors.append(f"{plugin.name}: skills/principle-{name} is not listed in Principles")
    for name in sorted(listed_playbooks - playbooks):
        errors.append(f"{plugin.name}: Playbooks lists {name} but playbooks/{name}.md is missing")
    for name in sorted(playbooks - listed_playbooks):
        errors.append(f"{plugin.name}: playbooks/{name}.md is not listed in Playbooks")

    for md in sorted(skills.rglob("*.md")):
        where = f"{plugin.name}/{md.relative_to(skills)}"
        body = md.read_text()
        for groups in PRINCIPLE_REF.findall(body):
            name = next(g for g in groups if g)
            if name not in principles:
                errors.append(f"{where}: references principle {name}, not in this plugin")
        for name in set(WORKFLOW_REF.findall(body)):
            if name not in workflows:
                errors.append(f"{where}: references workflow {name}, not defined in Workflows")
        for name in set(SKILL_REF.findall(body)):
            if name not in skill_dirs and name not in workflows:
                errors.append(f"{where}: references skill {name}, not in this plugin")
        for name in set(CODE_NAME.findall(body)) & known:
            if name not in skill_dirs and name not in workflows:
                errors.append(f"{where}: mentions `{name}`, which is neither a skill nor a workflow in this plugin")
        for name in set(PLAYBOOK_REF.findall(body)):
            if name not in playbooks:
                errors.append(f"{where}: references playbooks/{name}.md, not in this plugin")
        for target in set(CODE_PATH.findall(body)):
            owner = next((d for d in md.parents if d.parent == skills), md.parent)
            if not ((md.parent / target).exists() or (owner / target).exists()):
                errors.append(f"{where}: path {target} does not exist")
        for target in set(LINK.findall(body)):
            if not (md.parent / target).resolve().exists():
                errors.append(f"{where}: link {target} does not resolve")

    if plugin != SOURCE and SOURCE.is_dir():
        for name in sorted(principles):
            copy = skills / f"principle-{name}" / "SKILL.md"
            original = SOURCE / "skills" / f"principle-{name}" / "SKILL.md"
            if not original.is_file() or copy.read_bytes() != original.read_bytes():
                errors.append(f"{plugin.name}: principle-{name} differs from plugins/pstack; edit the source copy and recopy")

        for shared in ["scripts", "references"]:
            copy_root = skills / "pstack" / shared
            source_root = SOURCE / "skills" / "pstack" / shared
            if not copy_root.is_dir():
                continue
            for copy in sorted(f for f in copy_root.rglob("*") if f.is_file() and "node_modules" not in f.parts):
                original = source_root / copy.relative_to(copy_root)
                if not original.is_file() or copy.read_bytes() != original.read_bytes():
                    errors.append(f"{plugin.name}: pstack/{shared}/{copy.relative_to(copy_root)} differs from plugins/pstack; edit the source copy and recopy")

    for manifest in ["plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
        path = plugin / manifest
        if not path.is_file():
            errors.append(f"{plugin.name}: missing {manifest}")
        elif json.loads(path.read_text()).get("name") != plugin.name:
            errors.append(f"{plugin.name}: {manifest} name does not match the folder name")
    return errors


def check_marketplaces(plugin_names):
    errors = []
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    entries = {
        ".claude-plugin/marketplace.json": {p["name"]: p["source"] for p in claude["plugins"]},
        ".agents/plugins/marketplace.json": {p["name"]: p["source"]["path"] for p in codex["plugins"]},
    }
    for file, sources in entries.items():
        for name in sorted(plugin_names - sources.keys()):
            errors.append(f"{file}: plugin {name} is not listed")
        for name, source in sources.items():
            if source != f"./plugins/{name}":
                errors.append(f"{file}: {name} source is {source}, expected ./plugins/{name}")
    return errors


def main():
    plugins = sorted(p for p in PLUGINS.iterdir() if p.is_dir())
    known = {
        kebab(w)
        for p in plugins
        for w in re.findall(r"^- \*\*([a-z-]+)\.\*\*", section((p / "skills/pstack/SKILL.md").read_text(), "Workflows"), re.M)
    }
    known |= {d.name for p in plugins for d in (p / "skills").iterdir() if not d.name.startswith("principle-")}
    known.discard("pstack")
    errors = [e for p in plugins for e in check(p, known)]
    errors += check_marketplaces({p.name for p in plugins})
    for error in errors:
        print(error)
    print(f"{len(plugins)} plugins checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

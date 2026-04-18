# unity-game-research

Research an extracted Unity game and generate reusable, evidence-backed notes about its systems, mechanics, and architecture.

`unity-game-research` helps an agent inspect a Unity client and produce notes that can be reused and extended later instead of recreated from scratch.

## What This Skill Does

Use this skill when you want an agent to study topics such as:

- economy and progression
- combat and skills
- inventory and monetization
- networking and validation
- class architecture behind a subsystem

The skill works with extracted Unity client files and supports both Mono and IL2CPP layouts. Its output is a reusable `game-knowledge/` folder.

## Requirements

- A compatible client such as Claude Code or Codex
- Local filesystem access to the extracted game
- `python3` for the checkpoint script

## Install

Choose the installation method that fits your setup.

### Install with Skills CLI

If you already use the Skills CLI, this is the shortest path:

```bash
npx skills add avm-dev/unity-game-research
```

Repository URL:

`https://github.com/avm-dev/unity-game-research`

### Install with Git Clone

Clone the repository into the skills directory used by your client.

Codex and generic agent skills directory:

```bash
git clone https://github.com/avm-dev/unity-game-research.git ~/.agents/skills/unity-game-research
```

Claude Code:

```bash
git clone https://github.com/avm-dev/unity-game-research.git ~/.claude/skills/unity-game-research
```

### Install by Downloading the Folder

If you do not want to use `npx` or `git`, download the repository as a ZIP, extract it, and place the folder in one of these locations:

- `~/.agents/skills/unity-game-research`
- `~/.claude/skills/unity-game-research`

## Use

Ask the agent to use `unity-game-research` and name the system you want to study.

Example prompts:

- `Use unity-game-research. Study economy and progression.`
- `Use unity-game-research. Study the skill system.`
- `Use unity-game-research. Reconstruct the class architecture behind hero movement.`

You do not need to spell out:

- output folder
- checkpoint creation
- indexing
- resume behavior
- backend detection

## Repository Layout

- `SKILL.md`: main skill instructions
- `scripts/unity_research_checkpoint.py`: checkpoint and index builder
- `references/`: supporting research guides and schemas
- `tests/`: portability and regression tests
- `agents/`: optional client metadata

## Validation

Run the local checks with:

```bash
python3 -m unittest discover -s tests -v
skills-ref validate ./
```

## Portability Notes

- Do not hardcode machine-specific paths.
- Do not hardcode project-specific package names or extracted game paths.
- Prefer relative paths and generic discovery heuristics.

# unity-game-research

Portable Codex skill for researching Unity games from extracted client files.

## What It Includes

- `SKILL.md`
- `agents/`
- `references/`
- `scripts/`
- `tests/`

## Requirements

- Codex with local skill support
- `python3` for the checkpoint script and tests

## Install

Copy this directory into your Codex skills directory as `unity-game-research`.

Example target:
- `$CODEX_HOME/skills/unity-game-research`

## Use

Reference the skill as `unity-game-research` from Codex when you want to research
an extracted Unity game. The main workflow and expected outputs are documented in
`SKILL.md`.

## Main Use Cases

- Unity IL2CPP or Mono layout detection
- gameplay system research
- client validation and networking surface analysis
- generic cache and downloaded-bundle candidate discovery
- reusable dossier generation for later Q&A or reverse-engineering passes

## Repo Layout

- `SKILL.md`: main skill instructions
- `scripts/unity_research_checkpoint.py`: lightweight checkpoint/index builder
- `references/`: supporting guidance for dossier structure and adapters
- `tests/`: regression tests for portability-sensitive behavior
- `agents/`: agent metadata used by the skill

## Portability Notes

This package is intended to stay portable.

- Do not hardcode machine-specific paths.
- Do not hardcode project-specific package names or extracted game paths.
- Prefer relative paths and generic discovery heuristics.

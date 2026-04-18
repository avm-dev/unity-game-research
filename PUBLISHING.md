# Publishing

## What This Folder Is

This directory is the GitHub-ready repository payload. Its top level should contain:

- `SKILL.md`
- `agents/`
- `references/`
- `scripts/`
- `tests/`
- `README.md`
- `.gitignore`
- `LICENSE`
- `PUBLISHING.md`

## Initialize Git

Run these commands from this directory:

```bash
git init
git add .
git commit -m "Initial publish of unity-game-research"
```

## Create GitHub Repo With `gh`

```bash
git branch -M main
gh repo create unity-game-research --public --source=. --remote=origin --push
```

## Manual GitHub Remote Flow

If you create the repository in the GitHub UI first:

```bash
git init
git add .
git commit -m "Initial publish of unity-game-research"
git branch -M main
```

Then copy the SSH or HTTPS remote command shown by GitHub for the empty
repository and run it from this same directory, followed by:

```bash
git push -u origin main
```

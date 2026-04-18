# Publishing

## Repository Checklist

Before publishing, confirm:

- the repository is public
- `SKILL.md` is present at the repository root
- the `name` field matches the directory name
- the skill description is agent-neutral
- local tests pass
- `skills-ref validate ./` passes

## Local Validation

```bash
python3 -m unittest discover -s tests -v
skills-ref validate ./
```

## Initialize Git

```bash
git init
git add .
git commit -m "Initial publish of unity-game-research"
git branch -M main
```

## Create GitHub Repo With `gh`

```bash
gh repo create unity-game-research --public --source=. --remote=origin --push
```

## Submit To The Directory

Submit the public repository URL at:

- `https://agentskill.sh/submit`

The directory will scan the repository for `SKILL.md` files and import them.

## Optional Instant Sync

For faster updates, add a GitHub webhook:

- Payload URL: `https://agentskill.sh/api/webhooks/github`
- Content type: `application/json`
- Events: `push` only

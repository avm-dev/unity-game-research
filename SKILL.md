---
name: unity-game-research
description: Study a Unity game from the current working folder or a user-specified extracted game directory, collect technical evidence, infer gameplay systems, and write or update a reusable `game-knowledge/` dossier. Use when the user wants Codex to research one or more game systems end-to-end with minimal prompting, for example economy, progression, combat, monetization, hero movement, skills, inventory, quests, guild, networking, or any other specific subsystem. The user should only need to name the topics to study; Codex should handle detection, extraction, indexing, resume, and document generation automatically.
---

# Unity Game Research

## Overview

Run the whole investigation as one job. Start from the current folder unless the user gives another path, detect the Unity build layout, gather evidence, resume prior work automatically, and produce design documents that another agent can use for Q&A about the game.

## Default Behavior

- Treat the current working directory as the input root when the user says "here", "this folder", or gives no path.
- Write output to `./game-knowledge/` unless the user specifies another destination.
- If `game-knowledge/` already exists, resume from it and update in place without deleting unrelated user files.
- Prefer read-only analysis of the source tree. Do not move, rename, or modify original game artifacts.
- If the folder is not clearly a Unity game, say so early and stop before inventing a dossier.
- Treat extraction, indexing, and resume as internal responsibilities of the skill. Do not ask the user to request them explicitly.
- Assume the user will only name the systems to study. Infer all other operational steps yourself.

## User Contract

Assume the user's request will look like one of these:

- `Use $unity-game-research. Study economy, progression, and monetization.`
- `Use $unity-game-research. Study hero movement on the battlefield.`
- `Use $unity-game-research. Study the skill system.`

Do not require the user to mention:

- current folder
- output folder
- resume behavior
- extraction or indexing
- backend detection
- local tools
- evidence policy

Those are part of the skill.

## Internal Phases

Run these phases automatically and resume from the latest completed checkpoint when possible:

1. Confirm Unity markers anywhere in the discovered tree:
   - `assets/bin/Data/`
   - `assets/bin/Data/Managed/`
   - `assets/bin/Data/il2cpp_data/`
   - search the tree for `libil2cpp.so`, `libunity.so`, and `global-metadata.dat`
   - `libunity.so`
   - `libil2cpp.so`
   - `global-metadata.dat`
   - `globalgamemanagers`, `resources.assets`, `sharedassets*.assets`
2. Classify the scripting backend:
   - managed/Mono if game assemblies exist in `Managed/`
   - IL2CPP if both `libil2cpp.so` and `global-metadata.dat` are present anywhere in the discovered tree
3. Build or refresh a checkpoint state under `game-knowledge/`:
   - `manifest.yaml`
   - `progress.yaml`
   - `raw/`
   - `indexes/`
4. Extract game-facing signals from the best available artifacts:
   - managed assemblies or IL2CPP recovery outputs
   - strings, endpoints, config blobs, enum names, type names
   - asset names, prefab names, scene names, resources, localization data
5. Convert large raw outputs into compact indexes before doing substantial reasoning.
6. Infer gameplay systems only from evidence. Separate facts from interpretation.
7. Write or update only the topic documents requested by the user, then refresh shared summary files as needed.

## Resume Rules

- If `game-knowledge/progress.yaml` exists, read it first.
- Do not redo expensive extraction if matching `raw/` and `indexes/` artifacts already exist and still cover the requested topics.
- If the user asks for a new topic a week later, continue from prior checkpoints instead of starting over.
- Only rebuild stale or missing phases.
- Preserve previous topic documents unless new evidence contradicts them.
- Record each researched topic in `progress.yaml`.
- If a topic document already exists, update it in place instead of rewriting it from scratch unless the evidence base changed substantially.

## Tool Orchestration

- If local reverse-engineering tools are available, use them.
- Prefer deterministic tools for extraction and indexing, then use LLM reasoning on the compact outputs.
- Good candidates include filesystem inventory, string extraction, assembly/type listing, IL2CPP recovery helpers, and asset name extraction.
- Do not block on a specific tool if equivalent evidence can be collected another way.
- When a tool produces a large output, save it under `raw/` and create a condensed index under `indexes/` before reasoning.
- Prefer running `scripts/unity_research_checkpoint.py` first to build or refresh `manifest.yaml`, `progress.yaml`, `raw/`, `indexes/`, and `evidence/files-inventory.md`.
- Treat the checkpoint script as the default low-cost entrypoint for repeated sessions.
- Use deeper adapters opportunistically:
  - managed: `ilspycmd` or `monodis` if available, otherwise printable-string identifier extraction
  - native/IL2CPP: `readelf` and `nm` if available, otherwise keep relying on file inventory and strings
- Respect environment-variable overrides for local tool paths when present.
- Always inspect `indexes/tool-readiness.md` after checkpoint creation to understand what parts of the toolchain are available.
- Inspect `indexes/install-plan.md` when readiness is insufficient and installation may be worthwhile.
- If required tools are missing, continue with available fallbacks instead of blocking the request.
- Only attempt tool installation when the user explicitly approves installation work. Do not silently install anything.
- If installation is approved, prefer deterministic package-manager or local-binary installation commands and record the result in `technical-findings.md`.

## Missing Tool Notifications

When the requested research topic would materially benefit from a missing tool, tell the user explicitly.

Use these priority levels:

- `Required`: the requested task is effectively blocked without the tool
- `Recommended`: the task can continue, but depth or confidence will be materially worse
- `Optional`: the tool would help, but current evidence is probably enough

The notification should say:

- which tool is missing
- why it matters for the current topic
- whether work can continue without it
- whether installation is recommended now

Examples:

- `Missing tool: Cpp2IL. Priority: Recommended. Needed for deeper IL2CPP reconstruction of the skill system. Work can continue with reduced architecture fidelity.`
- `Missing tool: Ghidra. Priority: Optional. Useful only if static IL2CPP recovery remains too shallow.`

## Capability Gap Detection

Do not assume the predefined tool list is complete.

If the current environment lacks a needed capability, but no exact tool is known or auto-detected, tell the user explicitly that a capability gap exists.

Examples of capability gaps:

- deeper native control-flow analysis
- Unity asset table extraction
- runtime memory dumping
- network traffic interception
- managed assembly decompilation beyond string-level recovery

For a capability gap, report:

- `Missing capability`
- why it matters for the requested topic
- whether the current pass can continue
- one or more candidate tools if known

Example:

- `Missing capability: runtime memory dumping. Priority: Recommended. Needed because static IL2CPP artifacts appear protected. Candidate tools may include Frida-based or debugger-assisted dumping workflows.`

## Token Efficiency Rules

- Read `manifest.yaml` and `progress.yaml` before opening any other files.
- Prefer `indexes/` over `raw/`. Do not read `raw/` unless the needed evidence is missing from indexes.
- Treat `raw/` as a last-resort archive, not the default reasoning source.
- For a narrow request, open only the indexes relevant to that topic.
- If the user requests one system, research one system. Do not broaden scope by default.
- Prefer updating existing topic files over regenerating them.
- Do not refresh `summary.md` for every narrow topic unless the global understanding materially changed.
- Do not rebuild checkpoint artifacts if current ones are sufficient and inputs do not appear to have changed.
- Maintain a small working set of files per pass. Avoid opening every index file in the dossier.
- Stop extraction once evidence is sufficient to support a stable draft for the requested topic.

## Topic Routing

Before substantial reasoning, map the user request to a narrow topic slug and load only the most relevant artifacts first.

Recommended priority order:

- `topics/<slug>.md` if it already exists
- `indexes/candidate-systems.md`
- `indexes/strings-by-topic.md`
- `indexes/types-index.md`
- `indexes/native-symbols.md`
- `indexes/assets-index.md`
- `indexes/network-endpoints.md`
- `raw/` only if the indexes are insufficient

When useful, create or update a compact topic cache under `indexes/topics/<slug>.md` so later sessions can resume without re-reading multiple indexes.

## Developer Reconstruction Mode

If the user asks to reconstruct a mechanic as a developer, recover the programming architecture rather than only a gamedesign description.

Typical requests:

- `Use $unity-game-research. Reconstruct the programming class architecture for the skill system.`
- `Use $unity-game-research. Reconstruct the programming class architecture for hero movement on the battlefield.`

In this mode, prioritize:

- key classes and namespaces
- inheritance and interfaces
- responsibilities of each class
- method flow and call sequence
- state flow and data ownership
- service, controller, manager, model, and config relationships
- reimplementation notes and unresolved gaps

Prefer `indexes/types-index.md`, `indexes/native-symbols.md`, `indexes/strings-by-topic.md`, and relevant existing topic caches before broader dossier files.

## Dual-Perspective Mode

If the user asks for both gamedesign understanding and developer reconstruction for the same topic, produce both views without broadening the topic scope.

Typical requests:

- `Use $unity-game-research. Study the skill system from both a gamedesign and programming architecture perspective.`
- `Use $unity-game-research. Study hero movement on the battlefield from both a gamedesign and developer reconstruction perspective.`

In this mode:

- keep the research focused on one requested topic unless the user explicitly names several
- write the player-facing/system-design explanation in `topics/<slug>.md`
- write the code-architecture view in `topics/<slug>-architecture.md`
- write `topics/<slug>-reimplementation.md` when the evidence is sufficient to propose a reimplementation path
- share evidence across both documents instead of duplicating broad extraction work

## Evidence Rules

- Every non-trivial claim should point to evidence:
  - file path
  - assembly name
  - class/type name
  - string or config key
  - asset or scene path
- Distinguish four categories explicitly:
  - `Fact`: directly observed in files
  - `Inference`: likely interpretation of facts
  - `Unknown`: relevant but not confirmed from available evidence
  - `Server-side`: behavior is clearly authoritative or finalized outside the client, even if the exact implementation is unknown
- Never present guessed mechanics as certain just because the genre is obvious.
- If names are obfuscated, rely more on strings, resource names, endpoints, numeric tables, and cross-references.
- Use `Server-side` when the client clearly indicates backend ownership, validation, or final authority, instead of collapsing everything into `Unknown`.

## Required Output

Create or update these files under `game-knowledge/`:

- `manifest.yaml`
- `progress.yaml`
- `summary.md`
- `technical-findings.md`
- `unknowns.md`
- `glossary.md`
- `evidence/files-inventory.md`
- `indexes/`
- `raw/`

Expect these index artifacts when the checkpoint script has run:

- `indexes/assemblies-index.md`
- `indexes/types-index.md`
- `indexes/assets-index.md`
- `indexes/native-symbols.md`
- `indexes/network-endpoints.md`
- `indexes/strings-by-topic.md`
- `indexes/candidate-systems.md`
- `indexes/recovery-plan.md`
- `indexes/tool-readiness.md`
- `indexes/install-plan.md`

Create topic documents under `game-knowledge/topics/` using stable slugs derived from the user's requested systems:

- `topics/economy.md`
- `topics/progression.md`
- `topics/hero-movement-on-battlefield.md`
- `topics/skill-system.md`
- `topics/inventory.md`
- `topics/guild-system.md`

Also create category documents such as `systems/`, `mechanics/`, or `entities/` only when they materially help organization for the current game and requested topics.

For developer reconstruction requests, also allow:

- `topics/<slug>-architecture.md`
- `topics/<slug>-call-flow.md`
- `topics/<slug>-reimplementation.md`

For dual-perspective requests, prefer:

- `topics/<slug>.md`
- `topics/<slug>-architecture.md`
- `topics/<slug>-reimplementation.md` when useful

Do not create empty filler documents. If a topic cannot be supported yet, record it in `unknowns.md` and explain what evidence is missing.

Only create `topics/<slug>-reimplementation.md` when reimplementation feasibility is high. Otherwise keep reimplementation notes inside `topics/<slug>-architecture.md`.

## Document Rules

- Start each topical document with:
  - scope
  - confidence
  - evidence summary
- Then describe the system in gamedesign language.
- Then structure the body as:
  - `Facts`
  - `Inferences`
  - `Unknowns`
  - `Server-side`
- End with `Files and Evidence`.
- Keep the documents useful for a later Q&A agent. Optimize for retrieval, not literary prose.
- For targeted subsystem requests, go as deep as evidence allows. Example: if the user asks for hero movement on the battlefield, trace movement-related classes, states, pathfinding hints, animation/state machine names, nav or grid clues, input bindings, skill-movement coupling, and any restrictions or combat interactions relevant to movement.

For developer reconstruction requests, prefer this structure:

- `Purpose`
- `Key Classes`
- `Responsibilities`
- `Relationships`
- `Method Flow`
- `State And Data Flow`
- `Reimplementation Notes`
- `Unknowns`
- `Files and Evidence`

For dual-perspective requests:

- keep `topics/<slug>.md` focused on mechanics, player-facing rules, progression hooks, restrictions, and outcomes
- keep `topics/<slug>-architecture.md` focused on classes, responsibilities, relationships, and flows
- avoid merging both views into one bloated document unless the topic is tiny

## Reimplementation Feasibility

Assess reimplementation feasibility before creating `topics/<slug>-reimplementation.md`.

Use these levels:

- `high`: create `topics/<slug>-reimplementation.md`
- `medium`: keep reimplementation notes inside `topics/<slug>-architecture.md`
- `low`: do not propose a concrete reimplementation beyond high-level observations

Mark feasibility as `high` only when at least 4 of these 6 conditions are satisfied:

1. key classes for the subsystem are identified
2. the main execution or method flow is understood
3. state ownership is reasonably clear
4. rules/config/data inputs are visible
5. class relationships are identifiable
6. remaining unknowns are narrow and localized

Treat any of these as red flags that should usually force `medium` or `low`:

- severe obfuscation with no reliable role recovery
- no clear execution flow
- unclear state ownership
- evidence is mostly strings or UI labels
- the subsystem appears mostly server-authoritative
- facts and guesses cannot be cleanly separated

When feasibility is not `high`, add a short section to `topics/<slug>-architecture.md`:

- `Reimplementation Feasibility`
- `What Is Missing`
- `What Could Be Safely Recreated`

## Scope Requests

If the user asks for one or more specific systems:

1. Prioritize only those topics.
2. Still maintain `manifest.yaml`, `progress.yaml`, `summary.md`, `technical-findings.md`, and `unknowns.md`.
3. Do not spend time producing unrelated system documents unless strong evidence is already available at near-zero extra cost.
4. Treat a narrow request as permission to go deep, not broad.
5. If only one topic was requested, keep the pass single-topic unless blocking dependencies force a small amount of adjacent context.
6. If the request is framed as implementation or reconstruction work, switch to developer reconstruction mode automatically.
7. If the request explicitly asks for both design and code architecture, switch to dual-perspective mode automatically.

## Escalation Path

- For managed builds, inspect `Managed/` assemblies and prioritize `Assembly-CSharp.dll`.
- For IL2CPP builds, inventory `libil2cpp.so`, `libunity.so`, and `global-metadata.dat`, then explain what can and cannot be recovered statically.
- If deeper backend-specific guidance is needed, check `indexes/tool-readiness.md` first, then use `references/tool-adapters.md` to pick the best available adapter or fallback; report any missing capability directly.

## Mobile Online RPG Bias

Expect frequent evidence for:

- progression and leveling
- currencies and sinks
- inventory and equipment
- skill trees or active/passive skills
- quests and mission chains
- guild, clan, party, or social systems
- PvE and PvP rules
- events, daily tasks, and retention loops
- monetization and live-ops
- client/server authority boundaries

For live data or packed content, fall back to generic mobile signatures like `UnityCache/Shared`, `cache`, `files`, `AssetBundle`, `BundleFiles`, `__data`, or bundle-like files when the exact container layout is unclear.

Do not assume the server-side truth is fully visible in the client. For online RPGs, mark server-owned behavior as `Unknown` when the client only reveals hints.

## Validation And Networking

Use the smallest network surface that still proves the loop:

- start/finish DTOs and message types
- request/result types and error enums
- endpoint and config strings
- validator-like field paths and client-side compare helpers
- explicit client-versus-server authority boundaries

Treat client checks as local hints only when the server can still override the final state.

## References

- Read `references/dossier-schema.md` for the expected output tree and field meanings.
- Read `references/mechanics-inference-guide.md` when extracting mechanics from weak or partial evidence.
- Read `references/progress-schema.md` when creating or updating checkpoint files.
- Use `scripts/unity_research_checkpoint.py` to materialize checkpoint artifacts before substantial LLM reasoning.
- Read `references/tool-adapters.md` when deciding how to use available local reverse-engineering tools and fallbacks.
- Read `references/developer-reconstruction.md` when the user wants class architecture, flows, dependencies, or reimplementation guidance.

## Capability Notes

After checkpoint creation, inspect `indexes/tool-readiness.md` first. Use `references/tool-adapters.md` to pick the best available adapters and fallbacks; if a capability is missing, report the gap instead of assuming a deeper sibling workflow exists.

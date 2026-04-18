from __future__ import annotations

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"


class SkillTextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_PATH.read_text(encoding="utf-8")
        self.readme = README_PATH.read_text(encoding="utf-8")

    def test_mentions_tree_wide_il2cpp_search(self) -> None:
        for needle in ("libil2cpp.so", "libunity.so", "global-metadata.dat"):
            self.assertIn(needle, self.text)

    def test_mentions_mobile_fallback_and_validation_playbook(self) -> None:
        for needle in ("UnityCache/Shared", "validator-like field paths", "client-versus-server authority boundaries"):
            self.assertIn(needle, self.text)

    def test_mentions_portability_guidance_replacement(self) -> None:
        for needle in ("indexes/tool-readiness.md", "references/tool-adapters.md", "missing capability"):
            self.assertIn(needle, self.text)

    def test_does_not_reference_sibling_skill_paths(self) -> None:
        self.assertIsNone(re.search(r"\.\./[^`/\s]+/SKILL\.md", self.text))

    def test_has_license_and_compatibility_frontmatter(self) -> None:
        self.assertIn("license: MIT", self.text)
        self.assertIn("compatibility:", self.text)
        self.assertIn("description: Use when", self.text)

    def test_is_agent_neutral(self) -> None:
        self.assertNotIn("Codex", self.text)
        self.assertNotIn("Claude Code", self.text)

    def test_readme_mentions_cross_client_install_path(self) -> None:
        self.assertIn("~/.agents/skills/unity-game-research", self.readme)
        self.assertIn("~/.claude/skills/unity-game-research", self.readme)

    def test_skill_file_stays_compact(self) -> None:
        self.assertLess(len(self.text.splitlines()), 500)

    def test_readme_is_not_codex_only(self) -> None:
        self.assertNotIn("Portable Codex skill", self.readme)
        self.assertIn("Claude Code or Codex", self.readme)

    def test_readme_has_simple_install_command(self) -> None:
        self.assertIn("## Quick Install", self.readme)
        self.assertIn("npx skills add avm-dev/unity-game-research", self.readme)
        self.assertIn("git clone https://github.com/avm-dev/unity-game-research.git", self.readme)

    def test_readme_has_multiple_install_options(self) -> None:
        self.assertIn("## Install With Git Clone", self.readme)
        self.assertIn("## Install By Downloading The Folder", self.readme)

    def test_readme_shows_explicit_skill_invocation(self) -> None:
        self.assertIn("Use unity-game-research. Study the skill system.", self.readme)


if __name__ == "__main__":
    unittest.main()

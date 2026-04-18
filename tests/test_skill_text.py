from __future__ import annotations

import re
from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillTextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_PATH.read_text(encoding="utf-8")

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


if __name__ == "__main__":
    unittest.main()

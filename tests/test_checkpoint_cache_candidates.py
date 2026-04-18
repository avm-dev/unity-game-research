from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import unity_research_checkpoint as checkpoint


class CacheCandidateTests(unittest.TestCase):
    def test_discover_cache_candidates_finds_generic_mobile_signatures(self) -> None:
        relative_files = {
            "Android/data/com.example.game/files/UnityCache/Shared/ab/123/__data",
            "cache/BundleFiles/events/chunk.bundle",
            "cache/files/assetbundle/scene/__data",
        }

        candidates = checkpoint.discover_cache_candidates(relative_files)

        self.assertIn("Android/data/com.example.game/files/UnityCache/Shared/ab/123/__data", candidates)
        self.assertIn("cache/BundleFiles/events/chunk.bundle", candidates)
        self.assertIn("cache/files/assetbundle/scene/__data", candidates)

    def test_build_manifest_records_cache_candidates_count(self) -> None:
        result = checkpoint.ScanResult(
            unity_confirmed=False,
            backend="unknown",
            unity_markers=[],
            files_tree=[],
            managed_assemblies=[],
            native_libs=[],
            asset_files=[],
            metadata_files=[],
            cache_candidates=["cache/BundleFiles/events/chunk.bundle", "Android/data/com.example.game/files/UnityCache/Shared/ab/123/__data"],
            topic_hits={},
            endpoint_hits=[],
            tool_availability={},
            managed_identifiers={},
            native_symbols={},
            il2cpp_targets={},
            recovery_plan=[],
            readiness_lines=[],
            install_plan_lines=[],
            os_info={},
            package_manager_paths={},
        )

        manifest = checkpoint.build_manifest(Path("input"), Path("output"), result, checkpoint.Counter())

        self.assertEqual(manifest["cache_candidates_count"], 2)


if __name__ == "__main__":
    unittest.main()

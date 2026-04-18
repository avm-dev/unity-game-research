from __future__ import annotations

import tempfile
import sys
from pathlib import Path
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import unity_research_checkpoint as checkpoint


class BackendDetectionTests(unittest.TestCase):
    def test_split_apk_il2cpp_layout_detects_il2cpp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.arm64_v8a/lib/arm64-v8a").mkdir(parents=True)
            (root / "config.arm64_v8a/assets/bin/Data/Managed/Metadata").mkdir(parents=True)
            (root / "config.arm64_v8a/lib/arm64-v8a/libil2cpp.so").write_bytes(b"")
            (root / "config.arm64_v8a/assets/bin/Data/Managed/Metadata/global-metadata.dat").write_bytes(b"")

            result = checkpoint.scan_tree(root, max_file_size=1024, refresh_raw=False, output_root=root / "game-knowledge")

        self.assertEqual(result.backend, "il2cpp")
        self.assertIn("config.arm64_v8a/lib/arm64-v8a/libil2cpp.so", result.native_libs)
        self.assertIn(
            "config.arm64_v8a/assets/bin/Data/Managed/Metadata/global-metadata.dat",
            result.metadata_files,
        )

    def test_partial_il2cpp_evidence_remains_unknown(self) -> None:
        self.assertEqual(
            checkpoint.classify_backend(
                {"config.arm64_v8a/assets/bin/Data/Managed/Metadata/global-metadata.dat"}
            ),
            "unknown",
        )

    def test_noncanonical_il2cpp_layout_detects_il2cpp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "lib/arm64-v8a").mkdir(parents=True)
            (root / "Data/il2cpp_data/Metadata").mkdir(parents=True)
            (root / "lib/arm64-v8a/libil2cpp.so").write_bytes(b"")
            (root / "Data/il2cpp_data/Metadata/global-metadata.dat").write_bytes(b"")

            result = checkpoint.scan_tree(root, max_file_size=1024, refresh_raw=False, output_root=root / "game-knowledge")

        self.assertEqual(result.backend, "il2cpp")
        self.assertIn("lib/arm64-v8a/libil2cpp.so", result.native_libs)
        self.assertIn("Data/il2cpp_data/Metadata/global-metadata.dat", result.metadata_files)

    def test_find_unity_markers_reports_nested_unity_libraries(self) -> None:
        unity_confirmed, markers = checkpoint.find_unity_markers(
            {
                "config.arm64_v8a/lib/arm64-v8a/libunity.so",
                "config.arm64_v8a/lib/arm64-v8a/libil2cpp.so",
            }
        )

        self.assertTrue(unity_confirmed)
        self.assertIn("config.arm64_v8a/lib/arm64-v8a/libunity.so", markers)
        self.assertIn("config.arm64_v8a/lib/arm64-v8a/libil2cpp.so", markers)

    def test_basenames_in_vendor_docs_do_not_trigger_unity_or_il2cpp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/vendor").mkdir(parents=True)
            (root / "docs/vendor/libunity.so").write_bytes(b"")
            (root / "docs/vendor/libil2cpp.so").write_bytes(b"")
            (root / "docs/vendor/global-metadata.dat").write_bytes(b"")

            result = checkpoint.scan_tree(root, max_file_size=1024, refresh_raw=False, output_root=root / "game-knowledge")

        self.assertFalse(result.unity_confirmed)
        self.assertEqual(result.backend, "unknown")
        self.assertNotIn("docs/vendor/libunity.so", result.native_libs)
        self.assertNotIn("docs/vendor/libil2cpp.so", result.native_libs)
        self.assertNotIn("docs/vendor/global-metadata.dat", result.metadata_files)


if __name__ == "__main__":
    unittest.main()

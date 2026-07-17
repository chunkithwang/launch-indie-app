#!/usr/bin/env python3
"""Self-contained repository tests for launch-indie-app."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "launch-indie-app"
SKILL_MD = SKILL_DIR / "SKILL.md"
TASKS_JSON = SKILL_DIR / "references" / "launch-tasks.json"
MACOS_OVERRIDES_JSON = SKILL_DIR / "references" / "macos-task-overrides.json"
MACOS_DISTRIBUTION = SKILL_DIR / "references" / "macos-distribution.md"
GENERATOR = SKILL_DIR / "scripts" / "build_launch_plan.py"

EXPECTED_PHASE_COUNTS = {
    "Foundations": 7,
    "Store presence and beta": 10,
    "Launch week prep": 6,
    "Launch day": 5,
    "Feedback fortnight": 7,
    "Long tail": 5,
}


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError("SKILL.md frontmatter is not closed")

    values: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        if not raw_line.strip():
            continue
        key, separator, value = raw_line.partition(":")
        if not separator:
            raise AssertionError(f"invalid frontmatter line: {raw_line}")
        values[key.strip()] = value.strip()
    return values


class SkillStructureTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        required = [
            SKILL_MD,
            SKILL_DIR / "agents" / "openai.yaml",
            TASKS_JSON,
            MACOS_OVERRIDES_JSON,
            SKILL_DIR / "references" / "apple-requirements.md",
            MACOS_DISTRIBUTION,
            SKILL_DIR / "references" / "retrospective-lessons.md",
            SKILL_DIR / "references" / "source-coverage.md",
            GENERATOR,
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_frontmatter_contract(self) -> None:
        frontmatter = read_frontmatter(SKILL_MD)
        self.assertEqual(set(frontmatter), {"name", "description"})
        self.assertEqual(frontmatter["name"], SKILL_DIR.name)
        self.assertTrue(frontmatter["description"])
        self.assertLessEqual(len(frontmatter["description"]), 1024)

    def test_no_repository_docs_inside_skill(self) -> None:
        forbidden = {
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "INSTALLATION_GUIDE.md",
            "QUICK_REFERENCE.md",
        }
        present = {path.name for path in SKILL_DIR.rglob("*") if path.is_file()}
        self.assertFalse(forbidden & present)
        self.assertFalse(any(path.name == "__pycache__" for path in SKILL_DIR.rglob("*")))
        self.assertFalse(any(path.suffix == ".pyc" for path in SKILL_DIR.rglob("*")))


class TaskModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = json.loads(TASKS_JSON.read_text(encoding="utf-8"))
        cls.tasks = cls.model["tasks"]
        cls.macos_overrides = json.loads(MACOS_OVERRIDES_JSON.read_text(encoding="utf-8"))

    def test_source_phase_counts_and_span(self) -> None:
        self.assertEqual(len(self.tasks), 40)
        self.assertEqual(Counter(task["phase"] for task in self.tasks), EXPECTED_PHASE_COUNTS)
        offsets = [task["day_offset"] for task in self.tasks]
        self.assertEqual(offsets, sorted(offsets))
        self.assertEqual(min(offsets), -45)
        self.assertEqual(max(offsets), 60)

    def test_ids_and_dependencies(self) -> None:
        ids = [task["id"] for task in self.tasks]
        self.assertEqual(len(ids), len(set(ids)))
        id_to_offset = {task["id"]: task["day_offset"] for task in self.tasks}
        for task in self.tasks:
            for dependency in task["dependencies"]:
                self.assertIn(dependency, id_to_offset)
                self.assertLessEqual(id_to_offset[dependency], task["day_offset"])

    def test_macos_override_integrity(self) -> None:
        self.assertEqual(self.macos_overrides["platform"], "macos")
        self.assertEqual(
            self.macos_overrides["distribution_modes"],
            ["app-store", "direct", "both"],
        )
        task_ids = {task["id"] for task in self.tasks}
        overrides = self.macos_overrides["overrides"]
        self.assertTrue(set(overrides).issubset(task_ids))
        self.assertTrue(
            {
                "FND-05",
                "STB-02",
                "STB-05",
                "STB-06",
                "STB-07",
                "LWP-04",
                "DAY-01",
                "FBF-03",
            }.issubset(overrides)
        )
        for override in overrides.values():
            guidance = override.get("distribution_guidance", {})
            self.assertTrue(set(guidance).issubset({"app-store", "direct"}))
            self.assertTrue(all(value.strip() for value in guidance.values()))


class GeneratorTests(unittest.TestCase):
    def run_generator(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATOR), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_internal_validation(self) -> None:
        ios_result = self.run_generator(
            "--ship-date",
            "2026-09-15",
            "--today",
            "2026-07-17",
            "--validate-only",
        )
        self.assertIn("40 tasks", ios_result.stdout)
        self.assertIn("iOS (app-store)", ios_result.stdout)

        macos_result = self.run_generator(
            "--ship-date",
            "2026-09-15",
            "--platform",
            "macos",
            "--distribution",
            "both",
            "--validate-only",
        )
        self.assertIn("40 tasks", macos_result.stdout)
        self.assertIn("macOS (both)", macos_result.stdout)

    def test_all_output_formats_contain_all_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            outputs = {
                "markdown": output_dir / "plan.md",
                "csv": output_dir / "plan.csv",
                "json": output_dir / "plan.json",
            }
            for format_name, output_path in outputs.items():
                self.run_generator(
                    "--ship-date",
                    "2026-09-15",
                    "--today",
                    "2026-07-17",
                    "--format",
                    format_name,
                    "--output",
                    str(output_path),
                )
                self.assertTrue(output_path.is_file())

            markdown = outputs["markdown"].read_text(encoding="utf-8")
            self.assertIn("Canonical tasks: 40", markdown)
            self.assertEqual(markdown.count("| FND-"), 7)

            with outputs["csv"].open(encoding="utf-8", newline="") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 40)

            payload = json.loads(outputs["json"].read_text(encoding="utf-8"))
            self.assertEqual(payload["platform"], "ios")
            self.assertEqual(payload["distribution"], "app-store")
            self.assertEqual(payload["canonical_task_count"], 40)
            self.assertEqual(len(payload["tasks"]), 40)

    def test_macos_outputs_apply_channel_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            markdown_path = output_dir / "macos-both.md"
            csv_path = output_dir / "macos-both.csv"
            json_path = output_dir / "macos-both.json"

            for format_name, output_path in (
                ("markdown", markdown_path),
                ("csv", csv_path),
                ("json", json_path),
            ):
                self.run_generator(
                    "--ship-date",
                    "2026-09-15",
                    "--today",
                    "2026-07-17",
                    "--platform",
                    "macos",
                    "--distribution",
                    "both",
                    "--format",
                    format_name,
                    "--output",
                    str(output_path),
                )

            markdown = markdown_path.read_text(encoding="utf-8")
            self.assertIn("# Indie macOS App Launch Plan", markdown)
            self.assertIn("Mac App Store: enable App Sandbox", markdown)
            self.assertIn("Direct: archive with Developer ID", markdown)
            self.assertIn("1280x800", markdown)

            with csv_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 40)
            self.assertEqual({row["platform"] for row in rows}, {"macos"})
            self.assertEqual({row["distribution"] for row in rows}, {"both"})

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["platform"], "macos")
            self.assertEqual(payload["distribution"], "both")
            self.assertEqual(payload["canonical_task_count"], 40)

    def test_macos_direct_excludes_store_only_guidance(self) -> None:
        result = self.run_generator(
            "--ship-date",
            "2026-09-15",
            "--platform",
            "macos",
            "--distribution",
            "direct",
            "--format",
            "json",
        )
        payload = json.loads(result.stdout)
        tasks = {task["id"]: task for task in payload["tasks"]}
        guidance = tasks["STB-07"]["distribution_guidance"]
        self.assertIn("notarytool", guidance)
        self.assertNotIn("App Review", guidance)
        self.assertIn("signing defects", tasks["STB-07"]["rationale"])
        self.assertNotIn("pre-order converts", tasks["STB-07"]["rationale"])

    def test_macos_app_store_excludes_direct_guidance(self) -> None:
        result = self.run_generator(
            "--ship-date",
            "2026-09-15",
            "--platform",
            "macos",
            "--distribution",
            "app-store",
            "--format",
            "json",
        )
        payload = json.loads(result.stdout)
        tasks = {task["id"]: task for task in payload["tasks"]}
        guidance = tasks["STB-07"]["distribution_guidance"]
        self.assertIn("App Review", guidance)
        self.assertNotIn("notarytool", guidance)

    def test_ios_rejects_macos_distribution_flag(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--ship-date",
                "2026-09-15",
                "--platform",
                "ios",
                "--distribution",
                "direct",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("only valid with --platform macos", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

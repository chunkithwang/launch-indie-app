#!/usr/bin/env python3
"""Build a dated indie iOS or macOS launch plan from the bundled 40-task model."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
TASKS_PATH = SKILL_DIR / "references" / "launch-tasks.json"
MACOS_OVERRIDES_PATH = SKILL_DIR / "references" / "macos-task-overrides.json"
EXPECTED_TASK_COUNT = 40
EXPECTED_START_OFFSET = -45
EXPECTED_END_OFFSET = 60
PLATFORM_LABELS = {"ios": "iOS", "macos": "macOS"}
MACOS_DISTRIBUTIONS = ("app-store", "direct", "both")
OVERRIDE_FIELDS = {"action", "rationale", "done_when", "applies_when"}
EXPECTED_PHASE_COUNTS = {
    "Foundations": 7,
    "Store presence and beta": 10,
    "Launch week prep": 6,
    "Launch day": 5,
    "Feedback fortnight": 7,
    "Long tail": 5,
}


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid date '{value}'; expected YYYY-MM-DD"
        ) from exc


def load_model(
    platform: str = "ios", distribution: str = "app-store"
) -> dict[str, Any]:
    with TASKS_PATH.open(encoding="utf-8") as handle:
        model = json.load(handle)
    validate_model(model)
    if platform == "macos":
        with MACOS_OVERRIDES_PATH.open(encoding="utf-8") as handle:
            overrides = json.load(handle)
        validate_macos_overrides(overrides, model)
        model = apply_macos_overrides(model, overrides, distribution)
    return model


def validate_model(model: dict[str, Any]) -> None:
    tasks = model.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("launch-tasks.json must contain a tasks array")
    if len(tasks) != EXPECTED_TASK_COUNT:
        raise ValueError(f"expected {EXPECTED_TASK_COUNT} tasks, found {len(tasks)}")

    ids = [task.get("id") for task in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("task IDs must be unique")

    offsets = [task.get("day_offset") for task in tasks]
    if not all(isinstance(offset, int) for offset in offsets):
        raise ValueError("every day_offset must be an integer")
    if offsets != sorted(offsets):
        raise ValueError("tasks must be ordered by day_offset")
    if min(offsets) != EXPECTED_START_OFFSET or max(offsets) != EXPECTED_END_OFFSET:
        raise ValueError("task offsets must span day -45 through day +60")
    phase_counts = Counter(task.get("phase") for task in tasks)
    if dict(phase_counts) != EXPECTED_PHASE_COUNTS:
        raise ValueError(
            f"phase task counts differ from the source article: {dict(phase_counts)}"
        )

    required = {
        "id",
        "day_offset",
        "phase",
        "action",
        "rationale",
        "done_when",
        "dependencies",
    }
    id_to_offset = {task["id"]: task["day_offset"] for task in tasks}
    for task in tasks:
        missing = sorted(required - task.keys())
        if missing:
            raise ValueError(f"task {task.get('id', '<unknown>')} is missing: {', '.join(missing)}")
        unknown_dependencies = sorted(set(task["dependencies"]) - set(ids))
        if unknown_dependencies:
            raise ValueError(
                f"task {task['id']} references unknown dependencies: {', '.join(unknown_dependencies)}"
            )
        future_dependencies = [
            dependency
            for dependency in task["dependencies"]
            if id_to_offset[dependency] > task["day_offset"]
        ]
        if future_dependencies:
            raise ValueError(
                f"task {task['id']} depends on later tasks: {', '.join(future_dependencies)}"
            )


def validate_macos_overrides(overrides: dict[str, Any], model: dict[str, Any]) -> None:
    if overrides.get("platform") != "macos":
        raise ValueError("macos-task-overrides.json must target the macos platform")
    if tuple(overrides.get("distribution_modes", ())) != MACOS_DISTRIBUTIONS:
        raise ValueError("macOS distribution modes must be app-store, direct, and both")

    task_overrides = overrides.get("overrides")
    if not isinstance(task_overrides, dict) or not task_overrides:
        raise ValueError("macos-task-overrides.json must contain a non-empty overrides object")

    base_ids = {task["id"] for task in model["tasks"]}
    unknown_ids = sorted(set(task_overrides) - base_ids)
    if unknown_ids:
        raise ValueError(f"macOS overrides reference unknown tasks: {', '.join(unknown_ids)}")

    for task_id, override in task_overrides.items():
        if not isinstance(override, dict):
            raise ValueError(f"macOS override {task_id} must be an object")
        unknown_fields = sorted(
            set(override) - OVERRIDE_FIELDS - {"distribution_guidance"}
        )
        if unknown_fields:
            raise ValueError(
                f"macOS override {task_id} has unknown fields: {', '.join(unknown_fields)}"
            )
        for field in OVERRIDE_FIELDS & set(override):
            if not isinstance(override[field], str) or not override[field].strip():
                raise ValueError(f"macOS override {task_id}.{field} must be a non-empty string")

        guidance = override.get("distribution_guidance", {})
        if not isinstance(guidance, dict):
            raise ValueError(f"macOS override {task_id}.distribution_guidance must be an object")
        unknown_modes = sorted(set(guidance) - {"app-store", "direct"})
        if unknown_modes:
            raise ValueError(
                f"macOS override {task_id} has unknown distribution guidance: "
                f"{', '.join(unknown_modes)}"
            )
        for mode, text in guidance.items():
            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"macOS override {task_id}.distribution_guidance.{mode} "
                    "must be a non-empty string"
                )


def apply_macos_overrides(
    model: dict[str, Any], overrides: dict[str, Any], distribution: str
) -> dict[str, Any]:
    if distribution not in MACOS_DISTRIBUTIONS:
        raise ValueError(f"unsupported macOS distribution mode: {distribution}")

    task_overrides = overrides["overrides"]
    resolved_tasks: list[dict[str, Any]] = []
    for task in model["tasks"]:
        resolved = dict(task)
        override = task_overrides.get(task["id"], {})
        for field in OVERRIDE_FIELDS:
            if field in override:
                resolved[field] = override[field]

        guidance = override.get("distribution_guidance", {})
        selected_modes = (
            ("app-store", "direct") if distribution == "both" else (distribution,)
        )
        selected_guidance = [guidance[mode] for mode in selected_modes if mode in guidance]
        if selected_guidance:
            resolved["distribution_guidance"] = " ".join(selected_guidance)
        resolved_tasks.append(resolved)

    resolved_model = dict(model)
    resolved_model["title"] = overrides["title"]
    resolved_model["tasks"] = resolved_tasks
    return resolved_model


def day_label(offset: int) -> str:
    if offset == 0:
        return "D0"
    return f"D{offset:+d}"


def date_status(task_date: date, today: date) -> str:
    if task_date < today:
        return "overdue"
    if task_date == today:
        return "due today"
    return "upcoming"


def schedule(
    model: dict[str, Any],
    ship_date: date,
    today: date,
    platform: str,
    distribution: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in model["tasks"]:
        scheduled_date = ship_date + timedelta(days=task["day_offset"])
        row = dict(task)
        row["day"] = day_label(task["day_offset"])
        row["scheduled_date"] = scheduled_date.isoformat()
        row["calendar_status"] = date_status(scheduled_date, today)
        row["platform"] = platform
        row["distribution"] = distribution
        rows.append(row)
    return rows


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown(
    rows: list[dict[str, Any]],
    ship_date: date,
    today: date,
    platform: str,
    distribution: str,
) -> str:
    platform_label = PLATFORM_LABELS[platform]
    lines = [
        f"# Indie {platform_label} App Launch Plan",
        "",
        f"- Platform: {platform_label}",
        f"- Distribution: {distribution}",
        f"- Ship date: {ship_date.isoformat()}",
        f"- Status date: {today.isoformat()}",
        f"- Canonical window: {(ship_date + timedelta(days=EXPECTED_START_OFFSET)).isoformat()} to "
        f"{(ship_date + timedelta(days=EXPECTED_END_OFFSET)).isoformat()}",
        f"- Canonical tasks: {len(rows)}",
        "",
    ]

    current_phase = None
    for row in rows:
        if row["phase"] != current_phase:
            if current_phase is not None:
                lines.append("")
            current_phase = row["phase"]
            lines.extend(
                [
                    f"## {current_phase}",
                    "",
                    "| ID | Day | Date | Calendar status | Task | Done when |",
                    "|---|---:|---|---|---|---|",
                ]
            )
        lines.append(
            "| {id} | {day} | {scheduled_date} | {calendar_status} | {action} | {done_when} |".format(
                **{key: escape_cell(str(value)) for key, value in row.items()}
            )
        )
        if row.get("applies_when"):
            lines.append(
                f"|  |  |  | Conditional | Applies when: {escape_cell(row['applies_when'])} |  |"
            )
        if row.get("distribution_guidance"):
            lines.append(
                "|  |  |  | Distribution | {guidance} |  |".format(
                    guidance=escape_cell(row["distribution_guidance"])
                )
            )

    lines.extend(
        [
            "",
            "## Planning note",
            "",
            "Calendar status is date-based only. Replace it with evidence-backed project status such as "
            "planned, in progress, blocked, done, or not applicable during launch management.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_json(
    rows: list[dict[str, Any]],
    ship_date: date,
    today: date,
    platform: str,
    distribution: str,
) -> str:
    payload = {
        "platform": platform,
        "distribution": distribution,
        "ship_date": ship_date.isoformat(),
        "status_date": today.isoformat(),
        "canonical_task_count": len(rows),
        "tasks": rows,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_csv(rows: list[dict[str, Any]]) -> str:
    output = io.StringIO(newline="")
    fields = [
        "id",
        "phase",
        "day",
        "day_offset",
        "scheduled_date",
        "calendar_status",
        "platform",
        "distribution",
        "action",
        "rationale",
        "done_when",
        "dependencies",
        "applies_when",
        "distribution_guidance",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        serializable = dict(row)
        serializable["dependencies"] = ",".join(row["dependencies"])
        serializable.setdefault("applies_when", "")
        serializable.setdefault("distribution_guidance", "")
        writer.writerow(serializable)
    return output.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ship-date",
        required=True,
        type=parse_date,
        help="Release date in YYYY-MM-DD",
    )
    parser.add_argument(
        "--platform",
        choices=tuple(PLATFORM_LABELS),
        default="ios",
        help="Target Apple platform; defaults to ios",
    )
    parser.add_argument(
        "--distribution",
        choices=MACOS_DISTRIBUTIONS,
        help="macOS distribution mode; defaults to both for macOS",
    )
    parser.add_argument(
        "--today",
        type=parse_date,
        default=date.today(),
        help="Status date in YYYY-MM-DD; defaults to the local current date",
    )
    parser.add_argument(
        "--format", choices=("markdown", "csv", "json"), default="markdown"
    )
    parser.add_argument("--output", type=Path, help="Write output to this file instead of stdout")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the bundled model and print a short success message",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.platform == "ios" and args.distribution is not None:
        parser.error("--distribution is only valid with --platform macos")
    distribution = args.distribution or (
        "both" if args.platform == "macos" else "app-store"
    )
    try:
        model = load_model(args.platform, distribution)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.validate_only:
        print(
            f"OK: {len(model['tasks'])} tasks span "
            f"D{EXPECTED_START_OFFSET} through D+{EXPECTED_END_OFFSET} for "
            f"{PLATFORM_LABELS[args.platform]} ({distribution})."
        )
        return 0

    rows = schedule(model, args.ship_date, args.today, args.platform, distribution)
    if args.format == "json":
        content = render_json(
            rows, args.ship_date, args.today, args.platform, distribution
        )
    elif args.format == "csv":
        content = render_csv(rows)
    else:
        content = render_markdown(
            rows, args.ship_date, args.today, args.platform, distribution
        )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

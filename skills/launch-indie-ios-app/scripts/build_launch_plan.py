#!/usr/bin/env python3
"""Build a dated indie iOS launch plan from the bundled 40-task model."""

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
EXPECTED_TASK_COUNT = 40
EXPECTED_START_OFFSET = -45
EXPECTED_END_OFFSET = 60
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
        raise argparse.ArgumentTypeError(f"invalid date '{value}'; expected YYYY-MM-DD") from exc


def load_model() -> dict[str, Any]:
    with TASKS_PATH.open(encoding="utf-8") as handle:
        model = json.load(handle)
    validate_model(model)
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

    required = {"id", "day_offset", "phase", "action", "rationale", "done_when", "dependencies"}
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


def schedule(model: dict[str, Any], ship_date: date, today: date) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in model["tasks"]:
        scheduled_date = ship_date + timedelta(days=task["day_offset"])
        row = dict(task)
        row["day"] = day_label(task["day_offset"])
        row["scheduled_date"] = scheduled_date.isoformat()
        row["calendar_status"] = date_status(scheduled_date, today)
        rows.append(row)
    return rows


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown(rows: list[dict[str, Any]], ship_date: date, today: date) -> str:
    lines = [
        "# Indie iOS App Launch Plan",
        "",
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


def render_json(rows: list[dict[str, Any]], ship_date: date, today: date) -> str:
    payload = {
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
        "action",
        "rationale",
        "done_when",
        "dependencies",
        "applies_when",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        serializable = dict(row)
        serializable["dependencies"] = ",".join(row["dependencies"])
        serializable.setdefault("applies_when", "")
        writer.writerow(serializable)
    return output.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ship-date", required=True, type=parse_date, help="Release date in YYYY-MM-DD")
    parser.add_argument(
        "--today",
        type=parse_date,
        default=date.today(),
        help="Status date in YYYY-MM-DD; defaults to the local current date",
    )
    parser.add_argument("--format", choices=("markdown", "csv", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write output to this file instead of stdout")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the bundled model and print a short success message",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        model = load_model()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.validate_only:
        print(
            f"OK: {len(model['tasks'])} tasks span "
            f"D{EXPECTED_START_OFFSET} through D+{EXPECTED_END_OFFSET}."
        )
        return 0

    rows = schedule(model, args.ship_date, args.today)
    if args.format == "json":
        content = render_json(rows, args.ship_date, args.today)
    elif args.format == "csv":
        content = render_csv(rows)
    else:
        content = render_markdown(rows, args.ship_date, args.today)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

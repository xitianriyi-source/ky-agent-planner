#!/usr/bin/env python3
"""Read-only integrity verifier for the postgraduate-exam planning system."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path("02_项目/考研Agent规划系统")
PLAN_ROOT = Path("01_学科/考研计划")
BOARD_PATH = PLAN_ROOT / "考研任务看板.md"
ROUTE_PATH = PLAN_ROOT / "阶段路线图.md"
DAILY_ROOT = Path("00_Daily")
WEEKLY_ROOT = PLAN_ROOT / "周计划"
COORDINATION_ROOT = PROJECT_ROOT / "coordination"
RULES_ROOT = PROJECT_ROOT / "rules"

REQUIRED_KANBAN_SECTIONS = [
    "今日（最多3项）",
    "进行中（最多1项）",
    "本周队列",
    "完成",
    "取消/改期",
]
KANBAN_LIMITS = {"今日（最多3项）": 3, "进行中（最多1项）": 1}
ACTIVE_KANBAN_SECTIONS = set(REQUIRED_KANBAN_SECTIONS[:3])
TASK_RE = re.compile(r"^\s*-\s+\[([ xX])\]\s+(.*)$")
BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9_-]+)\s*$")
TASK_ENVELOPE_RE = re.compile(r"^【([^｜】]+)｜(P[0-2])｜([^】]+)】")
ISO_DATE_NAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")
LOOSE_DATE_NAME_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})\.md$")
WEEKLY_NAME_RE = re.compile(r"^(\d{4}-W\d{2})-(草案|正式)\.md$")
HANDOFF_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}-.+\.md$")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str
    line: int | None = None


@dataclass
class VerificationReport:
    vault_root: str
    issues: list[Issue] = field(default_factory=list)

    def add(
        self,
        severity: str,
        code: str,
        path: str,
        message: str,
        line: int | None = None,
    ) -> None:
        issue = Issue(severity, code, path, message, line)
        if issue not in self.issues:
            self.issues.append(issue)

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "ERROR"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "WARN"]

    @property
    def status(self) -> str:
        return "FAIL" if self.errors else "PASS"

    def as_dict(self) -> dict[str, Any]:
        ordered = sorted(self.issues, key=issue_sort_key)
        return {
            "status": self.status,
            "vault_root": self.vault_root,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "issues": [asdict(issue) for issue in ordered],
        }


@dataclass
class MarkdownDocument:
    path: Path
    text: str
    frontmatter: dict[str, Any]
    has_frontmatter: bool
    frontmatter_problems: list[str]


@dataclass(frozen=True)
class TaskOccurrence:
    block_id: str
    path: str
    line: int


class PlanningSystemVerifier:
    """Verify the planning system through one read-only interface."""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root.resolve()
        self.report = VerificationReport(str(self.vault_root))
        self._documents: dict[Path, MarkdownDocument] = {}
        self._frontmatter_reported: set[Path] = set()

    def verify(self) -> VerificationReport:
        self._check_core_files()
        cutoff = self._check_kanban()
        self._check_global_block_ids()
        formal_weeks = self._check_weekly_plans()
        self._check_daily(cutoff)
        self._check_coordination()
        self._check_rules()
        self._check_route(formal_weeks)
        return self.report

    def _relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.vault_root).as_posix()
        except ValueError:
            return path.as_posix()

    def _absolute(self, relative: Path | str) -> Path:
        return self.vault_root / relative

    def _add(
        self,
        severity: str,
        code: str,
        path: Path | str,
        message: str,
        line: int | None = None,
    ) -> None:
        display_path = self._relative(path) if isinstance(path, Path) else path
        self.report.add(severity, code, display_path, message, line)

    def _document(self, path: Path) -> MarkdownDocument:
        path = path.resolve()
        if path in self._documents:
            return self._documents[path]
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self._add("ERROR", "file_read_error", path, str(exc))
            document = MarkdownDocument(path, "", {}, False, [str(exc)])
        else:
            frontmatter, has_frontmatter, problems = parse_frontmatter(text)
            document = MarkdownDocument(
                path, text, frontmatter, has_frontmatter, problems
            )
        self._documents[path] = document
        return document

    def _frontmatter(self, path: Path) -> dict[str, Any]:
        document = self._document(path)
        if path.resolve() not in self._frontmatter_reported:
            self._frontmatter_reported.add(path.resolve())
            if not document.has_frontmatter:
                self._add(
                    "ERROR",
                    "missing_frontmatter",
                    path,
                    "Markdown file must start with YAML frontmatter.",
                )
            for problem in document.frontmatter_problems:
                self._add("ERROR", "invalid_frontmatter", path, problem)
        return document.frontmatter

    def _require_fields(
        self, path: Path, frontmatter: dict[str, Any], fields: Iterable[str]
    ) -> None:
        for key in fields:
            if key not in frontmatter or frontmatter[key] in (None, ""):
                self._add(
                    "ERROR",
                    "missing_required_field",
                    path,
                    f"Required frontmatter field is missing or empty: {key}",
                )

    def _check_core_files(self) -> None:
        core_files = {
            PROJECT_ROOT / "PROJECT.md": ("type", "version", "status", "updated"),
            PROJECT_ROOT / "SPEC.md": ("type", "version", "status", "updated"),
            PROJECT_ROOT / "HANDOFF.md": ("type", "status", "updated"),
            BOARD_PATH: ("kanban-plugin", "type", "canonical_since"),
            ROUTE_PATH: ("type", "status", "current_stage"),
            COORDINATION_ROOT / "README.md": ("type", "status", "updated"),
        }
        for relative, required_fields in core_files.items():
            path = self._absolute(relative)
            if not path.is_file():
                self._add("ERROR", "missing_core_file", path, "Required file is absent.")
                continue
            frontmatter = self._frontmatter(path)
            self._require_fields(path, frontmatter, required_fields)

    def _check_kanban(self) -> date:
        path = self._absolute(BOARD_PATH)
        default_cutoff = date(2026, 8, 19)
        if not path.is_file():
            return default_cutoff

        document = self._document(path)
        frontmatter = self._frontmatter(path)
        cutoff = parse_iso_date(str(frontmatter.get("canonical_since", "")))
        if cutoff is None:
            self._add(
                "ERROR",
                "invalid_canonical_since",
                path,
                "canonical_since must use YYYY-MM-DD.",
            )
            cutoff = default_cutoff

        sections: dict[str, list[tuple[int, str, str]]] = {}
        section_order: list[str] = []
        current_section: str | None = None
        in_fence = False

        for line_number, line in enumerate(document.text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            heading = re.match(r"^##\s+(.+?)\s*$", line)
            if heading:
                current_section = heading.group(1)
                section_order.append(current_section)
                sections.setdefault(current_section, [])
                continue
            task = TASK_RE.match(line)
            if not task or current_section is None:
                continue
            checked = task.group(1).lower() == "x"
            body = task.group(2).strip()
            sections.setdefault(current_section, []).append(
                (line_number, "x" if checked else " ", body)
            )

        for section in REQUIRED_KANBAN_SECTIONS:
            count = section_order.count(section)
            if count == 0:
                self._add(
                    "ERROR",
                    "missing_kanban_section",
                    path,
                    f"Required Kanban section is absent: {section}",
                )
            elif count > 1:
                self._add(
                    "ERROR",
                    "duplicate_kanban_section",
                    path,
                    f"Kanban section appears {count} times: {section}",
                )

        expected_order = [
            section for section in REQUIRED_KANBAN_SECTIONS if section in section_order
        ]
        actual_order = [
            section for section in section_order if section in REQUIRED_KANBAN_SECTIONS
        ]
        if actual_order != expected_order:
            self._add(
                "ERROR",
                "kanban_section_order",
                path,
                "Kanban sections are not in the order required by SPEC.md.",
            )

        for section, limit in KANBAN_LIMITS.items():
            task_count = len(sections.get(section, []))
            if task_count > limit:
                self._add(
                    "ERROR",
                    "kanban_wip_limit",
                    path,
                    f"{section} contains {task_count} tasks; maximum is {limit}.",
                )

        for section, tasks in sections.items():
            for line_number, checked, body in tasks:
                block_match = BLOCK_ID_RE.search(body)
                if not block_match:
                    if body.startswith("历史迁移记录"):
                        message = (
                            "Historical migration records must be plain bullets, not "
                            "unchecked task instances."
                        )
                        code = "kanban_historical_checkbox"
                    else:
                        message = "Kanban task is missing a stable block id."
                        code = "kanban_missing_block_id"
                    self._add("ERROR", code, path, message, line_number)
                    if body.startswith("历史迁移记录"):
                        continue

                if not TASK_ENVELOPE_RE.match(body):
                    self._add(
                        "ERROR",
                        "kanban_task_envelope",
                        path,
                        "Task must start with 【科目｜P0-P2｜日期或截止日】.",
                        line_number,
                    )
                if "验收：" not in body:
                    self._add(
                        "ERROR",
                        "kanban_missing_acceptance",
                        path,
                        "Task must contain an explicit 验收： clause.",
                        line_number,
                    )
                if section == "完成" and checked != "x":
                    self._add(
                        "ERROR",
                        "kanban_completion_mismatch",
                        path,
                        "Task in 完成 must use a checked checkbox.",
                        line_number,
                    )
                if section in ACTIVE_KANBAN_SECTIONS and checked == "x":
                    self._add(
                        "ERROR",
                        "kanban_active_checked",
                        path,
                        "Checked task must be moved out of an active Kanban section.",
                        line_number,
                    )

        return cutoff

    def _check_global_block_ids(self) -> None:
        occurrences: dict[str, list[TaskOccurrence]] = {}
        for path in self.vault_root.rglob("*.md"):
            if should_skip_path(path, self.vault_root):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            for line_number, line in iter_non_fenced_lines(text):
                task = TASK_RE.match(line)
                if not task:
                    continue
                block_match = BLOCK_ID_RE.search(task.group(2))
                if not block_match:
                    continue
                block_id = block_match.group(1)
                occurrence = TaskOccurrence(
                    block_id, self._relative(path), line_number
                )
                occurrences.setdefault(block_id, []).append(occurrence)

        for block_id, locations in occurrences.items():
            if len(locations) < 2:
                continue
            location_text = ", ".join(
                f"{item.path}:{item.line}" for item in locations
            )
            first = locations[0]
            self.report.add(
                "ERROR",
                "duplicate_block_id",
                first.path,
                f"Block id {block_id} has {len(locations)} checkbox instances: "
                f"{location_text}",
                first.line,
            )

    def _check_weekly_plans(self) -> set[str]:
        root = self._absolute(WEEKLY_ROOT)
        formal_by_week: dict[str, list[Path]] = {}
        draft_by_week: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
        if not root.is_dir():
            self._add("ERROR", "missing_weekly_directory", root, "Directory is absent.")
            return set()

        for path in sorted(root.glob("*.md")):
            if path.name == "README.md":
                continue
            name_match = WEEKLY_NAME_RE.match(path.name)
            if not name_match:
                self._add(
                    "WARN",
                    "unexpected_weekly_filename",
                    path,
                    "Weekly plan filename should be YYYY-Www-草案.md or YYYY-Www-正式.md.",
                )
                continue
            filename_week, kind = name_match.groups()
            frontmatter = self._frontmatter(path)
            self._require_fields(
                path,
                frontmatter,
                (
                    "type",
                    "week",
                    "status",
                    "generated_by",
                    "generated_at",
                    "date_start",
                    "date_end",
                    "capacity_hours",
                    "committed_hours",
                    "buffer_hours",
                    "stage",
                ),
            )
            week = str(frontmatter.get("week", ""))
            if week != filename_week:
                self._add(
                    "ERROR",
                    "weekly_week_mismatch",
                    path,
                    f"Frontmatter week {week!r} does not match filename {filename_week}.",
                )

            self._check_capacity(path, frontmatter)
            for key in ("date_start", "date_end"):
                if parse_iso_date(str(frontmatter.get(key, ""))) is None:
                    self._add(
                        "ERROR",
                        "invalid_weekly_date",
                        path,
                        f"{key} must use YYYY-MM-DD.",
                    )

            status = str(frontmatter.get("status", ""))
            if kind == "正式":
                formal_by_week.setdefault(filename_week, []).append(path)
                if status != "formal":
                    self._add(
                        "ERROR",
                        "formal_plan_status",
                        path,
                        "Formal plan must use status: formal.",
                    )
                self._require_fields(path, frontmatter, ("confirmed_by", "confirmed_at"))
                if frontmatter.get("confirmed_by") != "user":
                    self._add(
                        "ERROR",
                        "formal_plan_confirmation",
                        path,
                        "Formal plan must be confirmed_by: user.",
                    )
            else:
                draft_by_week.setdefault(filename_week, []).append((path, frontmatter))
                if status not in {"draft", "superseded"}:
                    self._add(
                        "ERROR",
                        "draft_plan_status",
                        path,
                        "Draft plan status must be draft or superseded.",
                    )

        for week, paths in formal_by_week.items():
            if len(paths) > 1:
                self._add(
                    "ERROR",
                    "multiple_formal_plans",
                    paths[0],
                    f"Week {week} has {len(paths)} formal plans.",
                )
            for draft_path, frontmatter in draft_by_week.get(week, []):
                if frontmatter.get("status") != "superseded":
                    self._add(
                        "ERROR",
                        "draft_not_superseded",
                        draft_path,
                        f"Week {week} already has a formal plan; its draft must be superseded.",
                    )

        return set(formal_by_week)

    def _check_capacity(self, path: Path, frontmatter: dict[str, Any]) -> None:
        values: dict[str, float] = {}
        for key in ("capacity_hours", "committed_hours", "buffer_hours"):
            value = to_number(frontmatter.get(key))
            if value is None:
                self._add(
                    "ERROR",
                    "invalid_capacity",
                    path,
                    f"{key} must be numeric.",
                )
                return
            values[key] = value
        expected = values["committed_hours"] + values["buffer_hours"]
        if abs(values["capacity_hours"] - expected) > 1e-9:
            self._add(
                "ERROR",
                "capacity_mismatch",
                path,
                "capacity_hours must equal committed_hours + buffer_hours.",
            )

    def _check_daily(self, cutoff: date) -> None:
        root = self._absolute(DAILY_ROOT)
        if not root.is_dir():
            self._add("ERROR", "missing_daily_directory", root, "Directory is absent.")
            return

        for path in sorted(root.glob("*.md")):
            loose_match = LOOSE_DATE_NAME_RE.match(path.name)
            if not loose_match:
                continue
            try:
                file_date = date(*(int(part) for part in loose_match.groups()))
            except ValueError:
                self._add(
                    "ERROR",
                    "invalid_daily_date",
                    path,
                    "Daily filename contains an invalid calendar date.",
                )
                continue
            if file_date < cutoff:
                continue

            if ISO_DATE_NAME_RE.match(path.name) is None:
                self._add(
                    "ERROR",
                    "non_iso_daily_filename",
                    path,
                    "Daily filename must use zero-padded YYYY-MM-DD.md.",
                )

            document = self._document(path)
            frontmatter = self._frontmatter(path)
            daily_type = frontmatter.get("type")
            is_legacy_cutover_file = (
                file_date == cutoff
                and frontmatter.get("status") == "superseded"
                and daily_type != "每日总结"
            )
            if document.has_frontmatter and not is_legacy_cutover_file:
                self._require_fields(path, frontmatter, ("date", "type"))
                if daily_type not in (None, "每日总结"):
                    self._add(
                        "ERROR",
                        "daily_type_mismatch",
                        path,
                        "Post-cutover dated files in 00_Daily must use type: 每日总结.",
                    )
                frontmatter_date = parse_iso_date(str(frontmatter.get("date", "")))
                if frontmatter_date is not None and frontmatter_date != file_date:
                    self._add(
                        "ERROR",
                        "daily_date_mismatch",
                        path,
                        "Frontmatter date does not match the Daily filename.",
                    )

            for line_number, line in iter_non_fenced_lines(document.text):
                if TASK_RE.match(line):
                    self._add(
                        "ERROR",
                        "daily_checkbox",
                        path,
                        "Post-cutover Daily files may reference tasks but may not copy checkboxes.",
                        line_number,
                    )

    def _check_coordination(self) -> None:
        expected = {
            "requests": ("agent_request", {"pending", "claimed", "completed", "blocked", "cancelled"}),
            "proposals": ("agent_proposal", {"pending", "approved", "applied", "rejected", "expired"}),
            "handoffs": ("agent_handoff", {"active", "resolved"}),
            "reports": ("agent_report", {"generated", "superseded", "archived"}),
        }
        root = self._absolute(COORDINATION_ROOT)
        for directory, (expected_type, allowed_statuses) in expected.items():
            folder = root / directory
            readme = folder / "README.md"
            if not readme.is_file():
                self._add(
                    "ERROR",
                    "missing_coordination_readme",
                    readme,
                    "Coordination subdirectory must contain README.md.",
                )
                continue
            for path in sorted(folder.glob("*.md")):
                if path.name == "README.md":
                    continue
                document = self._document(path)
                frontmatter = self._frontmatter(path)
                self._require_fields(
                    path,
                    frontmatter,
                    (
                        "type",
                        "id",
                        "created_at",
                        "created_by",
                        "status",
                        "authority_files",
                        "allowed_writes",
                    ),
                )
                if frontmatter.get("type") != expected_type:
                    self._add(
                        "ERROR",
                        "coordination_type_mismatch",
                        path,
                        f"Files in {directory}/ must use type: {expected_type}.",
                    )
                if frontmatter.get("status") not in allowed_statuses:
                    self._add(
                        "ERROR",
                        "coordination_status",
                        path,
                        f"Invalid status for {directory}/: {frontmatter.get('status')!r}.",
                    )
                if directory == "proposals":
                    self._require_fields(
                        path,
                        frontmatter,
                        ("requires_approval", "target_files", "evidence_files", "summary", "reason"),
                    )
                    if frontmatter.get("status") in {"approved", "applied"}:
                        self._require_fields(
                            path, frontmatter, ("approved_by", "approved_at")
                        )
                    if frontmatter.get("status") == "applied":
                        self._require_fields(
                            path, frontmatter, ("applied_at", "verification")
                        )
                elif directory == "handoffs" and not HANDOFF_NAME_RE.match(path.name):
                    self._add(
                        "ERROR",
                        "handoff_filename",
                        path,
                        "Handoff filename must be YYYY-MM-DD-HHmm-主题.md.",
                    )
                elif directory == "reports":
                    self._require_fields(
                        path, frontmatter, ("generated_by", "generated_at")
                    )

                for line_number, line in iter_non_fenced_lines(document.text):
                    if TASK_RE.match(line):
                        self._add(
                            "ERROR",
                            "coordination_checkbox",
                            path,
                            "Coordination files may not contain task checkboxes.",
                            line_number,
                        )

    def _check_rules(self) -> None:
        candidate_dirs = [self._absolute(RULES_ROOT / "candidates")]
        domains_root = self._absolute(PROJECT_ROOT / "domains")
        if domains_root.is_dir():
            candidate_dirs.extend(
                sorted(domains_root.glob("*/modules/*/candidates"))
            )

        required = (
            "source_id",
            "subject",
            "stage",
            "claim",
            "trigger",
            "action",
            "stop_condition",
            "source_file",
            "evidence_status",
            "status",
        )
        seen: set[Path] = set()
        for candidates in candidate_dirs:
            if not candidates.is_dir():
                continue
            for path in sorted(candidates.glob("*.md")):
                if path.name == "README.md" or path in seen:
                    continue
                seen.add(path)
                frontmatter = self._frontmatter(path)
                self._require_fields(path, frontmatter, required)
                if frontmatter.get("status") != "candidate":
                    self._add(
                        "ERROR",
                        "candidate_rule_status",
                        path,
                        "Candidate rule must use status: candidate.",
                    )
                if frontmatter.get("evidence_status") != "ai_synthesis":
                    self._add(
                        "ERROR",
                        "candidate_evidence_status",
                        path,
                        "Candidate rule must use evidence_status: ai_synthesis.",
                    )
                source_file = frontmatter.get("source_file")
                if source_file:
                    source_path = self._absolute(str(source_file))
                    if not source_path.is_file():
                        self._add(
                            "ERROR",
                            "missing_rule_source",
                            path,
                            f"Referenced source_file does not exist: {source_file}",
                        )

        active = self._absolute(RULES_ROOT / "active")
        if active.is_dir():
            for path in sorted(active.glob("*.md")):
                if path.name == "README.md":
                    continue
                frontmatter = self._frontmatter(path)
                self._require_fields(
                    path,
                    frontmatter,
                    ("source_id", "subject", "status", "approved_by", "approved_at"),
                )
                if frontmatter.get("status") != "active":
                    self._add(
                        "ERROR",
                        "active_rule_status",
                        path,
                        "Files in rules/active must use status: active.",
                    )
                if frontmatter.get("approved_by") != "user":
                    self._add(
                        "ERROR",
                        "active_rule_approval",
                        path,
                        "Active rule must be approved_by: user.",
                    )

    def _check_route(self, formal_weeks: set[str]) -> None:
        if not formal_weeks:
            return
        path = self._absolute(ROUTE_PATH)
        if not path.is_file():
            return
        frontmatter = self._frontmatter(path)
        if frontmatter.get("status") == "draft" or frontmatter.get(
            "approval_status"
        ) == "pending":
            self._add(
                "WARN",
                "route_pending_with_formal_plan",
                path,
                "A formal weekly plan exists while the stage route is still draft or pending approval.",
            )


def parse_frontmatter(text: str) -> tuple[dict[str, Any], bool, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False, []
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, True, ["YAML frontmatter has no closing --- delimiter."]

    values: dict[str, Any] = {}
    problems: list[str] = []
    current_key: str | None = None
    for line_number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            stripped = line.strip()
            if current_key is not None and stripped.startswith("- "):
                if values[current_key] is None:
                    values[current_key] = []
                if not isinstance(values[current_key], list):
                    problems.append(
                        f"Line {line_number}: sequence item follows a scalar value."
                    )
                    continue
                values[current_key].append(parse_scalar(stripped[2:]))
            continue
        match = FRONTMATTER_KEY_RE.match(line)
        if not match:
            problems.append(f"Line {line_number}: unsupported top-level YAML syntax.")
            current_key = None
            continue
        key, raw_value = match.groups()
        if key in values:
            problems.append(f"Line {line_number}: duplicate frontmatter key: {key}")
            current_key = None
            continue
        values[key] = parse_scalar(raw_value or "")
        current_key = key
    return values, True, problems


def parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def parse_iso_date(value: str) -> date | None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def to_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def iter_non_fenced_lines(text: str) -> Iterable[tuple[int, str]]:
    in_fence = False
    fence_marker = ""
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if not in_fence:
            yield line_number, line


def should_skip_path(path: Path, vault_root: Path) -> bool:
    try:
        parts = path.relative_to(vault_root).parts
    except ValueError:
        return True
    return any(part in {".git", ".obsidian", "node_modules"} for part in parts)


def issue_sort_key(issue: Issue) -> tuple[int, str, int, str]:
    severity_order = 0 if issue.severity == "ERROR" else 1
    return severity_order, issue.path, issue.line or 0, issue.code


def find_vault_root(explicit_root: str | None) -> Path:
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
        if is_vault_root(root):
            return root
        raise ValueError(f"Not a planning-system Vault root: {root}")

    for variable in ("VAULT_ROOT", "MY_LIB_HOME"):
        value = os.environ.get(variable)
        if value:
            root = Path(value).expanduser().resolve()
            if is_vault_root(root):
                return root

    starts = [Path.cwd().resolve(), Path(__file__).resolve().parent]
    visited: set[Path] = set()
    for start in starts:
        for candidate in (start, *start.parents):
            if candidate in visited:
                continue
            visited.add(candidate)
            if is_vault_root(candidate):
                return candidate
    raise ValueError("Unable to locate Vault root; use --vault-root or VAULT_ROOT.")


def is_vault_root(path: Path) -> bool:
    return (
        (path / "AGENTS.md").is_file()
        and (path / PROJECT_ROOT / "SPEC.md").is_file()
        and (path / PLAN_ROOT).is_dir()
    )


def print_text_report(report: VerificationReport) -> None:
    print("=" * 72)
    print("POSTGRADUATE-EXAM PLANNING SYSTEM VERIFICATION")
    print("=" * 72)
    print(f"Vault: {report.vault_root}")
    print(
        f"Status: {report.status} | Errors: {len(report.errors)} | "
        f"Warnings: {len(report.warnings)}"
    )
    for issue in sorted(report.issues, key=issue_sort_key):
        location = issue.path
        if issue.line is not None:
            location += f":{issue.line}"
        print(f"[{issue.severity}] {issue.code} | {location}")
        print(f"        {issue.message}")


def write_fixture(root: Path, relative: Path | str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_valid_fixture(root: Path) -> None:
    write_fixture(root, "AGENTS.md", "# Test Vault")
    for name, content in {
        "PROJECT.md": """
---
type: 项目总览
version: 1.0
status: active
updated: 2026-08-23
---
# Project
""",
        "SPEC.md": """
---
type: 系统规范
version: 1.0
status: active
updated: 2026-08-23
---
# Spec
""",
        "HANDOFF.md": """
---
type: Agent交接指南
status: active
updated: 2026-08-23
---
# Handoff
""",
    }.items():
        write_fixture(root, PROJECT_ROOT / name, content)

    write_fixture(
        root,
        BOARD_PATH,
        """
---
kanban-plugin: board
type: 考研任务看板
canonical_since: 2026-08-19
---
## 今日（最多3项）
- [ ] 【数学一｜P0｜8/23】完成测试；验收：记录结果 ^w34-math-test

## 进行中（最多1项）

## 本周队列

## 完成
- [x] 【系统｜P0｜8/22】确认计划；验收：正式版存在 ^w34-confirm-test

## 取消/改期
""",
    )
    write_fixture(
        root,
        ROUTE_PATH,
        """
---
type: 阶段路线图
status: active
approval_status: approved
current_stage: S1
---
# Route
""",
    )
    write_fixture(
        root,
        WEEKLY_ROOT / "2026-W34-草案.md",
        """
---
type: 周计划
week: 2026-W34
status: superseded
generated_by: test
generated_at: 2026-08-20
date_start: 2026-08-17
date_end: 2026-08-23
capacity_hours: 10
committed_hours: 8
buffer_hours: 2
stage: S1
---
# Draft
""",
    )
    write_fixture(
        root,
        WEEKLY_ROOT / "2026-W34-正式.md",
        """
---
type: 周计划
week: 2026-W34
status: formal
generated_by: test
generated_at: 2026-08-20
confirmed_by: user
confirmed_at: 2026-08-20T10:00:00Z
date_start: 2026-08-17
date_end: 2026-08-23
capacity_hours: 10
committed_hours: 8
buffer_hours: 2
stage: S1
---
# Formal
""",
    )
    write_fixture(
        root,
        DAILY_ROOT / "2026-08-23.md",
        """
---
date: 2026-08-23
type: 每日总结
study_minutes: 60
---
# Daily

- 已完成任务：w34-math-test
""",
    )
    for directory in ("requests", "proposals", "handoffs", "reports"):
        write_fixture(
            root,
            COORDINATION_ROOT / directory / "README.md",
            """
---
type: Agent协作目录说明
status: active
updated: 2026-08-23
---
# README
""",
        )
    write_fixture(
        root,
        COORDINATION_ROOT / "README.md",
        """
---
type: Agent协作协议
status: active
updated: 2026-08-23
---
# Coordination
""",
    )
    write_fixture(root, RULES_ROOT / "candidates" / "README.md", "# Candidates")
    write_fixture(root, RULES_ROOT / "active" / "README.md", "# Active")


def run_self_tests() -> bool:
    scenarios: list[tuple[str, str | None]] = [
        ("valid fixture", None),
        ("duplicate block id", "duplicate_block_id"),
        ("non-ISO Daily filename", "non_iso_daily_filename"),
        ("unconfirmed formal plan", "missing_required_field"),
    ]
    all_passed = True
    print("Running planning-system verifier self-tests:")
    for name, expected_code in scenarios:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            build_valid_fixture(root)
            if name == "duplicate block id":
                board = root / BOARD_PATH
                board.write_text(
                    board.read_text(encoding="utf-8").replace(
                        "## 进行中（最多1项）",
                        "## 进行中（最多1项）\n"
                        "- [ ] 【数学一｜P0｜8/23】重复；验收：记录结果 "
                        "^w34-math-test\n",
                    ),
                    encoding="utf-8",
                )
            elif name == "non-ISO Daily filename":
                source = root / DAILY_ROOT / "2026-08-23.md"
                source.rename(root / DAILY_ROOT / "2026-8-23.md")
            elif name == "unconfirmed formal plan":
                formal = root / WEEKLY_ROOT / "2026-W34-正式.md"
                formal.write_text(
                    formal.read_text(encoding="utf-8").replace(
                        "confirmed_at: 2026-08-20T10:00:00Z\n", ""
                    ),
                    encoding="utf-8",
                )

            report = PlanningSystemVerifier(root).verify()
            codes = {issue.code for issue in report.errors}
            passed = report.status == "PASS" if expected_code is None else expected_code in codes
            marker = "OK" if passed else "FAIL"
            print(f"  [{marker}] {name}: status={report.status}, errors={len(report.errors)}")
            if not passed:
                print(f"         expected={expected_code!r}, codes={sorted(codes)}")
                all_passed = False
    return all_passed


def configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    configure_utf8_output()
    parser = argparse.ArgumentParser(
        description="Read-only integrity verifier for the planning system."
    )
    parser.add_argument(
        "--vault-root",
        help="Vault root; otherwise VAULT_ROOT, MY_LIB_HOME, cwd and script parents are checked.",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Return a failure exit code when warnings are present.",
    )
    parser.add_argument(
        "--mock", action="store_true", help="Run deterministic self-tests in temporary Vaults."
    )
    args = parser.parse_args()

    if args.mock:
        return 0 if run_self_tests() else 1

    try:
        vault_root = find_vault_root(args.vault_root)
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    report = PlanningSystemVerifier(vault_root).verify()
    if args.json:
        print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
    else:
        print_text_report(report)

    if report.errors or (args.strict_warnings and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

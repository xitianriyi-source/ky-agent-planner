"""Deterministic Phase 4 checks for the MMG mathematics Skill draft.

The Skill is a Markdown behavior contract rather than executable code, so these
checks verify its explicit claims, source traceability, and write boundaries.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MODULE_ROOT = Path(
    "02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math"
)
SKILL_PATH = MODULE_ROOT / "skill/SKILL.md"
SYNTHESIS_PATH = MODULE_ROOT / "synthesis/phase-2-math-methodology.md"
MANIFEST_PATH = MODULE_ROOT / "sources/source-manifest.md"
REGISTRY_PATH = MODULE_ROOT / "sources/source-registry.md"
CANDIDATE_DIR = MODULE_ROOT / "candidates"


class Phase4Failure(AssertionError):
    """A named Phase 4 contract failure."""


def find_vault_root(start: Path) -> Path:
    """Resolve the Vault root without depending on the current directory."""
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (
            candidate / "02_项目/考研Agent规划系统/SPEC.md"
        ).is_file():
            return candidate
    raise Phase4Failure("Could not find Vault root from the current directory.")


def read_text(root: Path, relative: Path) -> str:
    path = root / relative
    if not path.is_file():
        raise Phase4Failure(f"Missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise Phase4Failure("Skill draft must start with YAML frontmatter.")
    end = text.find("\n---", 4)
    if end < 0:
        raise Phase4Failure("Skill draft frontmatter is not closed.")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def require(text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        raise Phase4Failure(f"{label}: missing {phrase!r}")


def require_any(text: str, phrases: tuple[str, ...], label: str) -> None:
    if not any(phrase in text for phrase in phrases):
        joined = " / ".join(repr(phrase) for phrase in phrases)
        raise Phase4Failure(f"{label}: none of {joined} found")


def manifest_source_ids(manifest: str) -> set[str]:
    return set(re.findall(r"\|\s*(mmg-src-\d+)\s*\|", manifest))


def candidate_source_ids(root: Path) -> set[str]:
    source_ids: set[str] = set()
    for path in sorted((root / CANDIDATE_DIR).glob("candidate_mmg_*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^source_id:\s*(mmg-src-\d+)\s*$", text, re.MULTILINE)
        if not match:
            raise Phase4Failure(f"Candidate has no source_id: {path}")
        source_ids.add(match.group(1))
    return source_ids


def check_metadata(root: Path, skill: str, synthesis: str) -> None:
    frontmatter = parse_frontmatter(skill)
    expected = {
        "name": "mmg-math-methodology",
        "version": "0.1.0-draft",
        "status": "phase_4_passed_pending_evidence",
        "phase": "4",
        "scope": "考研数学方法论",
        "evidence_status": "ai_synthesis",
        "production_ready": "false",
    }
    for key, value in expected.items():
        if frontmatter.get(key) != value:
            raise Phase4Failure(
                f"metadata: {key} must be {value!r}, got {frontmatter.get(key)!r}"
            )
    require(synthesis, "status: approved_for_phase_3", "metadata")
    require(synthesis, "五个心智模型保持独立", "metadata")


def check_model_independence(skill: str) -> None:
    headings = re.findall(r"^### (M[1-5])：", skill, re.MULTILINE)
    if headings != ["M1", "M2", "M3", "M4", "M5"]:
        raise Phase4Failure(f"models: expected M1..M5 once, got {headings}")
    require(skill, "不会吞并其他四个模型", "models")
    require(skill, "五个独立心智模型", "models")


def check_source_traceability(root: Path, skill: str, registry: str) -> None:
    manifest = read_text(root, MANIFEST_PATH)
    manifest_ids = manifest_source_ids(manifest)
    if manifest_ids != {f"mmg-src-{index:02d}" for index in range(1, 19)}:
        raise Phase4Failure("sources: manifest must contain mmg-src-01 through mmg-src-18")
    if candidate_source_ids(root) != {
        "mmg-src-02",
        "mmg-src-12",
        "mmg-src-14",
        "mmg-src-15",
        "mmg-src-16",
        "mmg-src-18",
    }:
        raise Phase4Failure("sources: candidate source_id set changed unexpectedly")
    skill_ids = set(re.findall(r"`(mmg-src-\d+)`", skill))
    if not skill_ids <= manifest_ids:
        raise Phase4Failure(f"sources: Skill references unknown ids {skill_ids - manifest_ids}")
    require(registry, "source_count: 18", "sources")
    require(registry, "evidence_status: ai_synthesis", "sources")
    require(skill, "source_ids: [mmg-src-xx]", "sources")
    require(skill, "source_id", "sources")


def check_known_positions(skill: str) -> None:
    # The following assertions are Phase 4 fidelity probes for known positions.
    require(skill, "基础阶段默认不建议观看 UP 主专题/技巧视频", "P1 basic-stage video boundary")
    require(skill, "强化阶段或强化结束后，才允许在已定位的薄弱点上按需使用专题材料", "P1 targeted video timing")
    require(skill, "基础阶段不强行做 A4", "P2 A4 boundary")
    require(skill, "先用小规模跨章节题组", "P3 mixed-practice scaling")
    require(skill, "讲义/真题基础证明题不能跳过", "P4 proof boundary")
    require(skill, "限时套卷统一批改", "P5 timed feedback boundary")
    require(skill, "没有个人证据时不改正式路线", "P6 past-paper route boundary")
    require(skill, "不以时长替代结果证据", "P7 output-over-duration boundary")


def check_conflict_handling(skill: str) -> None:
    conflict_headings = (
        "真题提前进入 vs 信息增量有限",
        "完整掌握 vs 选择性舍弃",
        "严格主线 vs 反馈修正",
        "A4 整理 vs 题目输出",
    )
    for heading in conflict_headings:
        require(skill, heading, f"conflicts: {heading}")
    require(skill, "不输出“越早越好”或“绝对不要提前”", "conflicts")
    require(skill, "不强行合并为绝对规则", "conflicts")
    require(skill, "调整建议必须交由用户决定", "conflicts")


def check_output_and_permissions(skill: str) -> None:
    for phrase in (
        "authority: non_authoritative",
        "approval_needed: true",
        "writes_allowed: []",
        "不创建或修改",
        "不写入 `02_项目/考研Agent规划系统/rules/active/`",
        "不把一次成功观察写成个人规律",
        "不删除原始 transcript",
        "不执行 Git commit、push、pull",
    ):
        require(skill, phrase, f"permissions: {phrase}")
    require(skill, "Phase 4 已知立场、边界和冲突测试", "release gate")
    require(skill, "不得安装为生产 Skill", "release gate")


def run(root: Path) -> None:
    skill = read_text(root, SKILL_PATH)
    synthesis = read_text(root, SYNTHESIS_PATH)
    registry = read_text(root, REGISTRY_PATH)
    check_metadata(root, skill, synthesis)
    check_model_independence(skill)
    check_source_traceability(root, skill, registry)
    check_known_positions(skill)
    check_conflict_handling(skill)
    check_output_and_permissions(skill)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-root", type=Path, help="Vault root; auto-detected by default")
    args = parser.parse_args()
    try:
        root = (args.vault_root or find_vault_root(Path.cwd())).resolve()
        run(root)
    except (Phase4Failure, OSError) as error:
        print(f"Phase 4: FAIL: {error}")
        return 1
    print("Phase 4: PASS | metadata, fidelity, conflicts, permissions, release gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())

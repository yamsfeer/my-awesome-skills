#!/usr/bin/env python3
"""
iteration-2 评分脚本
检验 design-flow skill 三个新功能：
1. state-machine-visual.md（Mermaid 可视化）
2. state-machine-interactive.html（可交互 HTML 查看器）
3. references/validate.py（数据契约校验）
"""
import json, os, re
from pathlib import Path

WORKSPACE = Path(__file__).parent
ITER1 = WORKSPACE.parent / "iteration-1"


def check(condition: bool, name: str, evidence: str) -> dict:
    return {"text": name, "passed": condition, "evidence": evidence}


# ──────────────── eval-0: FitStreak ────────────────

def grade_eval0(config: str) -> list:
    base = WORKSPACE / "eval-0-fitstreak" / config / "outputs" / "fitstreak"
    results = []

    # files_created
    files_ok = all((base / f).exists() for f in [
        "product-overview.md",
        "contracts/domain.yaml",
        "design/tokens.json"
    ])
    results.append(check(files_ok, "核心文件是否创建",
        f"检查 product-overview.md, contracts/domain.yaml, design/tokens.json，存在={files_ok}"))

    # domain_sensitive_markers
    domain = base / "contracts/domain.yaml"
    if domain.exists():
        content = domain.read_text(encoding="utf-8")
        has_marker = "禁止暴露" in content
        results.append(check(has_marker, "敏感字段是否标注", f"domain.yaml 含'禁止暴露'={has_marker}"))
    else:
        results.append(check(False, "敏感字段是否标注", "domain.yaml 不存在"))

    # tokens_frozen
    tokens = base / "design/tokens.json"
    if tokens.exists():
        content = tokens.read_text(encoding="utf-8")
        frozen = "_frozen" in content
        results.append(check(frozen, "Design Token 是否冻结", f"tokens.json 含'_frozen'={frozen}"))
    else:
        results.append(check(False, "Design Token 是否冻结", "tokens.json 不存在"))

    # wireframes_created
    wf_dir = base / "wireframes"
    wf_files = list(wf_dir.glob("*.md")) if wf_dir.exists() else []
    wf_has_art = False
    if wf_files:
        sample = wf_files[0].read_text(encoding="utf-8")
        wf_has_art = "┌" in sample or "│" in sample
    results.append(check(bool(wf_files) and wf_has_art, "线框图是否创建",
        f"wireframes/*.md 数量={len(wf_files)}, 含 ASCII 框={wf_has_art}"))

    # state_machine_created
    sm = base / "ue/state-machine.yaml"
    if sm.exists():
        content = sm.read_text(encoding="utf-8")
        has_states = "states" in content
        results.append(check(has_states, "状态机是否创建", f"state-machine.yaml 含'states'={has_states}"))
    else:
        results.append(check(False, "状态机是否创建", "state-machine.yaml 不存在"))

    # visual_state_machine (NEW)
    visual = base / "ue/state-machine-visual.md"
    if visual.exists():
        content = visual.read_text(encoding="utf-8")
        has_mermaid = "stateDiagram" in content or "mermaid" in content
        results.append(check(has_mermaid, "可视化状态机是否生成",
            f"state-machine-visual.md 存在={True}, 含 stateDiagram={has_mermaid}"))
    else:
        results.append(check(False, "可视化状态机是否生成", "state-machine-visual.md 不存在"))

    # interactive_html (NEW)
    html = base / "ue/state-machine-interactive.html"
    if html.exists():
        content = html.read_text(encoding="utf-8")
        has_mermaid_cdn = "mermaid" in content.lower()
        has_states_obj = "const STATES" in content or "STATES =" in content or "var STATES" in content
        ok = has_mermaid_cdn and has_states_obj
        results.append(check(ok, "可交互 HTML 查看器是否生成",
            f"HTML 存在={True}, mermaid CDN={has_mermaid_cdn}, STATES 对象={has_states_obj}"))
    else:
        results.append(check(False, "可交互 HTML 查看器是否生成", "state-machine-interactive.html 不存在"))

    return results


# ──────────────── eval-1: Shiwo ────────────────

def grade_eval1(config: str) -> list:
    base = WORKSPACE / "eval-1-shiwo" / config / "outputs" / "shiwo-marketplace"
    results = []

    files_ok = (base / "product-overview.md").exists() and (base / "contracts").is_dir()
    results.append(check(files_ok, "核心文件是否创建", f"product-overview.md 和 contracts/ 存在={files_ok}"))

    api = base / "contracts/api.yaml"
    if api.exists():
        content = api.read_text(encoding="utf-8")
        ep_count = content.count("method:") + content.count("- method:")
        # deduplicate count
        ep_count = len(re.findall(r"method:\s*(GET|POST|PUT|DELETE|PATCH)", content))
        ok = ep_count >= 5
        results.append(check(ok, "API 契约端点数量 ≥ 5", f"检测到端点数={ep_count}"))
    else:
        results.append(check(False, "API 契约端点数量 ≥ 5", "api.yaml 不存在"))

    domain = base / "contracts/domain.yaml"
    if domain.exists():
        has_marker = "禁止暴露" in domain.read_text(encoding="utf-8")
        results.append(check(has_marker, "敏感字段是否标注", f"含'禁止暴露'={has_marker}"))
    else:
        results.append(check(False, "敏感字段是否标注", "domain.yaml 不存在"))

    tokens = base / "design/tokens.json"
    if tokens.exists():
        frozen = "_frozen" in tokens.read_text(encoding="utf-8")
        results.append(check(frozen, "Design Token 是否冻结", f"含'_frozen'={frozen}"))
    else:
        results.append(check(False, "Design Token 是否冻结", "tokens.json 不存在"))

    # interactive_html (NEW)
    html = base / "ue/state-machine-interactive.html"
    if html.exists():
        content = html.read_text(encoding="utf-8")
        has_states = "STATES" in content
        results.append(check(has_states, "可交互 HTML 是否生成", f"HTML 存在，STATES 对象={has_states}"))
    else:
        results.append(check(False, "可交互 HTML 是否生成", "state-machine-interactive.html 不存在"))

    return results


# ──────────────── eval-2: FreelanceBook ────────────────

def grade_eval2(config: str) -> list:
    base = WORKSPACE / "eval-2-freelancebook" / config / "outputs" / "freelancebook"
    results = []

    files_ok = all((base / f).exists() for f in [
        "product-overview.md", "contracts/domain.yaml", "design/tokens.json"])
    results.append(check(files_ok, "核心文件是否创建", f"三个核心文件存在={files_ok}"))

    domain = base / "contracts/domain.yaml"
    if domain.exists():
        content = domain.read_text(encoding="utf-8")
        # 查找含 amount/price/fee 的字段类型定义
        type_matches = re.findall(r"(amount|price|fee|total|subtotal).*?\n.*?type:\s*(\w+)", content, re.IGNORECASE)
        bad_types = [t for _, t in type_matches if t.lower() in ("float", "double", "real")]
        ok = len(bad_types) == 0
        results.append(check(ok, "金额字段是否用精确类型",
            f"检测到 float/double 金额类型={bad_types if bad_types else '无'}"))
        has_marker = "禁止暴露" in content
        results.append(check(has_marker, "敏感字段是否标注", f"含'禁止暴露'={has_marker}"))
    else:
        results.append(check(False, "金额字段是否用精确类型", "domain.yaml 不存在"))
        results.append(check(False, "敏感字段是否标注", "domain.yaml 不存在"))

    roadmap = base / "product-roadmap.md"
    if roadmap.exists():
        content = roadmap.read_text(encoding="utf-8")
        version_count = len(re.findall(r"v\d+\.\d+|版本\s*\d+|Phase\s*\d+|阶段\s*\d+|MVP", content, re.IGNORECASE))
        ok = version_count >= 2
        results.append(check(ok, "路线图是否有版本分层", f"版本关键词出现次数={version_count}"))
    else:
        results.append(check(False, "路线图是否有版本分层", "product-roadmap.md 不存在"))

    # visual_state_machine (NEW)
    visual = base / "ue/state-machine-visual.md"
    if visual.exists():
        content = visual.read_text(encoding="utf-8")
        has_mermaid = "mermaid" in content.lower() or "stateDiagram" in content
        results.append(check(has_mermaid, "可视化状态机是否生成",
            f"visual.md 存在，含 mermaid={has_mermaid}"))
    else:
        results.append(check(False, "可视化状态机是否生成", "state-machine-visual.md 不存在"))

    return results


# ──────────────── eval-3: Validator ────────────────

def grade_eval3(config: str) -> list:
    report_path = WORKSPACE / "eval-3-validate" / config / "outputs" / "validation_report.md"
    results = []

    if not report_path.exists():
        results.append(check(False, "校验脚本是否成功运行", "validation_report.md 不存在"))
        results.append(check(False, "是否检测到敏感字段泄露 (A03)", "报告不存在"))
        results.append(check(False, "是否检测到响应类型错误 (A01)", "报告不存在"))
        results.append(check(False, "是否检测到 UI 端点错误 (U01)", "报告不存在"))
        return results

    content = report_path.read_text(encoding="utf-8")
    has_crash = "Traceback" in content or "Error:" in content[:200]
    results.append(check(not has_crash, "校验脚本是否成功运行",
        f"报告存在，含 Traceback={has_crash}"))

    has_a03 = ("A03" in content or "password_hash" in content) and (
        "敏感" in content or "暴露" in content or "sensitive" in content.lower())
    results.append(check(has_a03, "是否检测到敏感字段泄露 (A03)",
        f"报告含 A03/password_hash + 敏感描述={has_a03}"))

    has_a01 = "A01" in content or "NonExistentType" in content
    results.append(check(has_a01, "是否检测到响应类型错误 (A01)",
        f"报告含 A01/NonExistentType={has_a01}"))

    has_u01 = ("U01" in content or "UserProfilePage" in content or "users/profile" in content)
    results.append(check(has_u01, "是否检测到 UI 端点错误 (U01)",
        f"报告含 U01/UserProfilePage/users/profile={has_u01}"))

    return results


# ──────────────── 主程序 ────────────────

def main():
    runs = [
        (0, "fitstreak-fitness-app", "eval-0-fitstreak", "with_skill", grade_eval0),
        (1, "shiwo-campus-marketplace", "eval-1-shiwo", "with_skill", grade_eval1),
        (2, "freelancebook-finance-tool", "eval-2-freelancebook", "with_skill", grade_eval2),
        (3, "contract-validator", "eval-3-validate", "with_skill", grade_eval3),
        (3, "contract-validator", "eval-3-validate", "without_skill", grade_eval3),
    ]

    all_results = []
    for eval_id, eval_name, dir_name, config, grade_fn in runs:
        assertions = grade_fn(config)
        passed = sum(1 for a in assertions if a["passed"])
        total = len(assertions)
        grading = {"eval_id": eval_id, "config": config, "expectations": assertions}
        outdir = WORKSPACE / dir_name / config
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "grading.json").write_text(
            json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")
        all_results.append({
            "eval_id": eval_id,
            "eval_name": eval_name,
            "config": config,
            "expectations_total": total,
            "expectations_passed": passed,
            "pass_rate": round(passed / total, 2) if total else 0,
        })
        status = "✅" if passed == total else f"⚠️  {passed}/{total}"
        print(f"{status}  eval-{eval_id} ({eval_name}) [{config}]")

    # 汇总
    print("\n── 汇总 ──")
    for config in ["with_skill", "without_skill"]:
        group = [r for r in all_results if r["config"] == config]
        if not group:
            continue
        avg = sum(r["pass_rate"] for r in group) / len(group)
        print(f"  {config}: avg pass_rate = {avg:.2f} ({len(group)} evals)")

    # 写 benchmark.json
    (WORKSPACE / "benchmark_raw.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n结果已写入 benchmark_raw.json 和各 eval 目录下的 grading.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Grade design-flow eval outputs against assertions."""
import json
import os
import sys
from pathlib import Path
import re

GRADING_SCHEMA = {"text": str, "passed": bool, "evidence": str}

def check_file_exists(base_path, files):
    """Check if at least one file exists."""
    for f in files:
        if (Path(base_path) / f).exists():
            return True
    return False

def grade_eval(eval_dir, eval_id, eval_name, assertions):
    """Grade a single eval run."""
    results = {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "run_dir": str(eval_dir),
        "expectations": []
    }

    # Find project directory (contains product-overview.md)
    outputs_dir = Path(eval_dir) / "outputs"
    project_dirs = []
    for subdir in outputs_dir.iterdir():
        if subdir.is_dir() and (subdir / "product-overview.md").exists():
            project_dirs.append(subdir)

    if not project_dirs:
        return {"error": "No project directory found"}

    project_dir = project_dirs[0]
    slug = project_dir.name

    for assertion in assertions:
        aid = assertion["id"]
        name = assertion["name"]
        desc = assertion["description"]

        passed = False
        evidence = ""

        if aid == "files_created":
            # Check core files
            required = ["product-overview.md", "contracts/domain.yaml", "design/tokens.json"]
            found = [f for f in required if (project_dir / f).exists()]
            passed = len(found) >= 3
            evidence = f"Found {len(found)}/{len(required)} core files: {found}"

        elif aid == "domain_sensitive_markers":
            # Check domain.yaml for sensitive field markers
            domain_file = project_dir / "contracts" / "domain.yaml"
            if domain_file.exists():
                content = domain_file.read_text()
                has_marker = "⚠️ 禁止暴露" in content or "禁止暴露" in content
                passed = has_marker
                evidence = f"Contains '禁止暴露' marker: {has_marker}"
            else:
                passed = False
                evidence = "domain.yaml not found"

        elif aid == "tokens_frozen":
            # Check tokens.json for _frozen field
            tokens_file = project_dir / "design" / "tokens.json"
            if tokens_file.exists():
                content = tokens_file.read_text()
                has_frozen = '"_frozen"' in content and '"_frozen": true' in content
                passed = has_frozen
                evidence = f"Contains _frozen: true: {has_frozen}"
            else:
                passed = False
                evidence = "tokens.json not found"

        elif aid == "wireframes_created":
            # Check wireframes directory
            wireframes_dir = project_dir / "wireframes"
            if wireframes_dir.exists():
                md_files = list(wireframes_dir.glob("*.md"))
                has_ascii = False
                for f in md_files:
                    content = f.read_text()
                    if "┌" in content or "│" in content:  # ASCII art
                        has_ascii = True
                        break

                # Check for constraint markers
                has_markers = False
                for f in md_files:
                    content = f.read_text()
                    if "🔴" in content or "🔵" in content or "🟢" in content:
                        has_markers = True
                        break

                passed = len(md_files) >= 1 and has_ascii
                evidence = f"Found {len(md_files)} wireframes, ASCII art: {has_ascii}, constraint markers: {has_markers}"
            else:
                passed = False
                evidence = "wireframes/ directory not found"

        elif aid == "state_machine_created":
            # Check state machine file
            sm_file = project_dir / "ue" / "state-machine.yaml"
            if sm_file.exists():
                content = sm_file.read_text()
                has_states = "states:" in content
                passed = has_states
                evidence = f"Contains 'states:': {has_states}"
            else:
                passed = False
                evidence = "state-machine.yaml not found"

        elif aid == "api_endpoints":
            # Check api.yaml for endpoints
            api_file = project_dir / "contracts" / "api.yaml"
            if api_file.exists():
                content = api_file.read_text()
                # Count endpoint markers (GET / POST / PUT / DELETE)
                endpoint_count = len(re.findall(r'^\s*-\s*(GET|POST|PUT|DELETE|PATCH)\s+/', content, re.MULTILINE))
                # Also check for endpoints: section
                endpoints_section = "endpoints:" in content.lower()
                passed = endpoint_count >= 5 or endpoints_section
                evidence = f"Endpoints found: {endpoint_count}, endpoints section: {endpoints_section}"
            else:
                passed = False
                evidence = "api.yaml not found"

        elif aid == "amount_integer_type":
            # Check domain.yaml for amount fields as integer
            domain_file = project_dir / "contracts" / "domain.yaml"
            if domain_file.exists():
                content = domain_file.read_text()
                # Look for amount/price fields with integer type
                has_amount = "amount" in content.lower() or "price" in content.lower()
                has_integer = "integer" in content.lower() or "int" in content.lower()
                # Check it doesn't use float/decimal
                no_float = "float" not in content.lower() and "decimal" not in content.lower()
                passed = has_amount and has_integer and no_float
                evidence = f"Has amount/price: {has_amount}, integer type: {has_integer}, no float/decimal: {no_float}"
            else:
                passed = False
                evidence = "domain.yaml not found"

        elif aid == "roadmap_versions":
            # Check roadmap has version tiers
            roadmap_file = project_dir / "product-roadmap.md"
            if roadmap_file.exists():
                content = roadmap_file.read_text()
                version_markers = ["v1.0", "v1.5", "v2.0", "v2", "MVP", "成长", "扩张"]
                found = [m for m in version_markers if m in content]
                passed = len(found) >= 2
                evidence = f"Version markers found: {found}"
            else:
                passed = False
                evidence = "product-roadmap.md not found"

        results["expectations"].append({
            "text": f"{name}: {desc}",
            "passed": passed,
            "evidence": evidence
        })

    return results

def main():
    workspace = Path(__file__).parent
    iteration_dir = workspace

    all_results = []

    # Grade each eval
    for eval_dir in iteration_dir.iterdir():
        if not eval_dir.is_dir() or eval_dir.name.startswith("."):
            continue

        # Load metadata
        metadata_file = eval_dir / "eval_metadata.json"
        if not metadata_file.exists():
            print(f"Skipping {eval_dir.name}: no metadata")
            continue

        metadata = json.loads(metadata_file.read_text())
        eval_id = metadata["eval_id"]
        eval_name = metadata["eval_name"]
        assertions = metadata.get("assertions", [])

        # Grade with_skill
        with_skill_dir = eval_dir / "with_skill"
        if with_skill_dir.exists():
            result = grade_eval(with_skill_dir, eval_id, eval_name + "_with_skill", assertions)
            result["config"] = "with_skill"

            # Save grading.json
            grading_file = with_skill_dir / "grading.json"
            grading_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"Graded {eval_name} with_skill: {sum(1 for e in result['expectations'] if e['passed'])}/{len(result['expectations'])} passed")
            all_results.append(result)

        # Grade without_skill
        without_skill_dir = eval_dir / "without_skill"
        if without_skill_dir.exists():
            result = grade_eval(without_skill_dir, eval_id, eval_name + "_without_skill", assertions)
            result["config"] = "without_skill"

            grading_file = without_skill_dir / "grading.json"
            grading_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"Graded {eval_name} without_skill: {sum(1 for e in result['expectations'] if e['passed'])}/{len(result['expectations'])} passed")
            all_results.append(result)

    print(f"\nGrading complete. Results saved to grading.json in each run directory.")

if __name__ == "__main__":
    main()

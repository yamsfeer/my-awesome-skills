#!/usr/bin/env python3
"""
design-flow 数据契约校验器
用法：
  python3 references/validate.py <project-slug>
  python3 references/validate.py <project-slug> --strict
"""
import re, sys, yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Issue:
    level: str   # ERROR | WARN
    layer: str   # parse | domain | api | ui | cross
    code: str
    message: str
    hint: str = ""

    def __str__(self):
        icon = {"ERROR": "❌", "WARN": "⚠️ "}.get(self.level, "•")
        s = f"  {icon} [{self.code}] {self.message}"
        return s + (f"\n     💡 {self.hint}" if self.hint else "")


class ContractValidator:
    def __init__(self, project_dir: Path, strict: bool = False):
        self.project_dir = project_dir
        self.strict = strict
        self.issues: List[Issue] = []
        self.domain: Dict = {}
        self.api: Dict = {}
        self.ui: Dict = {}
        self._sensitive: Set[str] = set()  # "Entity.field"

    def _err(self, layer, code, msg, hint=""):
        self.issues.append(Issue("ERROR", layer, code, msg, hint))

    def _warn(self, layer, code, msg, hint=""):
        self.issues.append(Issue("WARN", layer, code, msg, hint))

    def _load_yaml(self, path: Path) -> Optional[Dict]:
        if not path.exists():
            return None
        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            self._err("parse", "P00", f"无法解析 {path.name}: {e}")
            return None

    def load(self) -> bool:
        c = self.project_dir / "contracts"
        d, a, u = (self._load_yaml(c / n) for n in
                   ["domain.yaml", "api.yaml", "ui-schema.yaml"])
        for name, val in [("contracts/domain.yaml", d),
                          ("contracts/api.yaml", a),
                          ("contracts/ui-schema.yaml", u)]:
            if val is None:
                self._err("parse", "P01", f"文件缺失：{name}",
                          "请先完成 Phase 3，或用 /df-contracts 重新生成")
        if None in (d, a, u):
            return False
        self.domain, self.api, self.ui = d, a, u
        return True

    # ── Domain ──────────────────────────────────────────────────────

    def validate_domain(self):
        entities: Dict = self.domain.get("entities") or {}
        if not entities:
            self._warn("domain", "D00", "domain.yaml 中没有实体定义（entities 为空）")
            return
        all_names = set(entities.keys())
        for ename, entity in entities.items():
            if not isinstance(entity, dict):
                continue
            fields: Dict = entity.get("fields") or {}
            if not fields:
                self._warn("domain", "D01", f"实体 {ename} 没有字段定义")
                continue
            # D02: primary_key
            if not any("primary_key" in str((f or {}).get("constraints", ""))
                       for f in fields.values() if isinstance(f, dict)):
                self._err("domain", "D02", f"实体 {ename} 缺少 primary_key 字段",
                          "在 id 字段的 constraints 中添加 primary_key")
            for fname, fdef in fields.items():
                if not isinstance(fdef, dict):
                    continue
                note = fdef.get("note", "")
                if "禁止暴露" in note or "永远不返回" in note:
                    self._sensitive.add(f"{ename}.{fname}")
                # D04: foreign_key 引用实体存在
                fk = re.search(r"foreign_key\((\w+)\.\w+\)",
                               str(fdef.get("constraints", "")))
                if fk and fk.group(1) not in all_names:
                    self._err("domain", "D04",
                              f"{ename}.{fname} 外键引用了不存在的实体 {fk.group(1)}",
                              f"检查实体名称，或在 entities 中补充 {fk.group(1)}")
                # D05: enum 必须有 values
                if fdef.get("type") == "enum" and not fdef.get("values"):
                    self._warn("domain", "D05",
                               f"{ename}.{fname} 是 enum 但未定义 values",
                               "添加 values: [val1, val2, ...]")
        # D06: sensitive_fields_summary 与字段对齐
        for entry in (self.domain.get("sensitive_fields_summary") or []):
            ef = str(entry).split(" - ")[0].strip().split(".")
            if len(ef) != 2:
                continue
            en, fn = ef
            if en not in entities:
                self._warn("domain", "D06",
                           f"sensitive_fields_summary 中实体 {en} 不存在")
            elif fn not in ((entities[en] or {}).get("fields") or {}):
                self._warn("domain", "D06",
                           f"sensitive_fields_summary 中字段 {en}.{fn} 不存在")

    # ── API ─────────────────────────────────────────────────────────

    def _resp_fields(self) -> Dict[str, Set[str]]:
        return {k: set(v.keys()) for k, v in (self.api.get("responses") or {}).items()
                if isinstance(v, dict)}

    def validate_api(self):
        responses: Dict = self.api.get("responses") or {}
        ep_groups = self.api.get("endpoints") or {}
        all_resp = set(responses.keys())
        if not responses:
            self._warn("api", "A00", "api.yaml responses 为空")
        if not ep_groups:
            self._warn("api", "A00", "api.yaml endpoints 为空")
        # A01: 端点 response 类型存在
        for eps in ep_groups.values():
            if not isinstance(eps, list):
                continue
            for ep in eps:
                if not isinstance(ep, dict):
                    continue
                r = ep.get("response")
                if isinstance(r, str) and r not in all_resp:
                    self._err("api", "A01",
                              f"端点 {ep.get('method','')} {ep.get('path','')} "
                              f"引用了未定义响应类型 {r}",
                              f"在 responses 中补充 {r} 的定义")
        # A02: responses 内嵌套类型引用存在
        basic = {"String","Number","Boolean","Any","Object","Integer","Float","Array"}
        for rname, rdef in responses.items():
            if not isinstance(rdef, dict):
                continue
            for fn, ft in rdef.items():
                if not isinstance(ft, str):
                    continue
                ref = ft.rstrip("[]").strip().split("|")[0].strip()
                if (re.match(r"^[A-Z][a-zA-Z]+$", ref)
                        and ref not in basic and ref not in all_resp):
                    self._warn("api", "A02",
                               f"响应类型 {rname}.{fn} 引用了未定义的类型 {ref}",
                               f"确认 {ref} 是否需在 responses 中定义")
        # A03（跨层）: 敏感字段不得直接出现在 API 响应中
        sens_names = {s.split(".")[1] for s in self._sensitive}
        for rname, rdef in responses.items():
            if not isinstance(rdef, dict):
                continue
            for fn in rdef:
                if fn in sens_names:
                    origins = [s for s in self._sensitive if s.endswith(f".{fn}")]
                    self._err("cross", "A03",
                              f"API 响应 {rname} 直接暴露了敏感字段 {fn}"
                              + (f"（源：{', '.join(origins)}）" if origins else ""),
                              "敏感字段需脱敏后暴露（如 email → email_masked）或移除")

    # ── UI ──────────────────────────────────────────────────────────

    def _ep_set(self) -> Set[tuple]:
        base = self.api.get("base_url", "")
        result: Set[tuple] = set()
        for eps in (self.api.get("endpoints") or {}).values():
            if not isinstance(eps, list):
                continue
            for ep in eps:
                if isinstance(ep, dict):
                    m, p = ep.get("method","").upper(), ep.get("path","")
                    n = re.sub(r"/:[^/]+", "/:p", p)
                    result.update([(m, n), (m, re.sub(r"/:[^/]+","/:p",f"{base}{p}"))])
        return result

    def _parse_ds(self, ds: str):
        parts = ds.strip().split(None, 1)
        return (parts[0].upper(), parts[1].strip()) if len(parts) == 2 else (None, None)

    def _ep_exists(self, method: str, path: str, ep_set: Set[tuple]) -> bool:
        n = re.sub(r"/:[^/]+", "/:p", path)
        return (method, n) in ep_set or any(
            m == method and (n.endswith(p) or p.endswith(n)) for m, p in ep_set)

    def _resp_type_for_ds(self, ds: str) -> Optional[str]:
        method, path = self._parse_ds(ds)
        if not method or not path:
            return None
        base = self.api.get("base_url","")
        pn = re.sub(r"/:[^/]+", "/:p", path)
        for eps in (self.api.get("endpoints") or {}).values():
            if not isinstance(eps, list):
                continue
            for ep in eps:
                if not isinstance(ep, dict):
                    continue
                en = re.sub(r"/:[^/]+", "/:p", f"{base}{ep.get('path','')}")
                if (ep.get("method","").upper() == method
                        and (pn == en or pn.endswith(re.sub(r"/:[^/]+","/:p",ep.get("path",""))))):
                    r = ep.get("response")
                    return r if isinstance(r, str) else None
        return None

    def validate_ui(self):
        pages: Dict = self.ui.get("pages") or {}
        if not pages:
            self._warn("ui", "U00", "ui-schema.yaml pages 为空")
            return
        ep_set = self._ep_set()
        resp_fields = self._resp_fields()
        for pname, pdef in pages.items():
            if not isinstance(pdef, dict):
                continue
            ds_raw = pdef.get("data_source", "")
            # U01: data_source 对应端点存在
            if ds_raw:
                ds1 = re.split(r"[（(]|或", ds_raw)[0].strip()
                m, p = self._parse_ds(ds1)
                if m and p and not self._ep_exists(m, p, ep_set):
                    self._warn("ui", "U01",
                               f"页面 {pname} data_source '{ds1}' 在 api.yaml 中无对应端点",
                               "检查路径拼写或在 api.yaml 中补充该端点")
            # U02: 建议有 loading / error 状态
            st_keys = [s.lower() for s in (pdef.get("states") or {})]
            if st_keys:
                if not any("loading" in s for s in st_keys):
                    self._warn("ui","U02",f"页面 {pname} 缺少 loading 状态",
                               "建议添加处理数据加载中的 UI")
                if not any("error" in s for s in st_keys):
                    self._warn("ui","U02",f"页面 {pname} 缺少 error 状态",
                               "建议添加处理接口异常的 UI")
            # U03: 组件字段 source 可追溯到 API 响应字段
            rtype = self._resp_type_for_ds(ds_raw) if ds_raw else None
            for comp in (pdef.get("components") or []):
                if not isinstance(comp, dict):
                    continue
                for fi in (comp.get("fields") or []):
                    if not isinstance(fi, dict):
                        continue
                    src = str(fi.get("source","")).strip()
                    if not src or not rtype or rtype not in resp_fields:
                        continue
                    src_clean = re.sub(r'^items\[[^\]]*\]\.?', '', src)
                    top = re.split(r"[\.\[\+\s]", src_clean, 1)[0]
                    known = resp_fields[rtype] | {"items","pagination"}
                    if top and top not in known:
                        self._warn("ui","U03",
                                   f"页面 {pname} 组件 {comp.get('name','')} "
                                   f"source='{src}' 中 '{top}' 不在响应类型 {rtype} 中",
                                   f"{rtype} 包含：{', '.join(sorted(resp_fields[rtype]))}")

    # ── 报告 + 入口 ────────────────────────────────────────────────

    def report(self) -> int:
        errors = [i for i in self.issues if i.level == "ERROR"]
        warns  = [i for i in self.issues if i.level == "WARN"]
        print("\n" + "═"*62)
        print("  design-flow 数据契约校验报告")
        print("═"*62)
        layer_names = {"parse":"文件解析","domain":"领域层 (domain.yaml)",
                       "api":"API 层 (api.yaml)","ui":"UI 层 (ui-schema.yaml)",
                       "cross":"跨层一致性"}
        printed = False
        for layer in ["parse","domain","api","ui","cross"]:
            items = [i for i in self.issues if i.layer == layer]
            if not items:
                continue
            print(f"\n▌ {layer_names.get(layer, layer)}")
            for issue in items:
                print(str(issue))
            printed = True
        if not printed:
            print("\n  ✅ 所有检查通过！三层契约完整且一致。")
        print("\n" + "─"*62)
        print(f"  汇总：{len(errors)} 个错误  {len(warns)} 个警告")
        print("─"*62 + "\n")
        if errors:
            print("  ❌ 校验未通过，请修复上述错误后重试。\n")
            return 1
        if self.strict and warns:
            print("  ⚠️  严格模式：存在警告，视为失败。\n")
            return 1
        if warns:
            print("  ⚠️  存在警告，建议修复，但不阻塞流程继续。\n")
        return 0

    def run(self) -> int:
        if not self.load():
            return self.report()
        self.validate_domain()
        self.validate_api()
        self.validate_ui()
        return self.report()


def main():
    if len(sys.argv) < 2:
        print("用法：python3 references/validate.py <project-slug> [--strict]")
        sys.exit(1)
    project_dir = Path(sys.argv[1])
    if not project_dir.exists():
        print(f"❌ 项目目录不存在：{project_dir}")
        sys.exit(1)
    sys.exit(ContractValidator(project_dir, "--strict" in sys.argv).run())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Optimization Agent (Dry-Run)
- Baselines: lint/type/tests/build timings (best-effort)
- Measures: frontend bundle sizes, largest files
- Analysis: simple frontend import graph reachability (orphans), backend unused imports via flake8 F401
- Output: reports/optimize_report.md (no code changes)

No new dependencies; uses stdlib and existing project scripts.
"""
from __future__ import annotations

import os
import sys
import subprocess
import time
import json
import gzip
from io import BytesIO
from pathlib import Path
import re
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "Frontend"
BACKEND = ROOT / "Backend"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def run_cmd(cmd: List[str], cwd: Path) -> Tuple[int, str, float]:
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
            check=False,
        )
        out = proc.stdout
        code = proc.returncode
    except FileNotFoundError as e:
        out = f"Command not found: {' '.join(cmd)}\n{e}"
        code = 127
    duration = time.time() - start
    return code, out, duration


def human_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def gzip_size_bytes(data: bytes) -> int:
    buf = BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(data)
    return len(buf.getvalue())


def measure_frontend_bundle() -> Dict:
    res = {
        "build_exists": False,
        "files": [],
        "total_raw": 0,
        "total_gzip": 0,
        "error": None,
    }
    build_dir = FRONTEND / "build" / "static" / "js"
    if not build_dir.exists():
        res["error"] = f"{build_dir} not found (run build)"
        return res
    res["build_exists"] = True
    files = sorted(build_dir.glob("*.js"))
    for f in files:
        try:
            data = f.read_bytes()
            raw = len(data)
            gz = gzip_size_bytes(data)
            res["files"].append({
                "path": str(f.relative_to(FRONTEND)),
                "raw": raw,
                "gzip": gz,
            })
            res["total_raw"] += raw
            res["total_gzip"] += gz
        except Exception as e:
            res["files"].append({"path": str(f), "error": str(e)})
    res["files"].sort(key=lambda x: x.get("gzip", 0), reverse=True)
    return res


IMPORT_RE = re.compile(r"^\s*import\s+(?:[\s\S]*?)\s*from\s*['\"]([^'\"]+)['\"];?\s*$|^\s*import\s*['\"]([^'\"]+)['\"];?\s*$")
REQUIRE_RE = re.compile(r"require\(['\"]([^'\"]+)['\"]\)")


def parse_imports(file_path: Path) -> Set[str]:
    imports: Set[str] = set()
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return imports
    for line in text.splitlines():
        m = IMPORT_RE.match(line)
        if m:
            mod = m.group(1) or m.group(2)
            if mod:
                imports.add(mod)
        for rm in REQUIRE_RE.finditer(line):
            mod = rm.group(1)
            if mod:
                imports.add(mod)
    return imports


def resolve_relative(base: Path, spec: str) -> List[Path]:
    # Handle only local relative imports
    if not (spec.startswith("./") or spec.startswith("../")):
        return []
    target = (base.parent / spec).resolve()
    candidates = []
    # JS/TSX resolutions
    exts = [".tsx", ".ts", ".jsx", ".js", ".json"]
    if target.is_file():
        return [target]
    for ext in exts:
        if target.with_suffix(ext).exists():
            candidates.append(target.with_suffix(ext))
    index_names = [target / f"index{ext}" for ext in exts]
    for p in index_names:
        if p.exists():
            candidates.append(p)
    return candidates


def build_frontend_graph() -> Tuple[Set[Path], Dict[Path, Set[Path]]]:
    src = FRONTEND / "src"
    if not src.exists():
        return set(), {}
    all_files: Set[Path] = set(
        p.resolve() for p in src.rglob("*") if p.suffix in {".js", ".jsx", ".ts", ".tsx"}
    )
    # Entry points
    entries = [p for p in [src / "index.tsx", src / "index.ts", src / "index.jsx", src / "index.js"] if p.exists()]
    if not entries:
        # Fallback to App.* if index missing
        entries = [p for p in [src / "App.tsx", src / "App.jsx", src / "App.ts", src / "App.js"] if p.exists()]
    graph: Dict[Path, Set[Path]] = {f: set() for f in all_files}
    for f in list(all_files):
        for spec in parse_imports(f):
            for dep in resolve_relative(f, spec):
                if dep.resolve() in all_files:
                    graph[f].add(dep.resolve())
    # Reachability
    seen: Set[Path] = set()
    stack = [e.resolve() for e in entries if e.exists()]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for dep in graph.get(cur, set()):
            if dep not in seen:
                stack.append(dep)
    return seen, graph


def backend_unused_imports() -> List[Dict]:
    code, out, dur = run_cmd([sys.executable, "-m", "flake8", ".", "--select=F401"], BACKEND)
    issues: List[Dict] = []
    if code == 127:
        return issues
    for line in out.splitlines():
        # Format: path:line:col: F401 'mod' imported but unused
        if ": F401 " in line:
            issues.append({"raw": line})
    return issues


def frontend_eslint_unused() -> List[Dict]:
    code, out, dur = run_cmd(["npm", "run", "lint"], FRONTEND)
    issues: List[Dict] = []
    if code != 0 and out:
        # Collect no-unused-vars lines
        for line in out.splitlines():
            if "no-unused-vars" in line or "unused" in line.lower():
                issues.append({"raw": line})
    return issues


def time_command_sets() -> Dict:
    results = {}
    # Frontend build
    results["frontend_build"] = {}
    code, out, dur = run_cmd(["npm", "run", "build"], FRONTEND)
    results["frontend_build"]["exit_code"] = code
    results["frontend_build"]["duration_sec"] = round(dur, 2)
    # Backend tests (fast subset)
    results["backend_pytest"] = {}
    code, out, dur = run_cmd([sys.executable, "-m", "pytest", "-q"], BACKEND)
    results["backend_pytest"]["exit_code"] = code
    results["backend_pytest"]["duration_sec"] = round(dur, 2)
    # Backend mypy
    results["backend_mypy"] = {}
    code, out, dur = run_cmd([sys.executable, "-m", "mypy", "."], BACKEND)
    results["backend_mypy"]["exit_code"] = code
    results["backend_mypy"]["duration_sec"] = round(dur, 2)
    return results


def largest_source_files(base: Path, exts: Set[str], top_n: int = 10) -> List[Dict]:
    files = []
    for p in base.rglob("*"):
        if p.suffix in exts and p.is_file():
            try:
                sz = p.stat().st_size
                files.append({"path": str(p.relative_to(base)), "bytes": sz})
            except Exception:
                pass
    files.sort(key=lambda x: x["bytes"], reverse=True)
    return files[:top_n]


def write_report(data: Dict) -> Path:
    report_path = REPORTS / "optimize_report.md"
    fb = data.get("frontend_bundle", {})
    fg_seen = data.get("frontend_graph_seen", set())
    fg_graph = data.get("frontend_graph", {})
    orphans = sorted([
        str(p.relative_to(FRONTEND / "src"))
        for p in (data.get("all_frontend_files", set()) - fg_seen)
    ]) if data.get("all_frontend_files") is not None else []

    lines: List[str] = []
    lines.append("# Optimization Agent Report (Dry-Run)")
    lines.append("")
    lines.append("## Baseline timings")
    tc = data.get("timings", {})
    for k, v in tc.items():
        lines.append(f"- {k}: exit={v.get('exit_code')} time={v.get('duration_sec')}s")
    lines.append("")

    lines.append("## Frontend bundle sizes")
    if fb.get("build_exists"):
        lines.append(f"- Total raw: {human_bytes(fb['total_raw'])}")
        lines.append(f"- Total gzip: {human_bytes(fb['total_gzip'])}")
        lines.append("- Largest files:")
        for f in fb.get("files", [])[:10]:
            if "raw" in f:
                lines.append(f"  - {f['path']} raw={human_bytes(f['raw'])} gzip={human_bytes(f['gzip'])}")
    else:
        lines.append(f"- Build missing: {fb.get('error')}")
    lines.append("")

    lines.append("## Frontend orphans (not reachable from entry)")
    if orphans:
        for o in orphans[:50]:
            lines.append(f"- {o}")
        if len(orphans) > 50:
            lines.append(f"- ... and {len(orphans)-50} more")
    else:
        lines.append("- None detected or graph not built")
    lines.append("")

    lines.append("## Backend unused imports (flake8 F401)")
    bui = data.get("backend_unused_imports", [])
    if bui:
        for i in bui[:100]:
            lines.append(f"- {i['raw']}")
        if len(bui) > 100:
            lines.append(f"- ... and {len(bui)-100} more")
    else:
        lines.append("- None detected or flake8 unavailable")
    lines.append("")

    lines.append("## Frontend linter unused hints")
    fui = data.get("frontend_unused", [])
    if fui:
        for i in fui[:100]:
            lines.append(f"- {i['raw']}")
        if len(fui) > 100:
            lines.append(f"- ... and {len(fui)-100} more")
    else:
        lines.append("- None detected or ESLint clean")
    lines.append("")

    lines.append("## Largest source files (potential split/optimize)")
    lines.append("### Frontend/src")
    for f in data.get("largest_frontend", []):
        lines.append(f"- {f['path']} ({human_bytes(f['bytes'])})")
    lines.append("### Backend")
    for f in data.get("largest_backend", []):
        lines.append(f"- {f['path']} ({human_bytes(f['bytes'])})")
    lines.append("")

    lines.append("## Suggested next actions (no changes applied)")
    lines.append("- Remove unused imports flagged above (safe, local diffs)")
    lines.append("- Consider deleting or moving orphan frontend files if truly unused")
    lines.append("- Split or lazy-load largest frontend modules; review bundle report")
    lines.append("- If you approve, the agent can auto-apply low-risk fixes in a PR-sized diff")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    data: Dict = {}

    # Baseline timings (best-effort; non-fatal)
    data["timings"] = time_command_sets()

    # Frontend bundle
    data["frontend_bundle"] = measure_frontend_bundle()

    # Frontend graph
    seen, graph = build_frontend_graph()
    data["frontend_graph_seen"] = seen
    data["frontend_graph"] = graph
    src = FRONTEND / "src"
    if src.exists():
        data["all_frontend_files"] = set(
            p.resolve() for p in src.rglob("*") if p.suffix in {".js", ".jsx", ".ts", ".tsx"}
        )
    else:
        data["all_frontend_files"] = None

    # Linters for unused
    data["backend_unused_imports"] = backend_unused_imports()
    data["frontend_unused"] = frontend_eslint_unused()

    # Largest sources
    data["largest_frontend"] = largest_source_files(FRONTEND / "src", {".js", ".jsx", ".ts", ".tsx"}) if (FRONTEND / "src").exists() else []
    data["largest_backend"] = largest_source_files(BACKEND, {".py"})

    report = write_report(data)
    print(f"Report written to {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Dump the live scene: current scene name, every element (name + path + text),
and a screenshot. This is how you learn the real object names to build screen
objects and tests against — run tools/discover.py once the AltServer is up, read
reports/scene_dump.md, then fill in selectors.
"""
from __future__ import annotations

from pathlib import Path


def dump(alt, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        scenes = alt.get_all_loaded_scenes()
    except Exception:
        scenes = []
    current = None
    try:
        current = alt.get_current_scene()
    except Exception:
        pass

    elements = alt.get_all_elements()

    lines = ["# Student app — scene dump", ""]
    lines.append(f"- Current scene: **{current}**")
    lines.append(f"- Loaded scenes: {scenes}")
    lines.append(f"- Elements: **{len(elements)}**")
    lines.append("")
    lines.append("| Name | Text | Path |")
    lines.append("|---|---|---|")
    for e in elements:
        name = getattr(e, "name", "") or ""
        try:
            text = (e.get_text() or "").replace("|", "/").replace("\n", " ")[:40]
        except Exception:
            text = ""
        try:
            data = e.to_json() if hasattr(e, "to_json") else {}
            path = (data.get("transformId") or data.get("id") or "")
        except Exception:
            path = ""
        lines.append(f"| {name.replace('|','/')} | {text} | {path} |")

    md = out_dir / "scene_dump.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        alt.get_png_screenshot(str(out_dir / "scene.png"))
    except Exception as exc:  # pragma: no cover - best effort
        print(f"[scene_dump] screenshot failed: {exc}")

    return md

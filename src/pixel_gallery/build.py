"""Build a static gallery page from a folder of images and a theme."""

from __future__ import annotations

import html
import shutil
from pathlib import Path
from typing import Any

IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def find_images(folder: Path, max_size: int) -> list[Path]:
    """Images in a folder, sorted by name, skipping files over the theme's upload limit."""
    return sorted(
        path
        for path in folder.iterdir()
        if path.suffix.lower() in IMAGE_TYPES and path.stat().st_size <= max_size
    )


def render_page(theme: dict[str, Any], images: list[str]) -> str:
    colors, layout = theme["colors"], theme["layout"]
    title = html.escape(theme["name"])
    thumbnails = "\n".join(
        f'    <img src="{html.escape(name)}" width="{layout["thumbnail_px"]}" loading="lazy" alt="">'
        for name in images
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ background: {colors["background"]}; color: {colors["text"]}; font-family: system-ui, sans-serif; }}
    main {{ display: grid; grid-template-columns: repeat({layout["columns"]}, 1fr); gap: 8px; }}
    img {{ width: 100%; border: 2px solid {colors["accent"]}; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <main>
{thumbnails}
  </main>
</body>
</html>
"""


def build_site(theme: dict[str, Any], images_dir: Path, out_dir: Path) -> Path:
    """Copy the images to out_dir, then write index.html and a _headers file for static hosts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    images = find_images(images_dir, theme["uploads"]["max_size"])
    for image in images:
        shutil.copy2(image, out_dir / image.name)
    headers = f"/*\n  Cache-Control: public, max-age={theme['cache']['max_age']}\n"
    (out_dir / "_headers").write_text(headers, encoding="utf-8")
    page = out_dir / "index.html"
    page.write_text(render_page(theme, [image.name for image in images]), encoding="utf-8")
    return page

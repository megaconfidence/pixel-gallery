"""The pixel-gallery command."""

from __future__ import annotations

import argparse
from pathlib import Path

from pixel_gallery.build import build_site
from pixel_gallery.theme import load_theme


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pixel-gallery", description="Build a static photo gallery.")
    parser.add_argument("images", type=Path, help="folder of images")
    parser.add_argument("--theme", type=Path, default=Path("themes/sunset.toml"), help="theme file")
    parser.add_argument("--out", type=Path, default=Path("site"), help="output folder")
    args = parser.parse_args(argv)
    page = build_site(load_theme(args.theme), args.images, args.out)
    print(f"Built {page}")

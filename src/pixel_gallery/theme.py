"""Gallery themes: TOML files that people share, loaded with chonkconf."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chonkconf

REQUIRED = ("name", "colors", "layout", "cache", "uploads")


def days(n: float) -> int:
    """Seconds in n days, for cache lifetimes."""
    return int(n * 24 * 60 * 60)


def megabytes(n: float) -> int:
    """Bytes in n megabytes (1 MB = 1024 * 1024 bytes), for upload limits."""
    return int(n * 1024 * 1024)


THEME_FUNCTIONS = {"days": days, "megabytes": megabytes}


def load_theme(path: str | Path) -> dict[str, Any]:
    """Load a theme file and check it has everything the site builder needs."""
    theme = chonkconf.load(path, functions=THEME_FUNCTIONS)
    missing = [key for key in REQUIRED if key not in theme]
    if missing:
        raise ValueError(f"{path}: theme is missing {', '.join(missing)}")
    return theme

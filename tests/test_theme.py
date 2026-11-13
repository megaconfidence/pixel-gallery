from pathlib import Path

import pytest

from pixel_gallery.theme import load_theme

THEMES = Path(__file__).parent.parent / "themes"


def test_sunset_theme():
    theme = load_theme(THEMES / "sunset.toml")
    assert theme["name"] == "Sunset"
    assert theme["layout"]["thumbnail_px"] == 256
    assert theme["cache"]["max_age"] == 7 * 24 * 60 * 60
    assert theme["uploads"]["max_size"] == 25 * 1024 * 1024


@pytest.mark.parametrize("path", sorted(THEMES.glob("*.toml")), ids=lambda path: path.stem)
def test_every_bundled_theme_loads(path):
    theme = load_theme(path)
    assert theme["cache"]["max_age"] > 0
    assert theme["uploads"]["max_size"] > 0


def test_a_theme_without_colors_is_rejected(tmp_path):
    path = tmp_path / "broken.toml"
    path.write_text('name = "Broken"\n[layout]\ncolumns = 2\n')
    with pytest.raises(ValueError, match="missing colors"):
        load_theme(path)

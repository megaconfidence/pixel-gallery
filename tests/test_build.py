from pathlib import Path

from pixel_gallery.build import build_site
from pixel_gallery.theme import load_theme

THEMES = Path(__file__).parent.parent / "themes"


def make_photos(folder: Path) -> Path:
    folder.mkdir()
    (folder / "cat.png").write_bytes(b"\x89PNG" + b"0" * 100)
    (folder / "dog.jpg").write_bytes(b"\xff\xd8" + b"0" * 100)
    (folder / "notes.txt").write_text("not an image")
    return folder


def test_build_writes_the_page_and_copies_images(tmp_path):
    page = build_site(load_theme(THEMES / "sunset.toml"), make_photos(tmp_path / "photos"), tmp_path / "site")
    html = page.read_text()
    assert "<title>Sunset</title>" in html
    assert 'src="cat.png"' in html and 'src="dog.jpg"' in html
    assert "notes.txt" not in html
    assert (tmp_path / "site" / "cat.png").exists()


def test_cache_header_follows_the_theme(tmp_path):
    build_site(load_theme(THEMES / "sunset.toml"), make_photos(tmp_path / "photos"), tmp_path / "site")
    assert "max-age=604800" in (tmp_path / "site" / "_headers").read_text()


def test_images_over_the_upload_limit_are_skipped(tmp_path):
    theme = load_theme(THEMES / "midnight.toml")
    photos = make_photos(tmp_path / "photos")
    (photos / "huge.png").write_bytes(b"0" * (theme["uploads"]["max_size"] + 1))
    page = build_site(theme, photos, tmp_path / "site")
    assert "huge.png" not in page.read_text()

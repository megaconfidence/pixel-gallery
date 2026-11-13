# pixel-gallery

Build a static photo gallery from a folder of images and a theme.

> **A demo project.** pixel-gallery was built for a video about the Mistral Agents SDK, as the app an agent keeps patched. Its theme loader, [chonkconf](https://github.com/megaconfidence/chonkconf), is a demo library too.

```bash
uv run pixel-gallery photos/ --theme themes/sunset.toml --out site/
```

## Themes

A theme is a TOML file: colors, layout, how long browsers cache the page, and the largest image to include. Themes are made to be shared: download one, drop it in `themes/` and build.

Values written as `"{{ ... }}"` are computed when the theme loads, with two helpers, `days(n)` and `megabytes(n)`:

```toml
[cache]
max_age = "{{ days(7) }}"

[uploads]
max_size = "{{ megabytes(25) }}"
```

## Tests

```bash
uv run pytest
```

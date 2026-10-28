# Editing Documentation

This guide explains how to edit the pyIPCS documentation source files and how to build the HTML output locally to preview your changes.

## Documentation Stack

pyIPCS documentation is built with [Sphinx](https://www.sphinx-doc.org/) using the following tools:

| Tool | Purpose |
|------|---------|
| [Sphinx](https://www.sphinx-doc.org/) | Documentation builder |
| [MyST Parser](https://myst-parser.readthedocs.io/) | Markdown support in Sphinx |
| [sphinx-autodoc-typehints](https://github.com/tox-dev/sphinx-autodoc-typehints) | Type hint rendering in API docs |
| [Furo](https://pradyunsg.me/furo/) | HTML theme |

## Directory Layout

```
docs/
├── Makefile            # Build commands (Linux/macOS)
├── make.bat            # Build commands (Windows)
└── source/
    ├── conf.py         # Sphinx configuration
    ├── index.md        # Root table of contents
    ├── api/            # API reference pages (auto-generated)
    ├── contributing/   # Contributing guides (this file lives here)
    ├── examples/       # Usage examples
    ├── getting-started/
    └── guide/          # Conceptual and architecture guides
```

All editable source files live under `docs/source/`. The `docs/build/` directory is generated and should not be edited directly.

## Install Documentation Dependencies

Documentation dependencies are included in `requirements-dev.txt`. If you have already followed the [Development Environment Setup](dev-setup) guide they are already installed. Otherwise:

```bash
pip install -r requirements-dev.txt
```

## Editing Documentation

### Markdown pages

Most pages are written in [MyST-flavoured Markdown](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html) (`.md` files). Edit them directly in `docs/source/`.

The MyST `colon_fence` extension is enabled, so you can use `:::` fences as an alternative to backtick fences for Sphinx directives:

```markdown
:::{note}
This is a note admonition.
:::
```

### Adding a new page

1. Create a new `.md` file in the appropriate subdirectory under `docs/source/`.
2. Register the page in the `toctree` in `docs/source/index.md`:

```markdown
\`\`\`{toctree}
:maxdepth: 1
:caption: Contributing

contributing/your-new-page
\`\`\`
```

### API reference pages

API reference pages under `docs/source/api/generated/` are auto-generated from Python docstrings via `sphinx.ext.autodoc` and `sphinx.ext.autosummary`. Do **not** edit these files directly — update the corresponding docstrings in `src/pyipcs/` instead and rebuild.

- Docstrings must use **Google style** (see [Napoleon docs](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)).
- Type hints in function signatures are rendered automatically by `sphinx-autodoc-typehints`.

### Sphinx configuration

Global build settings live in [`docs/source/conf.py`](../conf.py). Common things you might need to change:

- `extensions` — add or remove Sphinx extensions.
- `autodoc_mock_imports` — list packages that cannot be installed on the build host (e.g. `zoautil_py`).
- `intersphinx_mapping` — cross-reference targets for external projects.

## Building the Documentation

Run all build commands from the `docs/` directory.

### HTML (local preview)

```bash
cd docs
make html
```

The output is written to `docs/build/html/`. Open `docs/build/html/index.html` in a browser to preview.

### Clean build

If you see stale output or unexpected warnings, remove the previous build before rebuilding:

```bash
cd docs
make clean html
```

### Windows

Use `make.bat` instead of `make`:

```bat
cd docs
make.bat html
```

## Checking for Warnings

Sphinx prints warnings to the terminal during a build. Review them before submitting a pull request — broken cross-references, missing docstrings, and malformed directives all produce warnings.

To treat warnings as errors and catch every issue:

```bash
cd docs
make SPHINXOPTS="-W" html
```

## Live Preview (Optional)

[sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) watches for file changes and refreshes the browser automatically:

```bash
pip install sphinx-autobuild
cd docs
sphinx-autobuild source build/html
```

Then open `http://127.0.0.1:8000` in your browser.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import sys
from pathlib import Path

sys.path.insert(0, str(Path("../../src").resolve()))
sys.path.insert(0, str(Path("_ext").resolve()))

# Patch platform so pyipcs can be imported outside z/OS for doc builds
sys.platform = "zos"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_version", Path("../../src/pyipcs/_version.py").resolve())
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

project = 'pyIPCS'
copyright = '2026, John Gontaryk'
author = 'John Gontaryk'
release = _mod.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = f"{project} {release}"

# -- Extension configuration -------------------------------------------------

# Source file suffixes
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Mock z/OS-only dependencies unavailable on the build host
autodoc_mock_imports = ["zoautil_py"]

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
}

# Autosummary configuration
autosummary_generate = True
autosummary_generate_overwrite = True

# Napoleon configuration (Google-style docstrings)
napoleon_numpy_docstring = False
napoleon_google_docstring = True
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_notes = True

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 3

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# MyST-NB configuration
nb_execution_mode = "off"

# Suppress specific warnings
suppress_warnings = [
    "docutils",
]

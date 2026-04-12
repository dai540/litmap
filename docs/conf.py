from __future__ import annotations

import os
import sys

ROOT = os.path.abspath("..")
SRC = os.path.abspath(os.path.join("..", "src"))
sys.path.insert(0, SRC)
sys.path.insert(0, ROOT)

project = "litmap"
author = "Dai"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.autodoc",
]

source_suffix = {
    ".md": "markdown",
}

master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = ["colon_fence", "deflist"]

html_theme = "pydata_sphinx_theme"
html_title = "litmap documentation"
html_logo = "assets/litmap-logo.svg"
html_favicon = "assets/litmap-icon.svg"
html_static_path = ["_static", "assets"]
html_css_files = ["custom.css"]
html_show_sourcelink = False

html_theme_options = {
    "navigation_with_keys": True,
    "show_prev_next": False,
    "announcement": "Minimal package. Minimal docs. No large bundled data.",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/dai540/litmap",
            "icon": "fa-brands fa-github",
        },
    ],
}

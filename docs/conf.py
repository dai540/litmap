from __future__ import annotations

import os
import sys
from datetime import datetime

ROOT = os.path.abspath("..")
SRC = os.path.abspath(os.path.join("..", "src"))
sys.path.insert(0, SRC)
sys.path.insert(0, ROOT)

project = "litmap"
author = "Daiki"
copyright = f"{datetime.now():%Y}, {author}"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/*.html",
    "tutorials/admet-safety-landscape.md",
    "tutorials/immunotherapy-landscape.md",
    "tutorials/local-csv-corpus.md",
    "tutorials/openalex-topic-scan.md",
    "tutorials/target-discovery-omics.md",
    "tutorials/translational-biomarker-stratification.md",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
]

templates_path = ["_templates"]
html_theme = "pydata_sphinx_theme"
html_title = "litmap documentation"
html_logo = "assets/litmap-logo.svg"
html_favicon = "assets/litmap-icon.svg"
html_static_path = ["_static", "assets"]
html_css_files = ["custom.css"]
html_extra_path = ["case-studies", "tutorial-data", "examples"]
html_show_sourcelink = False

html_theme_options = {
    "navigation_with_keys": True,
    "show_prev_next": False,
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "secondary_sidebar_items": ["page-toc"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/dai540/litmap",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Tutorials",
            "url": "tutorials/index.html",
            "icon": "fa-solid fa-book-open",
        },
    ],
    "announcement": "Cluster in analysis space, then project into display space.",
    "sidebarwidth": 280,
}

html_context = {
    "default_mode": "light",
}

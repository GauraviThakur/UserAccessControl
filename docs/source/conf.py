
import os
import sys

# Add the project root directory to Python's module search path
sys.path.insert(0, os.path.abspath("../.."))

# Project information
project = "User Access Control"
copyright = "2026, Project Author"
author = "Project Author"
release = "1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

# HTML output settings
html_theme = "sphinx_rtd_theme"

# Source file settings
source_suffix = {
    ".rst": "restructuredtext",
}

# Language
language = "en"

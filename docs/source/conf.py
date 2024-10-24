# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

project = 'AlaniaHSE bot'
copyright = '2024, Атаев Георгий, Чибиров Руслан'
author = 'Атаев Георгий, Чибиров Руслан'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
      'sphinx.ext.autodoc', 
      'sphinx.ext.napoleon', 
      'autodocsumm', 
      'sphinx.ext.coverage',
      'sphinx_wagtail_theme',
      'sphinx.ext.viewcode'
]

auto_doc_default_options = {'autosummary': True}

sys.path.insert(0, os.path.abspath('../../src'))

templates_path = ['_templates']
exclude_patterns = ['sphinx_wagtail_theme']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_wagtail_theme'
html_static_path = ['_static']

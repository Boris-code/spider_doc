# -*- coding: utf-8 -*-
#
# python3-cookbook documentation build configuration file, created by
# sphinx-quickstart on Tue Aug 19 03:21:45 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['chinese_search', 'sphinx.ext.mathjax']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
source_suffix = ['.rst', '.md']

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'boris-spider'
copyright = u'2020, boris'
author = u'boris'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = 'v 1.0.0'
# The full version, including alpha/beta/rc tags.
release = '1.1.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'zh_CN'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'Mannul Doc'


# -- Options for LaTeX output ---------------------------------------------

# Comment this sentence when gernerating a HTML page package.
# latex_engine = 'xelatex'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'boris-spider.tex', 'boris-spider Documentation',
     'boris', 'howto'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'boris-spider', 'boris-spider Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'boris-spider', 'boris-spider Documentation',
     author, 'boris', u'boris',
     'Miscellaneous'),
]


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# To generate Chinese PDF, you need to add the following code.
if on_rtd:
    latex_elements = {
        # The paper size ('letterpaper' or 'a4paper').
        #'papersize': 'letterpaper',
        # The font size ('10pt', '11pt' or '12pt').
        #'pointsize': '10pt',
        # Additional stuff for the LaTeX preamble.
        'preamble': r'''
    \hypersetup{unicode=true}
    \usepackage{CJKutf8}
    \DeclareUnicodeCharacter{00A0}{\nobreakspace}
    \DeclareUnicodeCharacter{2203}{\ensuremath{\exists}}
    \DeclareUnicodeCharacter{2200}{\ensuremath{\forall}}
    \DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}
    \DeclareUnicodeCharacter{2713}{x}
    \DeclareUnicodeCharacter{27FA}{\ensuremath{\Longleftrightarrow}}
    \DeclareUnicodeCharacter{221A}{\ensuremath{\sqrt{}}}
    \DeclareUnicodeCharacter{221B}{\ensuremath{\sqrt[3]{}}}
    \DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}
    \DeclareUnicodeCharacter{2297}{\ensuremath{\otimes}}
    \begin{CJK}{UTF8}{gbsn}
    \AtEndDocument{\end{CJK}}
    ''',
    }
else:
    latex_elements = {
        'papersize': 'a4paper',
        'utf8extra': '',
        'inputenc': '',
        'babel'     : r'''\usepackage[english]{babel}''',
        'preamble' : r'''
        \usepackage{ctex}
        ''',
    }

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_exts = "../exts"
sys.path.append(os.path.abspath(_exts))

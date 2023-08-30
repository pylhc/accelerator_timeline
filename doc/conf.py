# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import pathlib
import os
import shutil
import sys
import warnings

# ignore numpy warnings, see:
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Ignore potential warnings from matplotlib when building the gallery
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Matplotlib is currently using agg, which is a" " non-GUI backend, so cannot show the figure.",
)


TOPLEVEL_DIR = pathlib.Path(__file__).parent.parent.absolute()
ABOUT_FILE = TOPLEVEL_DIR / "__init__.py"

if str(TOPLEVEL_DIR) not in sys.path:
    sys.path.insert(0, str(TOPLEVEL_DIR))

ABOUT_accelerator_timeline: dict = {}
with ABOUT_FILE.open("r") as f:
    exec(f.read(), ABOUT_accelerator_timeline)

# Set environment variable for scripts to check if we are in sphinx-mode
from utilities.sphinx_helper import SPHINX_BUILD_ENVIRON
os.environ[SPHINX_BUILD_ENVIRON] = '1'


# Copy accelerator data file
shutil.copy2(
    TOPLEVEL_DIR / "accelerator-parameters.csv", 
    TOPLEVEL_DIR / "doc" / "accelerator-parameters.csv"
)


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = ABOUT_accelerator_timeline["__title__"]
copyright_ = '2019-2023, pyLHC/OMC-TEAM'
author = ABOUT_accelerator_timeline["__author__"]

rst_prolog = f"""
:github_url: {ABOUT_accelerator_timeline['__url__']}
"""

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ABOUT_accelerator_timeline["__version__"][:3]
# The full version, including alpha/beta/rc tags.
release = ABOUT_accelerator_timeline["__version__"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"


# Config for the sphinx_issues extension
issues_github_path = "pylhc/accelerator_timeline"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "docs", "docker", "tests", ".github", ".vscode"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "obj"

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Extensions Configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # Include documentation from docstrings
    "sphinx.ext.autosectionlabel",  # Allow reference sections using its title
    "sphinx.ext.autosummary",  # Generate autodoc summaries
    "sphinx.ext.coverage",  # Collect doc coverage stats
    "sphinx.ext.doctest",  # Test snippets in the documentation
    "sphinx.ext.githubpages",  # Publish HTML docs in GitHub Pages
    "sphinx.ext.intersphinx",  # Link to other projects’ documentation
    "sphinx.ext.mathjax",  # Render math via JavaScript
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.todo",  # Support for todo items
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    # "sphinxcontrib.bibtex",  # Insert BibTeX citations into Sphinx documentation
    "sphinx_copybutton",  # Add a "copy" button to code blocks
    "sphinx_gallery.gen_gallery",  # Build an HTML gallery of examples from a set of Python scripts
    "sphinx_issues",  # Link to project's issue tracker
    "matplotlib.sphinxext.plot_directive",  # Include a Matplotlib plot in a Sphinx document
    "sphinx-prompt",  # prompt symbols will not be copy-pastable
]

# Config for autosectionlabel extension
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# Config for the napoleon extension
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# Configuration for sphinx.ext.todo
todo_include_todos = True

# Config for the sphinxcontrib.bibtex extension
# bibtex_bibfiles = ["references.bib"]
# bibtex_default_style = "unsrt"
# bibtex_reference_style = "label"

# -- Setup scrapers for the gallery ------------------------------------------
from plotly.io._sg_scraper import plotly_sg_scraper
import plotly.io as pio
pio.renderers.default = 'sphinx_gallery'

# To use SVG outputs when scraping matplotlib figures for the sphinx-gallery
from sphinx_gallery.scrapers import matplotlib_scraper
from sphinx_gallery.sorting import ExampleTitleSortKey
class matplotlib_svg_scraper(object):
    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, format="svg", **kwargs)

# Config for the matplotlib plot directive
plot_formats = [("svg", 250)]

# image_scrapers = (matplotlib_svg_scraper(), plotly_sg_scraper,)
image_scrapers = (matplotlib_svg_scraper(),)

# -- Configuration for the sphinx-gallery extension -------------------------------
sphinx_gallery_conf = {
    "examples_dirs": ["../"],  # directory where to find plotting scripts
    "gallery_dirs": ["gallery"],  # directory where to store generated plots
    "filename_pattern": "^((?!sgskip).)*$",  # which files to execute
    "subsection_order": ExampleTitleSortKey,
    "within_subsection_order": ExampleTitleSortKey,
    "reference_url": {"accelerator_timeline": None},  # Sets up intersphinx in gallery code
    "backreferences_dir": "gen_modules/backreferences",  # where function/class granular galleries are stored
    # Modules for which function/class level galleries are created
    "doc_module": "accelerator_timeline",
    "image_scrapers": image_scrapers,  # scrape galleries
    "image_srcset": ["2x"],  # use srcset twice as dense for high-resolution images display
    "min_reported_time": 2,  # minimum execution time to enable reporting
    "remove_config_comments": True,  # remove config comments from the code
    "capture_repr": ("_repr_html_",),  # use the html output
    "compress_images": ("images", "thumbnails", "-o1"),
    "only_warn_on_example_error": True,  # keep the build going if an example fails, very important for doc workflow
    "download_all_examples": False,
}

# Config for the sphinx_panels extension
panels_css_variables = {
    "tabs-color-label-inactive": "rgba(178, 206, 245, 0.90)",  # increase alpha from defaults
}


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "collapse_navigation": False,
    "display_version": True,
    "logo_only": True,
    "navigation_depth": 2,
}

# Name of an image file (path relative to the configuration directory)
# that is the logo of the docs, or URL that points an image file for the logo.
# It is placed at the top of the sidebar;
# its width should therefore not exceed 200 pixels.
html_logo = '_static/img/omc_logo.svg'


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#
html_static_path = ["_static"]

# A dictionary of values to pass into the template engine’s context for all
# pages. Single values can also be put in this dictionary using the
# -A command-line option of sphinx-build.
html_context = {
    "display_github": True,
    # the following are only needed if :github_url: is not set
    "github_user": author,
    "github_repo": project,
    "github_version": "master/doc/",
}

# A list of CSS files. The entry must be a filename string or a tuple
# containing the filename string and the attributes dictionary.
# The filename must be relative to the html_static_path, or a full URI with
# scheme like https://example.org/style.css.
# The attributes is used for attributes of <link> tag.
# It defaults to an empty list.
#
html_css_files = ["css/custom.css"]

smartquotes_action = "qe"  # renders only quotes and ellipses (...) but not dashes (option: D)

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
# html_last_updated_fmt = None

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr', 'zh'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "accelerator_timeline_doc"

# -- Options for LaTeX output ---------------------------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = "letter"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [(master_doc, "accelerator_timeline.tex", "accelerator_timeline Documentation", author, "manual")]

# Use Unicode aware LaTeX engine
latex_engine = "xelatex"  # or 'lualatex'

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = None

latex_elements = {}

# Keep babel usage also with xelatex (Sphinx default is polyglossia)
# If this key is removed or changed, latex build directory must be cleaned
latex_elements["babel"] = r"\usepackage{babel}"

# Font configuration
# Fix fontspec converting " into right curly quotes in PDF
# cf https://github.com/sphinx-doc/sphinx/pull/6888/
latex_elements[

    "fontenc"
] = r"""
\usepackage{fontspec}
\defaultfontfeatures[\rmfamily,\sffamily,\ttfamily]{}
"""

# Sphinx 2.0 adopts GNU FreeFont by default, but it does not have all
# the Unicode codepoints needed for the section about Mathtext
# "Writing mathematical expressions"
fontpkg = r"""
\IfFontExistsTF{XITS}{
 \setmainfont{XITS}
}{
 \setmainfont{XITS}[
  Extension      = .otf,
  UprightFont    = *-Regular,
  ItalicFont     = *-Italic,
  BoldFont       = *-Bold,
  BoldItalicFont = *-BoldItalic,
]}
\IfFontExistsTF{FreeSans}{
 \setsansfont{FreeSans}
}{
 \setsansfont{FreeSans}[
  Extension      = .otf,
  UprightFont    = *,
  ItalicFont     = *Oblique,
  BoldFont       = *Bold,
  BoldItalicFont = *BoldOblique,
]}
\IfFontExistsTF{FreeMono}{
 \setmonofont{FreeMono}
}{
 \setmonofont{FreeMono}[
  Extension      = .otf,
  UprightFont    = *,
  ItalicFont     = *Oblique,
  BoldFont       = *Bold,
  BoldItalicFont = *BoldOblique,
]}
% needed for \mathbb (blackboard alphabet) to actually work
\usepackage{unicode-math}
\IfFontExistsTF{XITS Math}{
 \setmathfont{XITS Math}
}{
 \setmathfont{XITSMath-Regular}[
  Extension      = .otf,
]}
"""
latex_elements["fontpkg"] = fontpkg


# Additional stuff for the LaTeX preamble.
latex_elements[
    "preamble"
] = r"""
   % Show Parts and Chapters in Table of Contents
   \setcounter{tocdepth}{0}
   % One line per author on title page
   \DeclareRobustCommand{\and}%
     {\end{tabular}\kern-\tabcolsep\\\begin{tabular}[t]{c}}%
   \usepackage{etoolbox}
   \AtBeginEnvironment{sphinxthebibliography}{\appendix\part{Appendices}}
   \usepackage{expdlist}
   \let\latexdescription=\description
   \def\description{\latexdescription{}{} \breaklabel}
   % But expdlist old LaTeX package requires fixes:
   % 1) remove extra space
   \makeatletter
   \patchcmd\@item{{\@breaklabel} }{{\@breaklabel}}{}{}
   \makeatother
   % 2) fix bug in expdlist's way of breaking the line after long item label
   \makeatletter
   \def\breaklabel{%
       \def\@breaklabel{%
           \leavevmode\par
           % now a hack because Sphinx inserts \leavevmode after term node
           \def\leavevmode{\def\leavevmode{\unhbox\voidb@x}}%
      }%
   }
   \makeatother
"""

# Sphinx 1.5 provides this to avoid "too deeply nested" LaTeX error
# and usage of "enumitem" LaTeX package is unneeded.
# Value can be increased but do not set it to something such as 2048
# which needlessly would trigger creation of thousands of TeX macros
latex_elements["maxlistdepth"] = "10"
latex_elements["pointsize"] = "11pt"

# Better looking general index in PDF
latex_elements["printindex"] = r"\footnotesize\raggedright\printindex"

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
latex_appendices = []

# If false, no module index is generated.
latex_use_modindex = True

latex_toplevel_sectioning = "part"

# If false, no module index is generated.
# latex_domain_indices = True

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "Accelerator Timeline", "Accelerator Timeline", [author], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "Accelerator Timeline",
        "Accelerator Timeline, Documentation",
        author,
        "Accelerator Timeline",
        "Collection of Data of Accelerators.",
        "Examples",
    )
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# -- Autodoc Configuration ---------------------------------------------------

# Add here all modules to be mocked up. When the dependencies are not met
# at building time. 
autodoc_mock_imports = []

# -- Instersphinx Configuration ----------------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
# use in refs e.g:
# :ref:`comparison manual <python:comparisons>`
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

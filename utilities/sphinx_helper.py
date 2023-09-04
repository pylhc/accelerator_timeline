
""" 
Sphinx Helper
*************

Some functionality to make working with Sphinx easier.
"""
import os
from pathlib import Path
import sys

SPHINX_BUILD_ENVIRON = "SPHINX_BUILD"


def get_gallery_dir() -> Path:
    """ Get the gallery directory. 
    
    Returns:
        Path: Path to the gallery directory.
    """
    return Path(__file__).parent.parent / "doc" / "gallery"


def is_sphinx_build() -> bool:
    """ Check if we are running in sphinx build mode.

    Returns:
        bool: True if in sphinx build mode.
    """
    return os.environ.get(SPHINX_BUILD_ENVIRON, "0") == "1"


def is_interactive() -> bool:
    """ Check if we are running in interactive mode.

    Returns:
        bool: True if in interactive mode.
    """
    return bool(getattr(sys, 'ps1', sys.flags.interactive))
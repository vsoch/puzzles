__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.0.11"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsoch@users.noreply.github.com"
NAME = "puzzles"
PACKAGE_URL = "https://github.com/vsoch/puzzles"
KEYWORDS = "python puzzle solver"
DESCRIPTION = "solve puzzles with Python"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("numpy", {"min_version": None}),
    ("matplotlib", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

ALL_REQUIRES = INSTALL_REQUIRES + TESTS_REQUIRES

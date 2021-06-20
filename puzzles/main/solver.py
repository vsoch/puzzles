__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from puzzles.main.segment import segment_jpgs
from puzzles.logger import bot
import os
import sys


def solve_puzzle(self, images=None):
    """Solve a puzzle from a set of input images of the pieces. Specifically,
    we do the following:

    - read in each valid input images (self.pieces)
    - segment from the background
    - run the solver algorithm

    each of the above steps can be done in the sibling scripts here, but
    this entrypoint is intended to complete the entire flow of steps.

    Parameters
    ==========
    images: a list (or single) image to segment for pieces.
    name: a name for the puzzle (defaults to robot namer)

    """
    # Add images to be solved?
    if images is not None:
        self.load_images(images)

    pieces = []
    for piece in self.pieces:

        # 1. segment jpgs
        segmented = segment_jpgs(piece.image)

        # 2.

    if len(pieces) == 1:
        pieces = pieces[0]
    return pieces

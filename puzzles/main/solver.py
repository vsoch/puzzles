'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from puzzles.main.segment import segment_jpgs
from puzzles.logger import bot
import os
import sys


def solve_puzzle(self, images=None):
    '''Solve a puzzle from a set of input images of the pieces. Specifically,
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
 
    '''
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

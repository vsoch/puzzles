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


def solve_puzzle(self, images):
    '''Solve a puzzle from a set of input images of the pieces. Specifically,
       we do the following:

       - read in each valid input images
       - segment from the background
       - run the solver algorithm

       each of the above steps can be done in the sibling scripts here, but
       this entrypoint is intended to complete the entire flow of steps.
 
       Parameters
       ==========
       images: a list (or single) image to segment for pieces.
 
    '''

    if not isinstance(images, list):
        images = [images]

    pieces = []
    for image in images:
        print('bwaaa write me!')

    if len(pieces) == 1:
        pieces = pieces[0]
    return pieces

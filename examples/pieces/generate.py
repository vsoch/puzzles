#!/usr/bin/env python3

from puzzles.models import PiecesPuzzle
import os

here = os.path.abspath(os.path.dirname(__file__))

images = [os.path.join(here, "img", x) for x in os.listdir(os.path.join(here, "img"))]

# Create the puzzle! We need the height (in pieces) and width (in pieces)
# You can overestimate the dimension, but you shouldn't under-estimate!
puzzle = PiecesPuzzle(images, height=4, width=4)

# This just plots the pieces
fig = puzzle.get_puzzle_figure()
fig.savefig(os.path.join(here, "pieces.png"))

puzzle.metrics()
# Minimum piece size : 30
# Width              : 32
# Height             : 32
# Number pieces      : 5

# Shuffle pieces (if necessary)
puzzle.shuffle()
fig = puzzle.get_puzzle_figure()
fig.savefig(os.path.join(here, "shuffle.png"))

# Solve (to the best that we can)
puzzle.solve()
solved_fig = puzzle.get_solved_figure()
solved_fig.savefig("examples/pieces/solved.png")

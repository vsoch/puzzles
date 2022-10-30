#!/usr/bin/env python3

from puzzles.models import PhotoPuzzle
import os

here = os.path.abspath(os.path.dirname(__file__))

print("Creating puzzle...")
puzzle = PhotoPuzzle(os.path.join(here, "img", "white-edges.png"), min_piece_size=120)

# Show the original image
# fig = puzzle.get_image_figure()
# fig = puzzle.get_puzzle_figure()

print("Shuffling...")
puzzle.shuffle()

# Now show the puzzle broken into pieces!
# puzfig = puzzle.get_puzzle_figure()
print("Solving...")
puzzle.solve()
solved_fig = puzzle.get_solved_figure()

print("Saving to white-pieces-solved.png")
solved_fig.savefig(os.path.join(here, "img", "white-pieces-solved.png"))

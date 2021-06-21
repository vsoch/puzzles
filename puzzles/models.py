__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2017-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from puzzles.logger import logger
from puzzles.utils import get_temporary_name

import collections
import numpy as np
from numpy import linalg as la

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os
import sys


class PlacedPiece:
    def __init__(self, index, loc):

        # The index of the piece in the puzzle array
        self.index = index

        # The x,y coordinate, not pixel location but piece location
        self.loc = loc

    def __str__(self):
        return "PuzzlePiece(index=%s, loc=%s)" % (self.index, self.loc)

    def __repr__(self):
        return self.__str__()


class PhotoPuzzle:
    def __init__(self, image, max_rgb=255, min_piece_size=30, font=None):
        """
        Generate a puzzle from a photo and solve it.
        """
        # Solver settings
        self.max_rgb = max_rgb
        self.min_piece_size = min_piece_size

        # If we generate puzzle images with text
        self.font = font or self.default_font()
        self.cmap = "gray"

        # Dictionary mapping each open location to a set of placed pieces.
        # Note that an open location means edges alongside a placed piece
        self.open_places = collections.defaultdict(set)

        # Locations of covered places to piece index.
        self.covered_places = {}

        # Lookup of piece distances
        self.piece_distances = {}

        self.pieces = []
        self.load_image(image)
        self.generate_pieces()

    def generate_pieces(self):
        """
        Given a loaded puzzle image, generate some number of pieces.
        """
        for i in range(self.horizontal_num_pieces):
            for j in range(self.vertical_num_pieces):
                # Split into pieces with dimensions x, y, and color
                self.pieces.append(
                    self.image[
                        j * self.piece_height : (j + 1) * self.piece_height,
                        i * self.piece_width : (i + 1) * self.piece_width,
                        :,
                    ]
                )

    def __exit__(self):
        """
        Close plots on instance destruction
        """
        plt.close()

    def metrics(self):
        """
        Print metrics about the puzzle, calculated based on min piece size.
        """
        logger.info("Image file         : %s" % self.filename)
        logger.info("Minimum piece size : %s" % self.min_piece_size)
        logger.info("Width              : %s" % self.width)
        logger.info("Height             : %s" % self.height)
        logger.info("Number pieces      : %s" % self.count_pieces())

    def load_image(self, image):
        """
        Load the image to turn into a puzzle.
        """
        if not os.path.exists(image):
            logger.exit("%s does not exist." % image)
        self.image_file = image
        self.filename = os.path.basename(image)
        self.image = mpimg.imread(image)
        self.height, self.width = self.image.shape[0:2]

    def get_image_figure(self, title=None, show=True):
        """
        Get a plot of the entire image.
        """
        # TODO what's th eright way to close tis?
        fig = plt.figure(figsize=(self.vertical_num_pieces, self.horizontal_num_pieces))
        plt.imshow(self.image, cmap=self.cmap)

        # If we have a title, add it
        if title:
            plt.title(title, fontdict=self.font)
        if show:
            plt.show()
        return plt

    def shuffle(self):
        """
        Shuffle the pieces, and reset open and covered pieces.
        """
        np.random.shuffle(self.pieces)
        self.open_places = collections.defaultdict(set)
        self.covered_places = {}

    def get_neighbors(self, x, y):
        """
        Get neighbor locations of a piece.
        """
        return {(x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y)}

    def add_piece(self, new_piece):
        """
        Given a set of covered and open places, place a piece!
        """
        if new_piece.loc in self.covered_places:
            raise ValueError("Location %s already occupied." % new_piece)

        # The new piece location is no longer open
        self.open_places.pop(new_piece.loc, None)

        # Add the piece to the lookup of covered places
        self.covered_places[new_piece.loc] = new_piece.index

        # The neighbors of the added piece
        for neighbor in self.get_neighbors(*new_piece.loc):
            if neighbor not in self.covered_places:
                self.open_places[neighbor].add(new_piece)

    def make_scores(self, unused_pieces_indices):
        """
        Given unused piece indices, calculate
        """
        scores = {}
        for new_piece_index in unused_pieces_indices:
            for loc, placed_neighbors in self.open_places.items():
                scores[new_piece_index, loc] = np.mean(
                    [
                        self.find_score(
                            new_piece=PlacedPiece(index=new_piece_index, loc=loc),
                            neighbor_piece=neighbor_piece,
                        )
                        for neighbor_piece in placed_neighbors
                    ]
                )
        return scores

    def get_piece_distance(self, p1, e1, p2, e2):
        """
        Calculate and cache the distance between two pieces
        """
        if (p1, e1, p2, e2) not in self.piece_distances:
            edge1 = self.get_piece_edges(p1, e1)
            edge2 = self.get_piece_edges(p2, e2)
            self.piece_distances[p1, e1, p2, e2] = self.edge_matching_score(
                edge1, edge2
            )
        return self.piece_distances[p1, e1, p2, e2]

    def get_piece_edges(self, p, e):
        """
        Get edges of a piece.

        This is where we link data from self.pieces into our calculation
        """
        piece = self.pieces[p]
        if e == 0:
            return piece[0, :]
        if e == 1:
            return piece[:, -1]
        if e == 2:
            return piece[-1, :][::-1]
        if e == 3:
            return piece[:, 0][::-1]
        raise ValueError("e should be 0, 1, 2, or 3. Got %s." % e)

    def edge_matching_score(self, edge1, edge2):
        """
        Given two edges, calculate a matching score
        """
        if edge1.shape != edge2.shape:
            return np.inf
        edge_diff = edge1 - edge2[::-1]
        return np.log(la.norm(np.minimum(edge_diff, self.max_rgb - edge_diff), ord=1))

    def find_score(self, new_piece, neighbor_piece):
        """
        Calculate a score between two pieces
        """
        x_diff = new_piece.loc[0] - neighbor_piece.loc[0]
        y_diff = new_piece.loc[1] - neighbor_piece.loc[1]

        # New piece to the RIGHT of neighbor
        if x_diff == 1 and y_diff == 0:
            return self.get_piece_distance(new_piece.index, 3, neighbor_piece.index, 1)

        # New piece to the LEFT of neighbor
        if x_diff == -1 and y_diff == 0:
            return self.get_piece_distance(new_piece.index, 1, neighbor_piece.index, 3)

        # New piece BELOW neighbor
        if x_diff == 0 and y_diff == 1:
            return self.get_piece_distance(new_piece.index, 0, neighbor_piece.index, 2)

        # New piece ABOVE neighbor
        if x_diff == 0 and y_diff == -1:
            return self.get_piece_distance(new_piece.index, 2, neighbor_piece.index, 0)

        raise ValueError(
            f"Found x_diff={x_diff} and y_diff={y_diff} between "
            "new_piece and neighbor_piece. One diff should be 0 and the other should "
            "be +1 or -1."
        )

    def solve(self):
        """
        Solve the puzzle (restore to original state, hopefully!
        """
        # Reset open and covered places
        self.open_places = collections.defaultdict(set)
        self.covered_places = {}

        # Add the first piece.
        self.add_piece(PlacedPiece(index=0, loc=(0, 0)))

        # Get indices of unused pieces
        unused_pieces_indices = set(range(len(self.pieces))) - {0}

        # Add remaining pieces to the puzzle
        while unused_pieces_indices:

            # Create a matching score based
            scores = self.make_scores(unused_pieces_indices)
            new_index, new_loc = min(scores, key=scores.get)
            unused_pieces_indices.remove(new_index)
            self.add_piece(PlacedPiece(index=new_index, loc=new_loc))

        self.reset_covered_indices()

    def reset_covered_indices(self):
        x_min = min([loc[0] for loc in self.covered_places])
        y_min = min([loc[1] for loc in self.covered_places])
        self.covered_places = {
            (x - x_min, y - y_min): index
            for (x, y), index in self.covered_places.items()
        }

    def plot_puzzle(self, n_rows, n_cols, plot_piece):
        """
        Shared function to plot puzzle
        """
        fig, axs = plt.subplots(n_rows, n_cols)
        fig.set_figheight(n_rows)
        fig.set_figwidth(n_cols)

        for y, ax_row in enumerate(axs):
            for x, ax in enumerate(ax_row):
                plot_piece(ax, x, y)
                ax = axs[y, x]
                ax.xaxis.set_visible(False)
                ax.axes.yaxis.set_visible(False)

        for col, ax in enumerate(axs[0]):
            ax.set_title(col)

        for row, ax in enumerate(axs[:, 0]):
            ax.set_ylabel(row)
            ax.axes.yaxis.set_visible(True)
            ax.axes.yaxis.set_ticks([])
        return fig

    def get_puzzle_figure(self):
        """
        Show the current state of the puzzle.

        This function plots self.pieces, not the puzzle solution.
        """

        def plot_piece(ax, x, y):
            ax.imshow(self.pieces[y + x * self.vertical_num_pieces])

        return self.plot_puzzle(
            self.vertical_num_pieces, self.horizontal_num_pieces, plot_piece
        )

    def get_solved_figure(self):
        """
        Get figure for solved puzzle
        """
        n_rows = max([loc[1] for loc in self.covered_places]) + 1
        n_cols = max([loc[0] for loc in self.covered_places]) + 1

        # The solved figure has a different function to plot the piece
        def plot_covered_piece(ax, x, y):
            if (x, y) in self.covered_places:
                piece_index = self.covered_places[(x, y)]
                ax.imshow(self.pieces[piece_index])

        return self.plot_puzzle(
            n_rows=max([loc[1] for loc in self.covered_places]) + 1,
            n_cols=max([loc[0] for loc in self.covered_places]) + 1,
            plot_piece=plot_covered_piece,
        )

    @property
    def vertical_num_pieces(self):
        return self.height // self.min_piece_size

    @property
    def horizontal_num_pieces(self):
        return self.width // self.min_piece_size

    @property
    def piece_height(self):
        return self.height // self.vertical_num_pieces

    @property
    def piece_width(self):
        return self.width // self.horizontal_num_pieces

    def default_font(self):
        """define the font style for saving png figures
        if a title is provided
        """
        return {"family": "serif", "color": "darkred", "weight": "normal", "size": 16}

    # Metadata

    def count_pieces(self):
        """return a count of the pieces"""
        return len(self.pieces)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[puzzle][%s:[%s]" % (self.filename, self.count_pieces())

    def save_png(self, output_folder=None, image_type="cleaned", title=None):
        """save an original or cleaned dicom as png to disk.
        Default image_format is "cleaned" and can be set
        to "original." If the image was already clean (not
        flagged) the cleaned image is just a copy of original
        """
        from matplotlib import pyplot as plt

        if hasattr(self, image_type):
            png_file = self._get_clean_name(output_folder, "png")
            plt = self.get_figure(image_type=image_type, title=title)
            plt.savefig(png_file)
            plt.close()
            return png_file
        else:
            bot.warning("use detect() --> clean() before saving is possible.")

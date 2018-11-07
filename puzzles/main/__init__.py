'''

Puzzle and Piece: main classes to represent a puzzle

Copyright (C) 2017-2018 Vanessa Sochat.

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

from puzzles.logger import bot
from puzzles.utils import get_temporary_name
from puzzles.main.solver import solve_puzzle

from skimage.io import imread

bot.level = 3

import os
import sys


class Piece(object):

    def __init__(self, filename, name=None):
 
        # Generate a robot name for the puzzle, if one not provided
        self.name = name or bot.RobotNamer.generate()       
        self.filename = None
        self.load_image(filename)

    def __str__(self):
        return self.name or self.filename

    def __repr__(self):
        return self.__str__()

    def load_image(self, filename):
        filename = os.path.abspath(filename)
        if os.path.exists(filename):
            self.filename = filename
            self.image = imread(filename)
        else:
            bot.warning("%s does not exist" % filename)


class Puzzle(object):

# Setup

    def __init__(self, images=None, name=None, font=None):
 
        # Generate a robot name for the puzzle, if one not provided
        self.name = name or bot.RobotNamer.generate()

        # We store pieces (object Piece) along with raw images
        self.pieces = []
        if images is not None:
            self.load_images(images)

        # If we generate puzzle images with text
        self.font = font or self.default_font()
        self.cmap = 'gray'

# Load

    def load_images(self, images):
        '''load one or more images into the puzzle

           Parameters
           ==========
           images: to load into the puzzle pieces

        '''
        if not isinstance(images, (list, tuple)):
            images = [images]

        for image in images:
            piece = Piece(image)
            if piece.filename is not None:
                self.pieces.append(piece)
            bot.info('Loaded %s pieces' % self.count_pieces())
     

    def default_font(self):
        '''define the font style for saving png figures
           if a title is provided
        '''
        return {'family': 'serif',
                'color':  'darkred',
                'weight': 'normal',
                'size': 16}


# Metadata

    def count_pieces(self):
        '''return a count of the pieces
        '''
        return len(self.pieces)

    def speak(self):
        '''
           a function for the client to announce him or herself, depending
           on the level specified. Includes number of pieces.

        '''
        if self.quiet is False:
            bot.info('[puzzles|%s pieces: %s] ' % (self.name,
                                                   self.count_pieces()))

    def __repr__(self):
        return "[puzzles][%s]" %self.count_pieces()

    def __str__(self):
        return "[puzzles][%s]" %self.count_pieces()

    def client_name(self):
        return self.name

        

    def clean(self):
        '''
        take a dicom image and a list of pixel coordinates, and return
        a cleaned file (if output file is specified) or simply plot 
        the cleaned result (if no file is specified)
    
        Parameters
        ==========
            add_padding: add N=margin pixels of padding
            margin: pixels of padding to add, if add_padding True
        '''

        if not self.results:
            bot.warning('Use %s.detect() to find coordinates first.' %self)

        else:
            bot.info('Scrubbing %s.' %self.dicom_file)

            # Load in dicom file, and image data
            dicom = read_file(self.dicom_file, force=True)

            # We will set original image to image, cleaned to clean
            self.original = dicom._get_pixel_array()
            self.cleaned = self.original.copy()

            # Compile coordinates from result
            coordinates = []
            for item in self.results['results']:
                if len(item['coordinates']) > 0:
                    for coordinate_set in item['coordinates']:
                        # Coordinates expected to be list separated by commas
                        new_coordinates = [int(x) for x in coordinate_set.split(',')]
                        coordinates.append(new_coordinates) # [[1,2,3,4],...[1,2,3,4]]

            for coordinate in coordinates:
                minr, minc, maxr, maxc = coordinate
                self.cleaned[minc:maxc, minr:maxr] = 0  # should fill with black
                                           

    def get_figure(self, show=False, image_type="cleaned", title=None):
        '''get a figure for an original or cleaned image. If the image
           was already clean, it is simply a copy of the original.
           If show is True, plot the image.
        '''
        from matplotlib import pyplot as plt
        
        if hasattr(self, image_type):
            fig, ax = plt.subplots(figsize=(10, 6))      
            ax.imshow(self.cleaned, cmap=self.cmap)
            if title is not None:
                plt.title(title, fontdict=self.font)
            if show is True:
                plt.show()
            return plt


    def _get_clean_name(self, output_folder, extension='dcm'):
        '''return a full path to an output file, with custom folder and
           extension. If the output folder isn't yet created, make it.
 
           Parameters
           ==========
           output_folder: the output folder to create, will be created if doesn't
           exist.
           extension: the extension of the file to create a name for, should
           not start with "."
        '''
        if output_folder is None:
            output_folder = self.output_folder

        if not os.path.exists(output_folder):
            bot.debug('Creating output folder %s' % output_folder)
            os.mkdir(output_folder)

        basename = re.sub('[.]dicom|[.]dcm', '', os.path.basename(self.dicom_file))
        return "%s/cleaned-%s.%s" %(output_folder, basename, extension)

    def save_png(self, output_folder=None, image_type="cleaned", title=None):
        '''save an original or cleaned dicom as png to disk.
           Default image_format is "cleaned" and can be set 
           to "original." If the image was already clean (not 
           flagged) the cleaned image is just a copy of original
        '''
        from matplotlib import pyplot as plt

        if hasattr(self, image_type):
            png_file = self._get_clean_name(output_folder, 'png')
            plt = self.get_figure(image_type=image_type, title=title)
            plt.savefig(png_file)
            plt.close()
            return png_file
        else:
            bot.warning('use detect() --> clean() before saving is possible.')


Puzzle.solve = solve_puzzle

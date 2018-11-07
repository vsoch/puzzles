#!/bin/env python

# This script will load in test images and use the Puzzle / Pieces classes
# to (manually) test segmentation quality, etc.

image = "../img/pieces.jpg"

puzzle = Puzzle(images=image, name=image)

# Test piece
piece = puzzle.pieces[0]
img = piece.image

## 1. Active Contour Model

print('Testing active contour model')

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour

img = rgb2gray(img)

s = np.linspace(0, 2*np.pi, 400)
x = 220 + 100*np.cos(s)
y = 100 + 100*np.sin(s)
init = np.array([x, y]).T

snake = active_contour(gaussian(img, 3),
                       init, alpha=0.015, beta=10, gamma=0.001)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])
plt.savefig('dev/active-contour-model.jpg')

print('Testing Quickshift')


# Imports
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.color import rgb2gray
from skimage.util import img_as_float

# Convert to float
img = img_as_float(piece.image)


# Test Felzenzwalb #############################################################

sigmas = [4.0, 5.0, 6.0, 10.0]
coords = [(0,0),(0,1),(1,0),(1,1)]
fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

for i in range(0,4):
    x = coords[i][0]
    y = coords[i][1]
    segments_fz = felzenszwalb(img, scale=100, sigma=sigmas[i], min_size=50)
    ax[x, y].imshow(mark_boundaries(img, segments_fz))
    ax[x, y].set_title("Felzenszwalbs's method, sigma %s" %sigmas[i])


for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()

# Test SLIC ####################################################################

# Doesn't seem to detect pieces well, but detects background in chunks

compacts = [10,25,50,100]
coords = [(0,0),(0,1),(1,0),(1,1)]
fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

for i in range(1,4):
    x = coords[i-1][0]
    y = coords[i-1][1]
    segments_slic = slic(img, n_segments=i*10, compactness=compacts[i=1], sigma=1)
    ax[x, y].imshow(mark_boundaries(img, segments_slic))
    ax[x, y].set_title("SLIC K-means based method, N=%s" %i)


for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()


# Test Quickshift ##############################################################

# Time doesn't scale well with kernel (slow to run)

coords = [(0,0),(0,1),(1,0),(1,1)]
fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

for i in range(1,4):
    x = coords[i-1][0]
    y = coords[i-1][1]
    segments_quick = quickshift(img, kernel_size=i*10, max_dist=6, ratio=0.5)
    ax[x, y].imshow(mark_boundaries(img, segments_quick))
    ax[x, y].set_title("Quickshift, kernel size=%s" %i)

for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()


# Test Watershed ###############################################################


gradient = sobel(rgb2gray(img))
segments_watershed = watershed(gradient, markers=250, compactness=0.001)

fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

for i in range(0,3):
    x = coords[i][0]
    y = coords[i][1]
    segments_watershed = watershed(gradient, markers=250, compactness=0.001)
    ax[x,y] = imshow(mark_boundaries(img, segments_watershed))
    ax[x,y].set_title('Watershet, markers 250')

for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()

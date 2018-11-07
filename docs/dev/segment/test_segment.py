#!/bin/env python

# This script will load in test images and use the Puzzle / Pieces classes
# to (manually) test segmentation quality, etc.

from puzzles.main import Puzzle

image = "../pieces.jpg"

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

coords = [(0,0),(0,1),(1,0),(1,1)]
markers = [10, 50, 100, 200]
gradient = sobel(rgb2gray(img))

fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

for i in range(0,4):
    x = coords[i][0]
    y = coords[i][1]
    segments_watershed = watershed(gradient, markers=markers[i], compactness=0.001)
    ax[x,y].imshow(mark_boundaries(img, segments_watershed))
    ax[x,y].set_title('Watershet, markers %s' %markers[i])

for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()


# Region Bound Based RAG #######################################################

from skimage.future import graph
from skimage import data, segmentation, color, filters, io

gimg = color.rgb2gray(img)

labels = segmentation.slic(img, compactness=30, n_segments=400)
edges = filters.sobel(gimg)
edges_rgb = color.gray2rgb(edges)

g = graph.rag_boundary(labels, edges)
lc = graph.show_rag(labels, g, edges_rgb, img_cmap=None, edge_cmap='viridis',
                    edge_width=1.2)

plt.colorbar(lc, fraction=0.03)
io.show()


# Sobel + Watershed ############################################################

from skimage.filters import sobel
from skimage.measure import label
from skimage.segmentation import slic, join_segmentations
from skimage.morphology import watershed
from skimage.color import label2rgb
from skimage import data

coins = rgb2gray(img)

# Make segmentation using edge-detection and watershed.
edges = sobel(coins)

# Identify some background and foreground pixels from the intensity values.
# These pixels are used as seeds for watershed.
markers = np.zeros_like(coins)
foreground, background = 1, 2
markers[coins < 30.0] = background
markers[coins > 150.0] = foreground

ws = watershed(edges, markers)
seg1 = label(ws == foreground)

# Make segmentation using SLIC superpixels.
seg2 = slic(coins, n_segments=117, max_iter=160, sigma=1, compactness=0.75,
            multichannel=False)

# Combine the two.
segj = join_segmentations(seg1, seg2)

# Show the segmentations.
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(9, 5),
                         sharex=True, sharey=True)
ax = axes.ravel()
ax[0].imshow(coins, cmap='gray')
ax[0].set_title('Image')

color1 = label2rgb(seg1, image=coins, bg_label=0)
ax[1].imshow(color1)
ax[1].set_title('Sobel+Watershed')

color2 = label2rgb(seg2, image=coins, image_alpha=0.5)
ax[2].imshow(color2)
ax[2].set_title('SLIC superpixels')

color3 = label2rgb(segj, image=coins, image_alpha=0.5)
ax[3].imshow(color3)
ax[3].set_title('Join')

for a in ax:
    a.axis('off')
fig.tight_layout()
plt.show()


# Otsu #########################################################################

from skimage.filters import threshold_otsu
thresh = threshold_otsu(image)
binary = image > thresh

#fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 2.5))
fig = plt.figure(figsize=(8, 2.5))
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2)
ax3 = plt.subplot(1, 3, 3, sharex=ax1, sharey=ax1)

ax1.imshow(image, cmap=plt.cm.gray)
ax1.set_title('Original')
ax1.axis('off')

ax2.hist(image)
ax2.set_title('Histogram')
ax2.axvline(thresh, color='r')

ax3.imshow(binary, cmap=plt.cm.gray)
ax3.set_title('Thresholded')
ax3.axis('off')

plt.show()

# Threshold Minimum ############################################################

from skimage.filters import threshold_minimum

thresh_min = threshold_minimum(image)
binary_min = image > thresh_min

fig, ax = plt.subplots(2, 2, figsize=(10, 10))

ax[0, 0].imshow(image, cmap=plt.cm.gray)
ax[0, 0].set_title('Original')

ax[0, 1].hist(image.ravel(), bins=256)
ax[0, 1].set_title('Histogram')

ax[1, 0].imshow(binary_min, cmap=plt.cm.gray)
ax[1, 0].set_title('Thresholded (min)')

ax[1, 1].hist(image.ravel(), bins=256)
ax[1, 1].axvline(thresh_min, color='r')

for a in ax[:, 0]:
    a.axis('off')
plt.show()

# Chan #########################################################################

from skimage import data, img_as_float
from skimage.segmentation import chan_vese

image = img_as_float(rgb2gray(img))

# Try thresholding first

from skimage.filters import threshold_mean
thresh = threshold_mean(image)
binary = image > thresh

fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].set_title('Original image')

ax[1].imshow(binary, cmap=plt.cm.gray)
ax[1].set_title('Result')

for a in ax:
    a.axis('off')

plt.show()


# Feel free to play around with the parameters to see how they impact the result
cv = chan_vese(image, mu=0.25, lambda1=1, lambda2=1, tol=1e-3, max_iter=200,
               dt=0.5, init_level_set="checkerboard", extended_output=True)

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.flatten()

ax[0].imshow(image, cmap="gray")
ax[0].set_axis_off()
ax[0].set_title("Original Image", fontsize=12)

ax[1].imshow(cv[0], cmap="gray")
ax[1].set_axis_off()
title = "Chan-Vese segmentation - {} iterations".format(len(cv[2]))
ax[1].set_title(title, fontsize=12)

ax[2].imshow(cv[1], cmap="gray")
ax[2].set_axis_off()
ax[2].set_title("Final Level Set", fontsize=12)

ax[3].plot(cv[2])
ax[3].set_title("Evolution of energy over iterations", fontsize=12)

fig.tight_layout()
plt.show()

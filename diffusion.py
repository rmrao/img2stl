#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from scipy.ndimage.filters import generic_filter

from imageprep import prepareImg

globimage = None
globsource = None

def diffuse(image, w=[1,1,1,1], source=None):
	# Weights: [Up, Down, Left, Right]
	ymax, xmax = image.shape
	ymax -= 1
	xmax -= 1
	newim = np.zeros(image.shape)
	yind, xind = np.indices(image.shape)
	newim[yind > 0] += w[0]*image[yind < ymax]
	newim[yind < ymax] += w[1]*image[yind > 0]
	newim[xind > 0] += w[2]*image[xind < xmax]
	newim[xind < xmax] += w[3]*image[xind > 0]

	newim[(yind > 0) & (xind > 0) & (yind < ymax) & (xind < xmax)] /= float(sum(w))
	newim[(yind == 0) & (xind > 0) & (xind < xmax)] /= float(w[1] + w[2] + w[3])
	newim[(yind == ymax) & (xind > 0) & (xind < xmax)] /= float(w[0] + w[2] + w[3])
	newim[(yind > 0) & (yind < ymax) & (xind == 0)] /= float(w[0] + w[1] + w[3])
	newim[(yind > 0) & (yind < ymax) & (xind == xmax)] /= float(w[0] + w[1] + w[2])
	newim[0, 0] /= float(w[1] + w[3])
	newim[ymax, 0] /= float(w[0] + w[3])
	newim[0, xmax] /= float(w[1] + w[2])
	newim[ymax, xmax] /= float(w[0] + w[2])

	if source is not None:
		newim[source] = image[source]

	return newim

def randwalk(image):
	return np.random.randint(2, size=image.shape)*2 - 1

def importance_filter(image):
	footprint = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
	return np.abs(generic_filter(image, lambda vals: vals.mean(), footprint=footprint) - image)

def multrandwalk(image, importance=None):
	if importance is None:
		importance = importance_filter(image)
	randwalk_mask = np.zeros(image.shape, dtype=bool)
	y, x = np.random.randint(image.shape[0]), np.random.randint(image.shape[1])
	randwalk_mask[y, x] = True
	isvalid = lambda (y, x), (ymax, xmax): (0 <= x < xmax) and (0 <= y < ymax)
	for i in range(10000):
		neighbors = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
		nvals = [importance[n] if isvalid(n, image.shape) else 0 for n in neighbors]
		if not any(nvals):
			nvals = [1 if isvalid(n, image.shape) else 0 for n in neighbors]
		probs = np.cumsum(nvals, dtype=np.float64)
		probs /= probs[-1]
		index = np.nonzero(probs > np.random.random())[0][0]
		y, x = neighbors[index]
		randwalk_mask[y, x] = True
	return randwalk_mask


def updateFig(i, anim, func):
	global globimage, globsource
	globimage = func(globimage, globsource)
	anim.set_data(globimage)
	return anim,

def test(image, func, n=100, source=None):
	global globimage, globsource
	globimage = image
	globsource = source
	fig = plt.figure()
	im = plt.imshow(image, cmap=cm.Greys_r, animated=True)
	ani = animation.FuncAnimation(fig, updateFig, frames=xrange(n), fargs=(im, func), interval=1)
	plt.show()

def updateFig2(i, anim, image, importance):
	global globimage
	rw = multrandwalk(image, importance)
	globimage[rw] = image[rw]
	anim.set_data(globimage)
	return anim,


def test2(image, n=10):
	global globimage
	globimage = np.zeros(image.shape) + 50
	importance = importance_filter(image)
	fig = plt.figure()
	im = plt.imshow(image, cmap=cm.Greys_r, animated=True)
	ani = animation.FuncAnimation(fig, updateFig2, frames=xrange(n), fargs=(im, image, importance), interval=50)
	plt.show()


import sys

if __name__ == '__main__':
	img = prepareImg('pics/escher.jpg', compress=True)
	if len(sys.argv) == 2 and sys.argv[1] == 'randwalk':
		test(img, lambda image, source: image + randwalk(image))
	elif len(sys.argv) == 2 and sys.argv[1] == 'diffuse':
		test(img, lambda image, source: diffuse(image, [1, 1, 1, 1], source))
	elif len(sys.argv) == 2 and sys.argv[1] == 'both':
		test(img, lambda image, source: diffuse(image, [1, 1, 1, 1], source) + randwalk(image))
	elif len(sys.argv) == 2 and sys.argv[1] == 'randwalk2':
		test2(img)
	else:
		print "Unknown test"

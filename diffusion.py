#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

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

	if source != None:
		newim[source] = image[source]

	return newim

def randwalk(image):
	return image + (np.random.randint(2, size=image.shape)*2 - 1)

def updateFig1(i, anim):
	global globimage
	globimage = randwalk(globimage)
	anim.set_data(globimage)
	return anim,

def updateFig2(i, anim):
	global globimage, globsource
	globimage = diffuse(globimage, [1, 1, 1, 1], globsource)
	anim.set_data(globimage)
	return anim,

def test1(image, n=100):
	global globimage
	globimage = image
	fig = plt.figure()
	im = plt.imshow(image, cmap=cm.Greys_r, animated=True)
	ani = animation.FuncAnimation(fig, updateFig1, frames=xrange(n), fargs=(im,), interval=1)
	plt.show()

def test2(image, n=100, source=None):
	global globimage, globsource
	globimage = image
	globsource = source
	fig = plt.figure()
	im = plt.imshow(image, cmap=cm.Greys_r, animated=True)
	ani = animation.FuncAnimation(fig, updateFig2, frames=xrange(n), fargs=(im,), interval=1)
	plt.show()

import sys

if __name__ == '__main__':
	img = prepareImg('pics/escher.jpg', compress=True)
	if len(sys.argv) == 2 and sys.argv[1] == 'randwalk':
		test1(img)
	else:
		test2(img)

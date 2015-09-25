import numpy as np
from PIL import Image

def img2array(filename):
	"""Turns an image into a numpy array. Requires PIL (Python Imaging Library) or Pillow (a PIL fork)."""
	img = Image.open(filename)
	array = np.array(img, dtype=np.float32)
	if array.ndim == 3:
		array = array.sum(2)
	return array

def compressImage(image, height):
	"""
	Note: Should probably replace this method with one from photutils or PIL.Image. Will probably be faster/more accurate and can handle
	both increasing and decreasing resolution
	"""
	"""
	Compresses the image to a given size. Given that 3D printing cannot handle fine resolution, any 
	loss of resolution is ultimately unimportant.
	"""
	h, w = image.shape
	width = int(w * height / float(h))
	array = np.zeros((height, width))
	y_step = h / float(height)
	x_step = w / float(width)
	for y in range(height):
		for x in range(width):
			array[y, x] = image[y * y_step, x * x_step]
	return array

def crop_image(image, _max=0.0, masks=None, table=None):
	locations = np.where(image > _max)
	ymin, ymax, xmin, xmax = min(locations[0]), max(locations[0]), min(locations[1]), max(locations[1])
	image = image[ymin:ymax + 1, xmin:xmax + 1]
	toreturn = image
	if masks:
		masks = [mask[ymin:ymax + 1, xmin:xmax + 1] for mask in masks]
		toreturn = [toreturn, masks]
	if table:
		print len(table['xcen'])
		table = table[table['xcen'] < xmax]
		table = table[table['ycen'] < ymax]
		table['xcen'] = table['xcen'] - xmin
		table['ycen'] = table['ycen'] - ymin
		table = table[table['xcen'] > 0]
		table = table[table['ycen'] > 0]
		print len(table['xcen'])
		toreturn.append(table)
	return toreturn

def normalize(array, norm, height=255.):
	"""
	Taken, with some slight modifications, from the module qimage2ndarray. As this module requires 
	installation of itself, SIP, and PyQt4, it is simpler to copy this 
	method, which does not require either extension. See http://hmeine.github.io/qimage2ndarray/ for 
	more information.

	The parameter `normalize` can be used to normalize an image's
	value range to 0..height:

	`normalize` = (nmin, nmax):
	  scale & clip image values from nmin..nmax to 0..height

	`normalize` = nmax:
	  lets nmin default to zero, i.e. scale & clip the range 0..nmax
	  to 0..height

	`normalize` = True:
	  scale image values to 0..255 (same as passing (gray.min(),
	  gray.max()))
	"""
	if not norm:
		return array

	if norm is True:
		norm = array.min(), array.max()
	elif np.isscalar(norm):
		norm = (0, norm)

	nmin, nmax = norm
	array = array - nmin
	array = array * height / float(nmax - nmin)
	return array
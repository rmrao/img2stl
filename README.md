# Convert Images to 3D STL format

## Usage:

Navigate to your `img2stl` folder then open a python shell:

	from imageprep import prepareImg
	from meshcreator import to_mesh
	img = prepareImg('<path2img>')
	to_mesh(img, '<new_file_name>')

A few notes:
	1. `prepareImg` has a bunch of parameters for doing some pre-processing on the image. I have set them to the defaults that generally work best. Feel free to experiment as you see fit. Code is not commented (this is from a larger project and was really just a debugging method), but it is fairly straightforward.
	2. `to_mesh` also has a few parameters. Really the only one you might want to mess with is the depth parameter, which allows you to set a depth for the back plate. If you want to print vertically, having a deeper back plate gives greater stability.
	3. `to_mesh` adds '.STL' to the end of the filename so you don't need to.
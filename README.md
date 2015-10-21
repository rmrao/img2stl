# Convert Images to 3D STL format

## Usage:

If you only want to run this with the default arguments, there is a script that will do this for you. Navigate to your `img2stl` folder, then run the following command:

	./makestl.py <path_to_img> <new_file_name>

If you do want to change the default arguments, then open a python shell and follow this format:

	from imageprep import prepareImg
	from meshcreator import to_mesh
	img = prepareImg('<path2img>', <arg1>, <arg2>, ...)
	to_mesh(img, '<new_file_name>', <arg1>, <arg2>, ...)

Some of the parameters you might want to change:
* `prepareImg` has a bunch of parameters for doing some pre-processing on the image. I have set them to the defaults that generally work best. Feel free to experiment as you see fit. Code is not commented (this is from a larger project and was really just a debugging method), but it is fairly straightforward.
* If your image is more than 500x500 pixels and you don't think you'll need the extra resolution (the image is smoothed anyway to create a better 3D structure), then you might want to set `crop=True` in `prepareImg`.
* `to_mesh` also has a few parameters. Really the only one you might want to mess with is the depth parameter, which allows you to set a depth for the back plate. If you want to print vertically, having a deeper back plate gives greater stability.
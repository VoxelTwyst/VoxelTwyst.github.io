from sys import argv
from PIL import Image
from numpy import asarray

from util import HSVImageData
import pixim


def get_two_images(id:str):  # This is just an admin function that loads the two images, which should be called <id>left and <id>right.
    left = HSVImageData( Image.open("in\\" + argv[2] + "left.png") ) # HSVImageData is explained in util.py
    right = HSVImageData( Image.open("in\\" + argv[2] + "left.png") )

    assert left.width == right.width and left.height == right.height, "Input images are not the same size"  # Complain about inconsistent image sizes

    return left, right


if __name__ == "__main__":
    print("Getting files...")

    left, right = get_two_images(argv[2])
    out = None

    if argv[1] == "pixim":  # This is the important one
        print("Running pixim...")
        out = pixim.run(left, right)  # Call the algorithm from the other file

    if out is not None:  # Render the output files (in a super awkward but necessary way)
        print("Generating output file at out\\" + argv[2] + "_" + argv[1] + ".png")
        out_image = Image.fromarray(asarray(out)).convert("RGB")  # I need to convert a 2D list of floats to a greyscale image. However, PIL only supports numpy arrays
                                                                  # so I have to convert it into one of those first.
        out_image.save("out/" + argv[2] + "_" + argv[1] + ".png")  # Then just save the image as PNG

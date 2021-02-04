from sys import argv
from PIL import Image
from numpy import asarray

from util import HSVImageData, DimensionError
import pixim
import monsim
import post_mond


""" NOTE TO SELF
other possible similarity functions:
- Contextual Similarity: based on the mean/median and stdev/iqr of the surrounding pixels
- Quotient Similarity: rather than finding the difference between a and b, find the quotient (need to watch out for zeros)
"""


def get_two_images(id:str):  # This is just an admin function that loads the two images, which should be called <id>left and <id>right.
                             # My thing that generates test data sets the id to the current date and time.
    left = HSVImageData( Image.open("in\\" + argv[2] + "left.png") ) # HSVImageData is explained in util.py
    right = HSVImageData( Image.open("in\\" + argv[2] + "left.png") )

    if left.width != right.width or left.height != right.height:
        raise DimensionError

    return left, right


if __name__ == "__main__":
    print("Getting files...")

    if argv[1] == "post_mond":  # Ignore this, this is for testing a different, unfinished algorithm
        print("Running mond...")
        out = post_mond.run(HSVImageData( Image.open("out\\" + argv[2]) ), 5)
    else:
        left, right = get_two_images(argv[2])

    if argv[1] == "pixim":  # This is the important one
        print("Running pixim...")
        out = pixim.run(left, right)  # Call the algorithm from the other file

    elif argv[1] == "monsim":  # Also ignore this
        print("Running monsim...")
        out = monsim.run(left, right, 3)

    if out != None:  # Render the output files (in a super awkward way)
        print("Generating output file at out\\" + argv[2] + "_" + argv[1] + ".png")
        out_image = Image.fromarray(asarray(out)).convert("RGB")  # I need to convert a 2D list of floats to a greyscale image. However, PIL only supports numpy arrays
                                                                  # so I have to convert it into one of those first.
        out_image.save("out/" + argv[2] + "_" + argv[1] + ".png")  # Then just save the image as PNG

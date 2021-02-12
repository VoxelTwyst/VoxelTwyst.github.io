# per-PIXel sIMilarity
import PIL as il

from util import HSVImageData, rotate


def similarity(a, b):  # Takes two colours and tells you how similar the colours are.
    sim_h = 1 - abs(a[0] - b[0])  # Take the absolute difference of the colour values, but then invert them because we want the similarity, not the difference.
    sim_s = 1 - abs(a[1] - b[1])
    sim_v = 1 - abs(a[2] - b[2])

    return (sim_h + sim_h + sim_s + sim_v)  # Return the average of the colour values.


def run(left:HSVImageData, right:HSVImageData):  # The actual thing
    print("- getting ready...")
    width = left.width  # Store the width and height of both images in easy-to-access variables because we verified earlier that both images are the same size.
    height = left.height

    similarity_maps = [[[0 for i in range(height)] for i in range(width)] for i in range(width)]  # Create a bunch of empty greyscale images (aka 2D number arrays)

    print("- generating similarity maps...")
    for depth in range(width):  # Depth is being interpreted in terms of a change in x-position, so we iterate horizontally.
                                # We basically shift the image along to the right.
        for x in range(width):  # We iterate through the first image:
            for y in range(height):
                try:  # For each pixel, try and compare its values in the two images, incorporating the x-shift from above.
                    similarity_maps[depth][x][y] = similarity(left[x + depth][y], right[x][y])
                except IndexError: # Sometimes the image will be shifted too far and there won't be matching pairs where they don't overlap.
                    pass  # When this happens we just ignore it.
    
    similarity_maps = rotate(similarity_maps)  # This function just changes the 3D array of similarity maps to make it easier to iterate over in the way I want
                                               # It is kind of explained in util.py.

    print("- generating depth map...")
    depth_map = [[0 for j in range(height)] for i in range(width)]  # Now we're making the final depth map, by selecting the depth at which the pixels are the most similar.
                                                                    # This is explained better in design.md.
    for x in range(width):  # Iterate per-pixel through all the similarity maps at once.
        for y in range(height):
            
            max_depth = 0
            number_at_max = 0
            for (depth, sim) in enumerate(similarity_maps[x][y]):  # Find the depth with the highest similarity value for that pixel.
                if sim > similarity_maps[x][y][int(max_depth)]:
                    max_depth = int(depth)
                    number_at_max = 1
                
                elif sim == similarity_maps[x][y][int(max_depth)]:  # If there's a tie for most similar, find the average of each of the most similar depths.
                    max_depth = int((max_depth * number_at_max) + depth)
                    number_at_max += 1
                    max_depth /= number_at_max
            
            depth_map[x][y] = max_depth  # Fill the value for that pixel in on the depth map.
        
    print("- done!")
    
    return depth_map  # finally return it

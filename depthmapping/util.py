from PIL import Image


class HSVImageData:  # Class for storing an image in HSV format
    @staticmethod
    def data_255_to_1(data):
        return [[(j[0] / 255, j[1] / 255, j[2] / 255) for j in i] for i in data]

    # data is stored from 0 to 1
    def __init__(self, *args):  # It can be converted from various other types
        
        if isinstance(args[0], Image.Image):
            data = list( args[0].convert("HSV").getdata() )[:-2]
            width, height = args[0].size
            data = [ data[i * width : (i + 1) * width] for i in range(height) ]

            data = HSVImageData.data_255_to_1(data)

        elif type(args[0]) == int:
            if len(args) == 2:
                args.append((0, 0, 0))

            data = [[args[3] for j in range(args[1])] for i in range(args[0])]
        
        elif len(args) > 1:
            data = args
        
        else:
            data = args[0]

        self.data = list(data)
        self.width = len(data)
        self.height = len(data[0])


    def __getitem__(self, indices):  # implement the image[...] syntax
        """
        image[x] --> The xth column.
        image[x, y] --> A tuple representing the colour of the pixel at (x, y).
        image[x, y, c] --> The float value of the component c ("h", "s", or "v") of the pixel at (x, y).
        """
        if type(indices) == int:
            return self.data[indices]

        try:
            return self.data[ indices[0] ][ indices[1] ][ {"h": 0, "s": 1, "v": 2}[indices[2]] ]
        except IndexError:
            return self.data[indices[0]][indices[1]]


    def __setitem__(self, indices, value):  # implement the image[x, y] = (h, s, v) syntax.
        self.data[indices[0]][indices[1]] = value


    def __str__(self):  # you can convert it into a string so you can print it out nicely for debugging.
        return str(self.data)


class DimensionError(Exception):  # Special class for the error that gets thrown when the two images are different sizes.
                                  # I should have used assert for this but oh well
    pass


def rotate(data):  # This just makes it easier to iterate through the similarity maps when I'm finding the depth map
    """
    Goes from
        [depths:[columns:[pixels]]]
    to
        [columns:[pixels:[depths]]]
    """

    r = [[[0 for o in data] for j in data[0][0]] for i in data[0]]

    for depth in range(len(data)):
        for x in range(len(data[depth])):
            for y in range(len(data[depth][x])):
                r[x][y][depth] = data[depth][x][y]

    return r


def median(arr):  # Finds the median of arr. This is a really slow way of doing it on purpose so I can "iterate" on it.
    arr = sorted(arr)
    if len(arr) % 2 == 1:
        return arr[len(arr) // 2]
    else:
        return 0.5 * (arr[len(arr) // 2 - 1] + arr[len(arr) // 2])
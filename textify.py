from shutil import get_terminal_size

import numpy as np
from PIL import Image


DEFAULT_ALPHABET = ' .:-=+*#%@'


def textify(path, line_height=7/4, brightness=1, invert=True,
            alphabet=DEFAULT_ALPHABET):
    """Convert an image to text.

    line_height: height/width ratio of a character
    alphabet: characters to use, ordered from darkest to lightest
    """
    img = Image.open(path)

    # Scale the image to take up the whole terminal width
    columns, _ = get_terminal_size()
    lines = round(img.size[1] / img.size[0] * columns / line_height)
    img = img.resize((columns, lines), resample=Image.BICUBIC)

    # Convert to grayscale by combining the RGB values of each pixel
    pixels = np.sum(np.asarray(img), axis=2)
    # Smush the pixel values between 0 and 1
    pixels = (pixels - pixels.min()) / pixels.max()
    if invert:
        pixels = 1.0 - pixels

    # Adjust brightness
    pixels = pixels ** brightness

    # Find the appropriate character index for each pixel
    pixels *= len(alphabet) - 1
    pixels = pixels.astype(int)

    # Get the corresponding character for each pixel
    chars = np.asarray(list(alphabet))[pixels]

    # Convert the 2D array to a single string
    return '\n'.join((''.join(row) for row in chars))


if __name__ == '__main__':
    import sys
    print(textify(sys.argv[1]))

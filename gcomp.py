import argparse
from project.image_comparison import ImageComparer


def compare(ha: str, dec: str, image: str, data: str):
    print('Input')
    print('ha: ' + ha)
    print('dec: ' + dec)
    print('Path to image: ' + image)
    print('Path to NED data: ' + data)

    ImageComparer(float(ha), float(dec)).compare(image, data)


parser = argparse.ArgumentParser()

parser.add_argument("ha")
parser.add_argument("dec")
parser.add_argument("image")
parser.add_argument("ned_data")

args = parser.parse_args()

compare(args.ha, args.dec, args.image, args.ned_data)

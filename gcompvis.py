from PyQt6 import QtWidgets
from project.image_comparison_interactive import ImageComparisonInteractive
import sys
import matplotlib
import argparse
matplotlib.use('QtAgg')


parser = argparse.ArgumentParser()

parser.add_argument("ha")
parser.add_argument("dec")
parser.add_argument("image")
parser.add_argument("ned_data")
parser.add_argument("search_radius", nargs='?', default=250)

args = parser.parse_args()
app = QtWidgets.QApplication(sys.argv)
w = ImageComparisonInteractive(args.ha, args.dec, args.image, args.ned_data, int(args.search_radius))
app.exec()

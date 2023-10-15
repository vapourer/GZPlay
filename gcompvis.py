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

args = parser.parse_args()
app = QtWidgets.QApplication(sys.argv)
w = ImageComparisonInteractive(args.ha, args.dec, args.image, args.ned_data)
app.exec()

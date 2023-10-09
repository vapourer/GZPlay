from PyQt6 import QtWidgets
from project.image_comparison_interactive import ImageComparisonInteractive
import sys
import matplotlib
matplotlib.use('QtAgg')


app = QtWidgets.QApplication(sys.argv)
w = ImageComparisonInteractive(214.998306, 53.008884, '87dba57e-bce6-4cdf-b937-d21331fd4a07.png', '88106301.csv')
app.exec()

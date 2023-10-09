import matplotlib
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QRadioButton, QGridLayout

from project.image_canvas import ImageCanvas
from project.transformation import Transformation

matplotlib.use('QtAgg')


class ImageComparisonInteractive(QtWidgets.QMainWindow):

    def __init__(self, ha: float, dec: float, png: str, ned: str, *args, **kwargs):
        super(ImageComparisonInteractive, self).__init__(*args, **kwargs)

        main_layout = QVBoxLayout()

        self.canvas = ImageCanvas(ha, dec)
        self.canvas.compare(png, ned)
        main_layout.addWidget(self.canvas)

        filters_layout = QGridLayout()

        button_default = QRadioButton("Default")
        filters_layout.addWidget(button_default, 0, 0)

        button_f115w = QRadioButton("F115W")
        filters_layout.addWidget(button_f115w, 0, 1)

        button_f150w = QRadioButton("F150W")
        filters_layout.addWidget(button_f150w, 0, 2)

        button_f200w = QRadioButton("F200W")
        filters_layout.addWidget(button_f200w, 0, 3)

        button_f277w = QRadioButton("F277W")
        filters_layout.addWidget(button_f277w, 1, 0)

        button_f356w = QRadioButton("F356W")
        filters_layout.addWidget(button_f356w, 1, 1)

        button_f410w = QRadioButton("F410W")
        filters_layout.addWidget(button_f410w, 1, 2)

        button_f444w = QRadioButton("F444W")
        filters_layout.addWidget(button_f444w, 1, 3)

        filters_layout_widget = QWidget()
        filters_layout_widget.setLayout(filters_layout)

        main_layout.addWidget(filters_layout_widget)
        main_layout.addWidget(filters_layout_widget)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)

        self.setCentralWidget(main_layout_widget)
        # self.setCentralWidget(canvas)

        self.show()

    def update_transformation_matrix(self, transformation: Transformation):
        self.canvas.update_transformation_matrix(transformation)

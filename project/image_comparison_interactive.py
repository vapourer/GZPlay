import matplotlib
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, QLineEdit, QLabel

from project.image_canvas import ImageCanvas
from project.transformation import Transformation

matplotlib.use('QtAgg')


class ImageComparisonInteractive(QtWidgets.QMainWindow):

    def __init__(self, ha: float, dec: float, png: str, ned: str, search_radius: int, *args, **kwargs):
        super(ImageComparisonInteractive, self).__init__(*args, **kwargs)

        self.png = png
        self.ned = ned

        main_layout = QGridLayout()

        self.canvas = ImageCanvas(ha, dec, png, ned, search_radius)
        self.canvas.load()
        main_layout.addWidget(self.canvas, 0, 0)

        filters_layout = QGridLayout()

        button_default = QRadioButton("Default")
        button_default.setChecked(True)
        button_default.clicked.connect(lambda: self.update_transformation_matrix(Transformation.DEFAULT))
        filters_layout.addWidget(button_default, 0, 0)

        button_f115w = QRadioButton("F115W")
        button_f115w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F115W))
        filters_layout.addWidget(button_f115w, 0, 1)

        button_f150w = QRadioButton("F150W")
        button_f150w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F150W))
        filters_layout.addWidget(button_f150w, 0, 2)

        button_f200w = QRadioButton("F200W")
        button_f200w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F200W))
        filters_layout.addWidget(button_f200w, 0, 3)

        button_f277w = QRadioButton("F277W")
        button_f277w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F277W))
        filters_layout.addWidget(button_f277w, 1, 0)

        button_f356w = QRadioButton("F356W")
        button_f356w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F356W))
        filters_layout.addWidget(button_f356w, 1, 1)

        button_f410w = QRadioButton("F410W")
        button_f410w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F410M))
        filters_layout.addWidget(button_f410w, 1, 2)

        button_f444w = QRadioButton("F444W")
        button_f444w.clicked.connect(lambda: self.update_transformation_matrix(Transformation.F444W))
        filters_layout.addWidget(button_f444w, 1, 3)

        filters_layout_widget = QWidget()
        filters_layout_widget.setLayout(filters_layout)

        button_reverse_signs = QPushButton('Reverse signs')
        button_reverse_signs.clicked.connect(lambda: self.reverse_signs())

        self.cdelt_input = QLineEdit()
        cdelt = self.canvas.get_cdelt()[1]
        self.cdelt_input.setText(str('%7f' % cdelt))
        cdelt_button = QPushButton("Update cdelt")
        cdelt_button.clicked.connect(lambda: self.update_cdelt())

        cdelt_layout = QHBoxLayout()
        cdelt_layout.addWidget(button_reverse_signs)
        cdelt_layout.addWidget(self.cdelt_input)
        cdelt_layout.addWidget(cdelt_button)

        cdelt_layout_widget = QWidget()
        cdelt_layout_widget.setLayout(cdelt_layout)

        bottom_left_layout = QVBoxLayout()
        bottom_left_layout.addWidget(filters_layout_widget)
        bottom_left_layout.addWidget(cdelt_layout_widget)

        bottom_left_layout_widget = QWidget()
        bottom_left_layout_widget.setLayout(bottom_left_layout)

        main_layout.addWidget(bottom_left_layout_widget, 1, 0)

        self.wcs_header_label = QLabel()
        self.wcs_header_label.setText(self.canvas.primary_header())

        self.rotation_label = QLabel()
        self.rotation_label.setText((self.canvas.calculate_rotation()))

        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(self.wcs_header_label)
        top_right_layout.addWidget(self.rotation_label)

        top_right_layout_widget = QWidget()
        top_right_layout_widget.setLayout(top_right_layout)
        main_layout.addWidget(top_right_layout_widget, 0, 1)

        button_rot90_0_1 = QPushButton('rot90 axes=(0,1)')
        button_rot90_0_1.clicked.connect(lambda: self.rotate_pi_slash_two_0_1())

        button_rot90_1_0 = QPushButton('rot90 axes=(1, 0)')
        button_rot90_1_0.clicked.connect(lambda: self.rotate_pi_slash_two_1_0())

        rot90_layout = QHBoxLayout()
        rot90_layout.addWidget(button_rot90_0_1)
        rot90_layout.addWidget(button_rot90_1_0)

        rot90_layout_widget = QWidget()
        rot90_layout_widget.setLayout(rot90_layout)

        button_flip_left_right = QPushButton('Flip left/right')
        button_flip_left_right.clicked.connect(lambda: self.flip_left_right())

        button_flip_up_down = QPushButton('Flip up/down')
        button_flip_up_down.clicked.connect(lambda: self.flip_up_down())

        flip_layout = QHBoxLayout()
        flip_layout.addWidget(button_flip_left_right)
        flip_layout.addWidget(button_flip_up_down)

        flip_layout_widget = QWidget()
        flip_layout_widget.setLayout(flip_layout)

        button_flip = QPushButton('Flip')
        button_flip.clicked.connect(lambda: self.flip())

        button_roll = QPushButton('Roll')
        button_roll.clicked.connect(lambda: self.roll())

        flip_roll_layout = QHBoxLayout()
        flip_roll_layout.addWidget(button_flip)
        flip_roll_layout.addWidget(button_roll)

        flip_roll_layout_widget = QWidget()
        flip_roll_layout_widget.setLayout(flip_roll_layout)

        self.name_input = QLineEdit()
        self.name_input.setText('Filename')

        button_save = QPushButton('Save image')
        button_save.clicked.connect(lambda:  self.save_image())

        save_layout = QHBoxLayout()
        save_layout.addWidget(self.name_input)
        save_layout.addWidget(button_save)

        save_layout_widget = QWidget()
        save_layout_widget.setLayout(save_layout)

        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.addWidget(rot90_layout_widget)
        bottom_right_layout.addWidget(flip_layout_widget)
        bottom_right_layout.addWidget(flip_roll_layout_widget)
        bottom_right_layout.addWidget(save_layout_widget)

        bottom_right_layout_widget = QWidget()
        bottom_right_layout_widget.setLayout(bottom_right_layout)
        main_layout.addWidget(bottom_right_layout_widget, 1, 1)

        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)

        self.setCentralWidget(main_layout_widget)

        self.show()

    def update_cdelt(self):
        self.canvas.update_cdelt(float(self.cdelt_input.text()))
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def update_transformation_matrix(self, transformation: Transformation):
        self.canvas.update_transformation_matrix(transformation)
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def rotate_pi_slash_two_0_1(self):
        self.canvas.rotate_pi_slash_two_0_1()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def rotate_pi_slash_two_1_0(self):
        self.canvas.rotate_pi_slash_two_1_0()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def flip_left_right(self):
        self.canvas.flip_left_right()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def flip_up_down(self):
        self.canvas.flip_up_down()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def flip(self):
        self.canvas.flip()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def roll(self):
        self.canvas.roll()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def reverse_signs(self):
        self.canvas.reverse_signs()
        self.wcs_header_label.setText(self.canvas.primary_header())
        self.rotation_label.setText((self.canvas.calculate_rotation()))

    def save_image(self):
        self.canvas.figure.savefig(self.name_input.text() + '.png')

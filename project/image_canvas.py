from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from project.image_configuration import ImageConfiguration
from project.ned_data_reader import NedDataReader
from project.transformation import Transformation
import matplotlib

matplotlib.use('QtAgg')


class ImageCanvas(FigureCanvasQTAgg):
    WIDTH = 5
    HEIGHT = 5
    DPI = 100

    def __init__(self, ha: float, dec: float, png: str, ned: str):
        self.image_configuration = ImageConfiguration(ha, dec)
        self.image = np.asarray(Image.open(png))
        self.ned_rows = NedDataReader(ned).extract()

        self.figure = Figure(figsize=(self.WIDTH, self.HEIGHT), dpi=self.DPI)
        self.axes = self.figure.add_subplot(111)
        self.rendered_image = self.axes.imshow(self.image)
        self.axes.add_image(self.rendered_image)

    def update_transformation_matrix(self, transformation: Transformation):
        self.image_configuration.set_transformation_matrix(transformation)
        self.update_image()

    def update_cdelt(self, abs_value: float):
        self.image_configuration.set_cdelt([abs_value * -1, abs_value])
        self.update_image()

    def get_cdelt(self) -> [float, float]:
        return self.image_configuration.get_cdelt()

    def rotate_pi_slash_two_0_1(self):
        self.image_configuration.rotate_pi_slash_two_0_1()
        self.update_image()

    def rotate_pi_slash_two_1_0(self):
        self.image_configuration.rotate_pi_slash_two_1_0()
        self.update_image()

    def primary_header(self) -> str:
        return self.image_configuration.primary_header()

    def update_image(self):
        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        self.rendered_image = self.axes.imshow(self.image)
        self.axes.add_image(self.rendered_image)

        self.set_centre_and_ned_radius()
        self.set_features()
        self.axes.set_axis_off()

        self.draw()

    def load(self):
        self.set_centre_and_ned_radius()
        self.set_features()
        self.axes.set_axis_off()
        super(ImageCanvas, self).__init__(self.figure)

    def set_centre_and_ned_radius(self):
        centre = plt.Circle((self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE),
                            self.image_configuration.MARKER_RADIUS, color='w', fill=False)
        self.rendered_image.axes.add_artist(centre)
        outer_circle = plt.Circle(
            (self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE),
            self.image_configuration.IMAGE_RADIUS, color='w', fill=False)
        self.rendered_image.axes.add_artist(outer_circle)

    def set_features(self):
        record_number = []
        ha = []
        dec = []

        counters = range(1, len(self.ned_rows))

        for counter in counters:
            record_number.append(self.ned_rows[counter][0])
            ha.append(float(self.ned_rows[counter][2]))
            dec.append(float(self.ned_rows[counter][3]))

        x, y = self.image_configuration.convert_sky_coordinates(ha, dec)

        counters = range(len(record_number))

        for counter in counters:
            feature = plt.Circle((x[counter], y[counter]), self.image_configuration.MARKER_RADIUS, color='y',
                                 fill=False)
            self.rendered_image.axes.add_artist(feature)
            self.rendered_image.axes.annotate(record_number[counter], xy=(x[counter], y[counter]),
                                              xytext=(self.image_configuration.LABEL_OFFSET,
                                                      self.image_configuration.LABEL_OFFSET),
                                              textcoords='offset points', color='y')

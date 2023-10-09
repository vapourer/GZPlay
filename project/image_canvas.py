from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from astropy.wcs import WCS
from project.image_configuration import ImageConfiguration
from project.ned_data_reader import NedDataReader
from project.transformation import Transformation
import matplotlib
matplotlib.use('QtAgg')


class ImageCanvas(FigureCanvasQTAgg):
    WIDTH = 5
    HEIGHT = 5
    DPI = 100

    def __init__(self, ha: float, dec: float):
        self.image_configuration = ImageConfiguration(ha, dec)
        self.w = WCS(naxis=2)
        self.w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        self.w.wcs.crpix = [self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE]
        self.w.wcs.crval = [ha, dec]
        self.w.wcs.cdelt = self.image_configuration.CDELT_INITIAL_VALUE
        self.w.wcs.pc = [[self.image_configuration.PC_DEFAULT[0], self.image_configuration.PC_DEFAULT[1]],
                         [self.image_configuration.PC_DEFAULT[2], self.image_configuration.PC_DEFAULT[3]]]

    def set_transformation_matrix(self, pc1_1: float, pc1_2: float, pc2_1: float, pc2_2: float):
        self.w.wcs.pc = [[pc1_1, pc1_2], [pc2_1, pc2_2]]

    def update_transformation_matrix(self, transformation: Transformation):
        matrix = self.image_configuration.PC_DEFAULT

        match transformation:
            case 1:
                matrix = self.image_configuration.PC_DEFAULT
            case 2:
                matrix = self.image_configuration.PC_F115W
            case 3:
                matrix = self.image_configuration.PC_F150W
            case 4:
                matrix = self.image_configuration.PC_F200W
            case 5:
                matrix = self.image_configuration.PC_F277W
            case 6:
                matrix = self.image_configuration.PC_F356W
            case 7:
                matrix = self.image_configuration.PC_F410M
            case 8:
                matrix = self.image_configuration.PC_F444W

        self.w.wcs.pc = [[matrix[0], matrix[1]],
                         [matrix[2], matrix[3]]]

    def set_coordinate_increments(self, cdelt1: float, cdelt2: float):
        self.w.wcs.cdelt = [cdelt1, cdelt2]

    def compare(self, png: str, ned: str):
        fig = Figure(figsize=(self.WIDTH, self.HEIGHT), dpi=self.DPI)

        axes = fig.add_subplot(111)
        image = np.asarray(Image.open(png))
        rendered_image = axes.imshow(image)
        axes.add_image(rendered_image)

        ned_rows = NedDataReader(ned).extract()

        centre = plt.Circle((self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE),
                            self.image_configuration.MARKER_RADIUS, color='w', fill=False)
        rendered_image.axes.add_artist(centre)
        outer_circle = plt.Circle((self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE),
                                  self.image_configuration.IMAGE_RADIUS, color='w', fill=False)
        rendered_image.axes.add_artist(outer_circle)

        record_number = []
        ha = []
        dec = []

        counters = range(1, len(ned_rows))

        for counter in counters:
            record_number.append(ned_rows[counter][0])
            ha.append(float(ned_rows[counter][2]))
            dec.append(float(ned_rows[counter][3]))

        x, y = self.image_configuration.convert_sky_coordinates(ha, dec)

        counters = range(len(record_number))

        for counter in counters:
            feature = plt.Circle((x[counter], y[counter]), self.image_configuration.MARKER_RADIUS, color='y', fill=False)
            rendered_image.axes.add_artist(feature)
            rendered_image.axes.annotate(record_number[counter], xy=(x[counter], y[counter]),
                                         xytext=(self.image_configuration.LABEL_OFFSET, self.image_configuration.LABEL_OFFSET),
                                         textcoords='offset points', color='y')

        axes.set_axis_off()
        super(ImageCanvas, self).__init__(fig)

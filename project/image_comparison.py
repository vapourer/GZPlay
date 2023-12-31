import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from astropy.wcs import WCS
from project.ned_data_reader import NedDataReader
from project.image_configuration import ImageConfiguration


class ImageComparer:

    def __init__(self, ha: float, dec: float):
        self.image_configuration = ImageConfiguration(ha, dec)
        self.w = WCS(naxis=2)
        self.w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        self.w.wcs.crpix = [self.image_configuration.CENTRE_COORDINATE, self.image_configuration.CENTRE_COORDINATE]
        self.w.wcs.crval = [ha, dec]
        self.w.wcs.cdelt = self.image_configuration.CDELT_INITIAL_VALUE
        self.w.wcs.pc = [[self.image_configuration.PC_DEFAULT[0], self.image_configuration.PC_DEFAULT[1]],
                         [self.image_configuration.PC_DEFAULT[2], self.image_configuration.PC_DEFAULT[3]]]

    def compare(self, png: str, ned: str):
        image = np.asarray(Image.open(png))
        rendered_image = plt.imshow(image)

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

        plt.axis('off')
        plt.show()

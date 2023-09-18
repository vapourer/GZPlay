import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from astropy.wcs import WCS
import csv


class ImageComparer:
    ORIGIN = 0
    CENTRE_COORDINATE = 249
    IMAGE_RADIUS = 250
    MARKER_RADIUS = 10
    LABEL_OFFSET = 5
    PC1_1 = 0.6498658740531003
    PC1_2 = -0.7600489100980279
    PC2_1 = -0.7600489100980279
    PC2_2 = -0.6498658740531003
    # CDELT = [-0.000004, 0.000004]
    CDELT = [-0.0000028, 0.0000028]

    # PC1_1 = 0.6498658740531003 / 1.5
    # PC1_2 = -0.7600489100980279 / 1.5
    # PC2_1 = -0.7600489100980279 / 1.5
    # PC2_2 = -0.6498658740531003 / 1.5
    # CDELT = [-0.000005, 0.000005]

    # PC1_1 = 0.6498658740531003 * 87 / 250
    # PC1_2 = -0.7600489100980279 * 87 / 250
    # PC2_1 = -0.7600489100980279 * 87 / 250
    # PC2_2 = -0.6498658740531003 * 87 / 250
    # CDELT = [-0.000004 * 87 / 250, 0.000004* 87 / 250]

    # PC1_1 = 0.64988103732628
    # PC1_2 = 0.76003594475769
    # PC2_1 = 0.7600359447576
    # PC2_2 = -0.64988103732628
    # CDELT = [1.7473243234539e-05, 1.7473243234539e-05]

    # PC1_1 = -0.65115906238239
    # PC1_2 = -0.75894128592223
    # PC2_1 = -0.75894128592223
    # PC2_2 = 0.65115906238239
    # CDELT = [1.7476196475944e-05, 1.7476196475944e-05]
    #
    # PC1_1 = -0.65126480057247
    # PC1_2 = -0.75885055151545
    # PC2_1 = -0.75885055151545
    # PC2_2 = 0.65126480057247
    # CDELT = [1.7474963270928e-05, 1.7474963270928e-05]

    # def __init__(self, ha: float, dec: float, fits: str):
    #     self.w = WCS(naxis=2)
    #     self.w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
    #     self.w.wcs.crpix = [self.CENTRE_COORDINATE, self.CENTRE_COORDINATE]
    #     self.w.wcs.crval = [ha, dec]
    #     self.w.wcs.cdelt = [-0.000004, 0.000004]
    #     self.w.wcs.pc = [[self.PC1_1, self.PC1_2], [self.PC2_1, self.PC2_2]]

    def __init__(self, ha: float, dec: float):
        self.w = WCS(naxis=2)
        self.w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        self.w.wcs.crpix = [self.CENTRE_COORDINATE, self.CENTRE_COORDINATE]
        self.w.wcs.crval = [ha, dec]
        self.w.wcs.cdelt = self.CDELT
        self.w.wcs.pc = [[self.PC1_1, self.PC1_2], [self.PC2_1, self.PC2_2]]

    def convert_sky_coordinates(self, ha: [float], dec: [float]) -> np.ndarray:
        return self.w.wcs_world2pix(ha, dec, self.ORIGIN)

    def primary_header(self):
        print(self.w)

    # The following function supplied by Claude Cornen,
    # who also advised on the WCS configuration.
    # See https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/talk/1267/2992080?comment=5038565
    def calculate_rotation(self):
        determinant = (self.PC1_1 * self.PC2_2) - (self.PC1_2 * self.PC2_1)

        signed_unit = 1.0

        if determinant < 0.0:
            signed_unit = -1.0

        rot1_cd = math.atan2(-self.PC2_1, signed_unit * self.PC1_1)
        rot2_cd = math.atan2(signed_unit * self.PC1_2, self.PC2_2)
        rot_av = (rot1_cd + rot2_cd) / 2.0
        crota_cd = math.degrees(rot_av)
        skew = math.degrees(abs(rot1_cd - rot2_cd))

        print('Orientation degrees:', crota_cd, 'skew:', skew, sep='\t')

    def compare(self, png: str, ned: str):
        image = np.asarray(Image.open(png))
        rendered_image = plt.imshow(image)

        ned_rows = []

        with open(ned, newline='') as csvfile:
            ned_reader = csv.reader(csvfile, delimiter=',')

            for row in ned_reader:
                ned_rows.append(row)

        centre = plt.Circle((self.CENTRE_COORDINATE, self.CENTRE_COORDINATE), self.MARKER_RADIUS, color='w', fill=False)
        rendered_image.axes.add_artist(centre)
        outer_circle = plt.Circle((self.CENTRE_COORDINATE, self.CENTRE_COORDINATE), self.IMAGE_RADIUS, color='w', fill=False)
        rendered_image.axes.add_artist(outer_circle)

        record_number = []
        ha = []
        dec = []

        counters = range(1, len(ned_rows))

        for counter in counters:
            record_number.append(ned_rows[counter][0])
            ha.append(float(ned_rows[counter][2]))
            dec.append(float(ned_rows[counter][3]))

        x, y = self.convert_sky_coordinates(ha, dec)

        counters = range(len(record_number))

        for counter in counters:
            feature = plt.Circle((x[counter], y[counter]), self.MARKER_RADIUS, color='y', fill=False)
            rendered_image.axes.add_artist(feature)
            rendered_image.axes.annotate(record_number[counter], xy=(x[counter], y[counter]), xytext=(self.LABEL_OFFSET, self.LABEL_OFFSET), textcoords='offset points', color='y')

        plt.axis('off')
        plt.show()


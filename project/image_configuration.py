import math
import numpy as np
from astropy.wcs import WCS


class ImageConfiguration:
    ORIGIN = 0
    CENTRE_COORDINATE = 249
    IMAGE_RADIUS = 250
    MARKER_RADIUS = 10
    LABEL_OFFSET = 5

    # F115W
    # F150W
    # F200W
    # F277W
    # F356W
    # F410M
    # F444W

    PC_DEFAULT = [0.6498658740531003, -0.7600489100980279, -0.7600489100980279, -0.6498658740531003]
    PC_F115W = [0.6431047847515428, 0.7657781897061785, 0.7657781897061785, -0.6431047847515428]
    PC_F150W = [0.6431011065157383, 0.76578127869401, 0.76578127869401, -0.6431011065157383]
    PC_F200W = [0.6431035354104004, 0.7657792389080836, 0.7657792389080836, -0.6431035354104004]
    PC_F277W = [0.6498855848167091, 0.7600320563288394, 0.7600320563288394, -0.6498855848167091]
    PC_F356W = [0.6498829221367624, 0.7600343331159343, 0.7600343331159343, -0.6498829221367624]
    PC_F410M = [0.6498819340851529, 0.7600351779685866, 0.7600351779685866, -0.6498819340851529]
    PC_F444W = [0.6498843448164907, 0.7600331166221908, 0.7600331166221908, -0.6498843448164907]
    CDELT_INITIAL_VALUE = [-0.0000015, 0.0000015]

    def __init__(self, ha: float, dec: float):
        self.w = WCS(naxis=2)
        self.w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        self.w.wcs.crpix = [self.CENTRE_COORDINATE, self.CENTRE_COORDINATE]
        self.w.wcs.crval = [ha, dec]
        self.w.wcs.cdelt = self.CDELT_INITIAL_VALUE
        self.w.wcs.pc = [[self.PC_DEFAULT[0], self.PC_DEFAULT[1]],
                         [self.PC_DEFAULT[2], self.PC_DEFAULT[3]]]

    def update_transformation_matrix(self, matrix: list[float]):
        self.w.wcs.pc = [[matrix[0], matrix[1]],
                         [matrix[2], matrix[3]]]

    def convert_sky_coordinates(self, ha: [float], dec: [float]) -> np.ndarray:
        return self.w.wcs_world2pix(ha, dec, self.ORIGIN)

    def primary_header(self):
        print(self.w)

    # The following function supplied by Claude Cornen,
    # who also advised on the WCS configuration.
    # See https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/talk/1267/2992080?comment=5038565
    def calculate_rotation(self):
        determinant = (self.PC_DEFAULT[0] * self.PC_DEFAULT[3]) - (
                self.PC_DEFAULT[1] * self.PC_DEFAULT[2])

        signed_unit = 1.0

        if determinant < 0.0:
            signed_unit = -1.0

        rot1_cd = math.atan2(-self.PC_DEFAULT[2], signed_unit * self.PC_DEFAULT[0])
        rot2_cd = math.atan2(signed_unit * self.PC_DEFAULT[1], self.PC_DEFAULT[3])
        rot_av = (rot1_cd + rot2_cd) / 2.0
        crota_cd = math.degrees(rot_av)
        skew = math.degrees(abs(rot1_cd - rot2_cd))

        print('Orientation degrees:', crota_cd, 'skew:', skew, sep='\t')
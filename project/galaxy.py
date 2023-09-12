import math
from project.degrees_radians_converter import DegreesRadiansConverter


class Galaxy:
    SPEED_OF_LIGHT = 299792458

    def __init__(self, ra: float, dec: float, z: float):
        converter = DegreesRadiansConverter()
        self.__ra = converter.convert_degrees_to_radians(ra)
        self.__dec = (math.pi / 2) - converter.convert_degrees_to_radians(dec)
        self.__z = z

    def ra(self) -> float:
        return self.__ra

    def dec(self) -> float:
        return self.__dec

    def z(self) -> float:
        return self.__z

    def velocity(self) -> float:
        return self.__z * self.SPEED_OF_LIGHT

import math
from project.galaxy import Galaxy


class GalaxySeparationCalculator:

    def __init__(self, galaxy1: Galaxy, galaxy2: Galaxy, hubble: float):
        self.__galaxy1 = galaxy1
        self.__galaxy2 = galaxy2
        self.__h = hubble

    def angle(self) -> float:
        cos_dec_g1 = math.cos(self.__galaxy1.dec())
        sin_dec_g1 = math.sin(self.__galaxy1.dec())
        cos_dec_g2 = math.cos(self.__galaxy2.dec())
        sin_dec_g2 = math.sin(self.__galaxy2.dec())
        cos_ra_g1_g2 = math.cos(self.__galaxy1.ra() - self.__galaxy2.ra())
        return math.acos(cos_dec_g1 * cos_dec_g2 + sin_dec_g1 * sin_dec_g2 * cos_ra_g1_g2)

    def distance(self) -> float:
        return (8 / math.pi) * math.sqrt(self.__galaxy1.velocity() * self.__galaxy2.velocity()) * math.sin(
            self.angle() / 2) / self.__h

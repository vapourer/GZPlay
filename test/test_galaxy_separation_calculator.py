from project.galaxy import Galaxy
from project.galaxy_separation_calculator import GalaxySeparationCalculator
import pytest

class TestGalaxySeparationCalculator:

    HUBBLE = 67.8

    def test_angle(self):
        # Arrange
        expected_angle = 0.00069937       
        g_calculator = self.__create_calculator()
        
        # Act
        actual_angle = round(g_calculator.angle(), 8)
        
        # Assert
        assert expected_angle == actual_angle
        
    def test_distance(self):
        # Arrange
        expected_distance = 14.823295
        g_calculator = self.__create_calculator()
        
        # Act
        actual_distance = round(g_calculator.distance(), 6)
        
        # Assert
        assert expected_distance == actual_distance
        
    def __create_calculator(self) -> GalaxySeparationCalculator:
        g1 = Galaxy(185.426987, 14.597761, 0.00372)
        g2 = Galaxy(185.3864907979321, 14.6061267510547, 0.00381)
        return GalaxySeparationCalculator(g1, g2, self.HUBBLE)
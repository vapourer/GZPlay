class BrtFacCalculator:

    MULTIPLICATIVE_IDENTITY = 1.0
    MAGNITUDE_LOWER_THRESHOLD = 19
    BRTFAC_POLYNOMIAL_COEFFICIENT_1 = -0.0125
    BRTFAC_POLYNOMIAL_COEFFICIENT_2 = 0.5875
    BRTFAC_POLYNOMIAL_CONSTANT = -5.65
    MAX_BRTFAC = 1.25
    MAX_RFAC = 0.0
    MIN_RFAC = -0.17
    MAGNITUDE_UPPER_THRESHOLD = 21
    RFAC_POLYNOMIAL_COEFFICIENT_1 = 0.00035
    RFAC_POLYNOMIAL_COEFFICIENT_2 = -0.0055
    RFAC_POLYNOMIAL_CONSTANT = -0.15

    def __init__(self, mag_select: float, radius_select: float):
        self.mag_select = mag_select
        self.radius_select = radius_select
        
    def calculate(self) -> float:
        brtfac = self.MULTIPLICATIVE_IDENTITY
        
        if self.mag_select > self.MAGNITUDE_LOWER_THRESHOLD:
            brtfac = self.BRTFAC_POLYNOMIAL_COEFFICIENT_1 * (self.mag_select)**2 + self.BRTFAC_POLYNOMIAL_COEFFICIENT_2 * self.mag_select + self.BRTFAC_POLYNOMIAL_CONSTANT
            brtfac = min([brtfac, self.MAX_BRTFAC])
            
        rfac = self.MAX_RFAC
        
        if self.mag_select <= self.MAGNITUDE_UPPER_THRESHOLD:
            rfac = self.RFAC_POLYNOMIAL_COEFFICIENT_1 * (self.radius_select)**2 + self.RFAC_POLYNOMIAL_COEFFICIENT_2 * self.radius_select + self.RFAC_POLYNOMIAL_CONSTANT            
            rfac = max([self.MIN_RFAC, min([rfac, self.MAX_RFAC])])        
            brtfac += rfac
        
        return max([self.MULTIPLICATIVE_IDENTITY, min([brtfac, self.MAX_BRTFAC])])

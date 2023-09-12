class PixRadCalculator:
    
    MAGFAC_THRESHOLD = 22
    RADIUS_MULTIPLIER = 30
    RATIO_EXPONENT = 0.4
    MAGNITUDE_MULTIPLIER = 7
    MAX_MAG_SELECT = 17
    ADDITIVE_IDENTITY = 0
    MULTIPLICATIVE_IDENTITY = 1

    def __init__(self, flux_rad_0p50: float, flux_rad_0p99: float, mag_select: float, radius_select: float):
        self.flux_rad_0p50 = flux_rad_0p50
        self.flux_rad_0p99 = flux_rad_0p99
        self.mag_select = mag_select
        self.radius_select = radius_select
        
    def calculate(self) -> float:
        r_ratio = 1
    
        if self.flux_rad_0p50 > 0:
            r_ratio = self.flux_rad_0p99 / self.flux_rad_0p50
            
        magfac = max([self.ADDITIVE_IDENTITY, self.mag_select - self.MAGFAC_THRESHOLD])
        
        pixrad = self.RADIUS_MULTIPLIER * self.radius_select * max([r_ratio**self.RATIO_EXPONENT, self.MULTIPLICATIVE_IDENTITY]) - self.MAGNITUDE_MULTIPLIER * magfac
        
        if self.mag_select <= self.MAX_MAG_SELECT:
            pixrad *= 2
            
        return pixrad

class ArcSecondConverter:

    PIXEL_SCALE = 0.031
    SECONDS_IN_MINUTES = 60

    def __init__(self, pixrad: float):
        self.pixrad = pixrad
        
    def convert_pixrad(self) -> float:
        return self.pixrad * self.PIXEL_SCALE

    def convert_pixrad_arcminutes(self) -> float:
        return self.pixrad * self.PIXEL_SCALE / self.SECONDS_IN_MINUTES
        
    def convert(self, pix: float) -> float:
        return pix * self.PIXEL_SCALE
    
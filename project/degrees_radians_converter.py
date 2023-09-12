import math

class DegreesRadiansConverter:
    
    SEMICIRCLE = 180
    
    def __init__(self):
        pass
        
    def convert_degrees_to_radians(self, degrees: float) -> float:
        return math.pi * degrees / self.SEMICIRCLE
        
    def convert_radians_to_degrees(self, radians: float) -> float:
        return self.SEMICIRCLE * radians / math.pi
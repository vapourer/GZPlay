import argparse
from project.pixrad_calculator import PixRadCalculator
from project.brtfac_calculator import BrtFacCalculator
from project.arcsecond_converter import ArcSecondConverter


# Realisation of Brooke Simmons' pseudocode for processing GZ metadata,
# from https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/talk/1269/2979734?comment=4894623
def calculate(flux_rad_0p50, flux_rad_0p95, flux_rad_0p99, mag_select, radius_select):
    print('Input')
    print('flux_rad_0p50: ' + flux_rad_0p50)
    print('flux_rad_0p95: ' + flux_rad_0p95)
    print('flux_rad_0p99: ' + flux_rad_0p99)
    print('mag_select: ' + mag_select)
    print('radius_select: ' + radius_select)
    print()

    print('Output')

    pixrad = PixRadCalculator(float(flux_rad_0p50), float(flux_rad_0p99), float(mag_select),
                              float(radius_select)).calculate()
    arc_second_converter = ArcSecondConverter(pixrad)

    print('pixrad: ' + str(pixrad))
    print('brtfac: ' + str(BrtFacCalculator(float(mag_select), float(radius_select)).calculate()))
    print('pixrad converted to arcseconds: ' + str(arc_second_converter.convert_pixrad()))
    print('flux_rad_0p50 converted to arcseconds: ' + str(arc_second_converter.convert(float(flux_rad_0p50))))
    print('flux_rad_0p95 converted to arcseconds: ' + str(arc_second_converter.convert(float(flux_rad_0p95))))
    print('flux_rad_0p99 converted to arcseconds: ' + str(arc_second_converter.convert(float(flux_rad_0p99))))


parser = argparse.ArgumentParser()

parser.add_argument("flux_rad_0p50")
parser.add_argument("flux_rad_0p95")
parser.add_argument("flux_rad_0p99")
parser.add_argument("mag_select")
parser.add_argument("radius_select")

args = parser.parse_args()

calculate(args.flux_rad_0p50, args.flux_rad_0p95, args.flux_rad_0p99, args.mag_select, args.radius_select)

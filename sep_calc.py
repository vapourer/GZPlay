from project.galaxy import Galaxy
from project.galaxy_separation_calculator import GalaxySeparationCalculator
from project.degrees_radians_converter import DegreesRadiansConverter


def invite_input(invite: str) -> float:
    value = 0.00
    correct = False

    while not correct:
        value_as_string = input(invite)

        if value_as_string.replace('.', '').isnumeric():
            value = float(value_as_string)
            correct = True

    return value


# After advice from Claude Cornen.
# See https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/talk/1269/716582?comment=1401233
# Realisation of Equation 4 from https://adsabs.harvard.edu/full/1992A%26A...255...69G
def calculate():
    kpc_to_ly = 3261.5638
    g1_ra = invite_input('Galaxy 1 RA: ')
    g1_dec = invite_input('Galaxy 1 Dec: ')
    g1_z = invite_input('Galaxy 1 redshift (z): ')
    g2_ra = invite_input('Galaxy 2 RA: ')
    g2_dec = invite_input('Galaxy 2 Dec: ')
    g2_z = invite_input('Galaxy 2 redshift (z): ')
    hubble = invite_input('Hubble value: ')

    g1 = Galaxy(g1_ra, g1_dec, g1_z)
    g2 = Galaxy(g2_ra, g2_dec, g2_z)
    gcal = GalaxySeparationCalculator(g1, g2, hubble)
    gcal_radians = gcal.angle()
    gcal_degrees = DegreesRadiansConverter().convert_radians_to_degrees(gcal_radians)
    gcal_minutes = gcal_degrees * 60
    gcal_seconds = gcal_minutes * 60
    gcal_kpc = gcal.distance()
    gcal_ly = gcal_kpc * kpc_to_ly

    print()
    print('Angular separation (radians): ' + str(round(gcal_radians, 9)))
    print('Angular separation (degrees): ' + str(round(gcal_degrees, 3)))
    print('Angular separation (minutes): ' + str(round(gcal_minutes, 3)))
    print('Angular separation (seconds): ' + str(round(gcal_seconds, 3)))
    print('Separation (R): ' + str(round(gcal_kpc, 2)) + ' Kpc = ' + str(int(round(gcal_ly, 0))) + ' ly')


calculate()

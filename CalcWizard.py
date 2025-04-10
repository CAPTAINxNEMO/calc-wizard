# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QInputDialog
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
# Mathematical Functions
from math import sin, cos, tan, asin, acos, atan, radians, pi, e, log, log2, log10
# For API request
from requests import get
# Icon Check
import sys
from os.path import dirname, abspath, join
# API Key Check
from os import environ

if getattr(sys, 'frozen', False):
    baseDir = sys._MEIPASS # type: ignore
else:
    baseDir = dirname(abspath(__file__))
iconPath = join(baseDir, 'CalcWizardIcon.ico')

calculatorInput = ''
currencyConversionInput = ''
lengthConversionInput = ''
areaConversionInput = ''
volumeConversionInput = ''
weightConversionInput = ''
temperatureConversionInput = ''
speedConversionInput = ''
pressureConversionInput = ''
powerConversionInput = ''

API_KEY = environ.get('CW_CURRENCY_API_KEY')

def saveAPI(key):
    global API_KEY
    API_KEY = key
    environ['CW_CURRENCY_API_KEY'] = key
    try:
        from subprocess import run
        run(['setx', 'CW_CURRENCY_API_KEY', key], check = False, capture_output = True)
    except Exception as e:
        warningMessageBox = QMessageBox()
        warningMessageBox.setWindowIcon(QIcon(iconPath))
        warningMessageBox.setIcon(QMessageBox.Icon.Warning)
        warningMessageBox.setWindowTitle('Warning')
        warningMessageBox.setText(f'Could not save API key to system environment: {e}')
        warningMessageBox.exec()

lengthConversionFactors = {
    # Metre (m)
    (0, 0): 1, (0, 1): 1000, (0, 2): 100, (0, 3): 10, (0, 4): 0.001, (0, 5): 1000000, (0, 6): 1000000000, (0, 7): 1000000000000, (0, 8): (5000 / 127), (0, 9): (1250 / 381), (0, 10): (1250 / 1143), (0, 11): (125 / 201168), (0, 12): (1 / 1852),
    # Millimetre (mm)
    (1, 0): 0.001, (1, 1): 1, (1, 2): 0.1, (1, 3): 0.01, (1, 4): 0.000001, (1, 5): 1000, (1, 6): 1000000, (1, 7): 1000000000, (1, 8): (5 / 127), (1, 9): (5 / 1524), (1, 10): (5 / 4572), (1, 11): (1 / 1609344), (1, 12): (1 / 1852000),
    # Centimetre (cm)
    (2, 0): 0.01, (2, 1): 10, (2, 2): 1, (2, 3): 0.1, (2, 4): 0.00001, (2, 5): 10000, (2, 6): 10000000, (2, 7): 10000000000, (2, 8): (50 / 127), (2, 9): (25 / 762), (2, 10): (25 / 2286), (2, 11): (5 / 804672), (2, 12): (1 / 185200),
    # Decimetre (dm)
    (3, 0): 0.1, (3, 1): 100, (3, 2): 10, (3, 3): 1, (3, 4): 0.0001, (3, 5): 100000, (3, 6): 100000000, (3, 7): 100000000000, (3, 8): (500 / 127), (3, 9): (125 / 381), (3, 10): (125 / 1143), (3, 11): (25 / 402336), (3, 12): (1 / 18520),
    # Kilometre (km)
    (4, 0): 1000, (4, 1): 1000000, (4, 2): 100000, (4, 3): 10000, (4, 4): 1, (4, 5): 1000000000, (4, 6): 1000000000000, (4, 7): 1000000000000000, (4, 8): (5000000 / 127), (4, 9): (1250000 / 381), (4, 10): (1250000 / 1143), (4, 11): (15625 / 25146), (4, 12): (250 / 463),
    # Micrometre (μm)
    (5, 0): 0.000001, (5, 1): 0.001, (5, 2): 0.0001, (5, 3): 0.00001, (5, 4): 0.000000001, (5, 5): 1, (5, 6): 1000, (5, 7): 1000000, (5, 8): (1 / 25400), (5, 9): (1 / 304800), (5, 10): (1 / 914400), (5, 11): (1 / 1609344000), (5, 12): (1 / 1852000000),
    # Nanometre (nm)
    (6, 0): 0.000000001, (6, 1): 0.000001, (6, 2): 0.0000001, (6, 3): 0.00000001, (6, 4): 0.000000000001, (6, 5): 0.001, (6, 6): 1, (6, 7): 1000, (6, 8): (1 / 25400000), (6, 9): (1 / 304800000), (6, 10): (1 / 914400000), (6, 11): (1 / 1609344000000), (6, 12): (1 / 1852000000000),
    # Picometre (pm)
    (7, 0): 0.000000000001, (7, 1): 0.000000001, (7, 2): 0.0000000001, (7, 3): 0.00000000001, (7, 4): 0.000000000000001, (7, 5): 0.000001, (7, 6): 0.001, (7, 7): 1, (7, 8): (1 / 25400000000), (7, 9): (1 / 304800000000), (7, 10): (7 / 914400000000), (7, 11): (1 / 1609344000000000), (7, 12): (1 / 1852000000000000),
    # Inch (in)
    (8, 0): 0.0254, (8, 1): 25.4, (8, 2): 2.54, (8, 3): 0.254, (8, 4): 0.0000254, (8, 5): 25400, (8, 6): 25400000, (8, 7): 25400000000, (8, 8): 1, (8, 9): (1 / 12), (8, 10): (1 / 36), (8, 11): (3 / 1760), (8, 12): (9260000 / 127),
    # Foot (ft)
    (9, 0): 0.3048, (9, 1): 304.8, (9, 2): 30.48, (9, 3): 3.048, (9, 4): 0.0003048, (9, 5): 304800, (9, 6): 304800000, (9, 7): 304800000000, (9, 8): 12, (9, 9): 1, (9, 10): (1 / 3), (9, 11): (3 / 1760), (9, 12): (2315000 / 381),
    # Yard (yd)
    (10, 0): 0.9144, (10, 1): 914.4, (10, 2): 91.44, (10, 3): 9.144, (10, 4): 0.0009144, (10, 5): 914400, (10, 6): 914400000, (10, 7): 914400000000, (10, 8): 36, (10, 9): 3, (10, 10): 1, (10, 11): (1 / 1760), (10, 12): (2315000 / 1143),
    # Mile (mi)
    (11, 0): 1609.344, (11, 1): 1609344, (11, 2): 160934.4, (11, 3): 16093.44, (11, 4): 1.609344, (11, 5): 1609344000, (11, 6): 1609344000000, (11, 7): 1609344000000000, (11, 8): (440 / 9), (11, 9): (1760 / 3), (11, 10): 1760, (11, 11): 1, (11, 12): (57875 / 50292),
    # Nautical Mile (nmi)
    (12, 0): 1852, (12, 1): 1852000, (12, 2): 18520000, (12, 3): 185200000, (12, 4): 1.852, (12, 5): 1852000000, (12, 6): 1852000000000, (12, 7): 1852000000000000, (12, 8): (127 / 9260000), (12, 9): (381 / 2315000), (12, 10): (1143 / 2315000), (12, 11): (50292 / 57875), (12, 12): 1
}
areaConversionFactors = {
    # Square Metre (m²)
    (0, 0): 1, (0, 1): 100, (0, 2): 10000, (0, 3): 1000000, (0, 4): 0.000001, (0, 5): 1550.0031, (0, 6): (5166677 / 480000), (0, 7): (5166677 / 13381632000000), (0, 8): (5166677 / 20908800000), (0, 9): 0.0001,
    # Square Decimetre (dm²)
    (1, 0): 0.01, (1, 1): 1, (1, 2): 100, (1, 3): 10000, (1, 4): 0.00000001, (1, 5): 15.500031, (1, 6): (5166677 / 48000000), (1, 7): (5166677 / 1338163200000000), (1, 8): (5166677 / 2090880000000), (1, 9): 0.000001,
    # Square Centimetre (cm²)
    (2, 0): 0.0001, (2, 1): 0.01, (2, 2): 1, (2, 3): 100, (2, 4): 0.0000000001, (2, 5): 0.5166677, (2, 6): (5166677 / 4800000000), (2, 7): (5166677 / 133816320000000000), (2, 8): (5166677 / 209088000000000), (2, 9): 0.00000001,
    # Square Millimetre (mm²)
    (3, 0): 0.000001, (3, 1): 0.0001, (3, 2): 0.01, (3, 3): 1, (3, 4): 0.000000000001, (3, 5): 0.005166677, (3, 6): (5166677 / 480000000000), (3, 7): (5166677 / 13381632000000000000), (3, 8): (5166677 / 20908800000000000), (3, 9): 0.0000000001,
    # Square Kilometre (km²)
    (4, 0): 1000000, (4, 1): 100000000, (4, 2): 10000000000, (4, 3): 1000000000000, (4, 4): 1, (4, 5): 516667700, (4, 6): (5166677 / 48), (4, 7): (5166677 / 13381632), (4, 8): (51666770 / 209088), (4, 9): 100,
    # Square Inch (in²)
    (5, 0): (10000 / 5166677), (5, 1): (1000000 / 5166677), (5, 2): (100000000 / 5166677), (5, 3): (10000000000 / 5166677), (5, 4): (1 / 516667700), (5, 5): 1, (5, 6): (1 / 144), (5, 7): (1 / 1338163200), (5, 8): (1 / 2090880), (5, 9): (1 / 5166677),
    # Square Foot (ft²)
    (6, 0): (480000 / 5166677), (6, 1): (48000000 / 5166677), (6, 2): (4800000000 / 5166677), (6, 3): (480000000000 / 5166677), (6, 4): (48 / 516667700), (6, 5): 144, (6, 6): 1, (6, 7): (1 / 27878400), (6, 8): (1 / 43560), (6, 9): (48 / 5166677),
    # Square Mile (mi²)
    (7, 0): (13381632000000 / 5166677), (7, 1): (1338163200000000 / 5166677), (7, 2): (133816320000000000 / 5166677), (7, 3): (13381632000000000000 / 5166677), (7, 4): (13381632 / 5166677), (7, 5): 1338163200, (7, 6): 27878400, (7, 7): 1, (7, 8): 640, (7, 9): (1338163200 / 5166677),
    # Acre (ac)
    (8, 0): (20908800000 / 5166677), (8, 1): (2090880000000 / 5166677), (8, 2): (209088000000000 / 5166677), (8, 3): (20908800000000000 / 5166677), (8, 4): (209088 / 51666770), (8, 5): 2090880, (8, 6): 43560, (8, 7): (1 / 640), (8, 8): 1, (8, 9): (2090880 / 5166677),
    # Hectare (ha)
    (9, 0): 10000, (9, 1): 1000000, (9, 2): 100000000, (9, 3): 10000000000, (9, 4): 0.01, (9, 5): 5166677, (9, 6): (5166677 / 48), (9, 7): (5166677 / 1338163200), (9, 8): (5166677 / 2090880), (9, 9): 1
}
volumeConversionFactors = {
    # Cubic Metre (m³)
    (0, 0): 1, (0, 1): 1000, (0, 2): 1000000, (0, 3): 1000000000, (0, 4): 1000, (0, 5): 1000000, (0, 6): (125000000000 / 2048383), (0, 7): (1953125000 / 55306341), (0, 8): (16000000000 / 454609), (0, 9): (100000000 / 454609),
    # Cubic Decimetre (dm³)
    (1, 0): 0.001, (1, 1): 1, (1, 2): 1000, (1, 3): 1000000, (1, 4): 1, (1, 5): 1000, (1, 6): (125000000 / 2048383), (1, 7): (1953125 / 55306341), (1, 8): (16000000 / 454609), (1, 9): (100000 / 454609),
    # Cubic Centimetre (cm³)
    (2, 0): 0.000001, (2, 1): 0.001, (2, 2): 1, (2, 3): 1000, (2, 4): 0.001, (2, 5): 1, (2, 6): (125000 / 2048383), (2, 7): (15625 / 442450728), (2, 8): (16000 / 454609), (2, 9): (100 / 454609),
    # Cubic Millimetre (mm³)
    (3, 0): 0.000000001, (3, 1): 0.000001, (3, 2): 0.001, (3, 3): 1, (3, 4): 0.000001, (3, 5): 0.001, (3, 6): (125 / 2048383), (3, 7): (125 / 3539605824), (3, 8): (16 / 454609), (3, 9): (1 / 4546090),
    # Litre (L)
    (4, 0): 0.001, (4, 1): 1, (4, 2): 1000, (4, 3): 1000000, (4, 4): 1, (4, 5): 1000, (4, 6): (125000000 / 2048383), (4, 7): (1953125 / 55306341), (4, 8): (16000000 / 454609), (4, 9): (100000 / 454609),
    # Millilitre (mL)
    (5, 0): 0.000001, (5, 1): 0.001, (5, 2): 1, (5, 3): 1000, (5, 4): 0.001, (5, 5): 1, (5, 6): (125000 / 2048383), (5, 7): (15625 / 442450728), (5, 8): (16000 / 454609), (5, 9): (100 / 454609),
    # Cubic Inch (in³)
    (6, 0): 0.000016387064, (6, 1): 0.016387064, (6, 2): 016.387064, (6, 3): 016387.064, (6, 4): 0.016387064, (6, 5): 016.387064, (6, 6): 1, (6, 7): (1/ 1728), (6, 8): (32774128 / 56826125), (6, 9): (2048383 / 568261250),
    # Cubic Foot (ft³)
    (7, 0): 0.028316846592, (7, 1): 28.316846592, (7, 2): 28316.846592, (7, 3): 28316846.592, (7, 4): 28.316846592, (7, 5): 28316.846592, (7, 6): 1728, (7, 7): 1, (7, 8): (56633693184 / 56826125), (7, 9): (1769802912 / 284130625),
    # Fluid Ounce (fl. oz)
    (8, 0): 0.0000284130625, (8, 1): 0.0284130625, (8, 2): 28.4130625, (8, 3): 28413.0625, (8, 4): 0.0284130625, (8, 5): 28.4130625, (8, 6): (56826125 / 32774128), (8, 7): (56826125 / 56633693184), (8, 8): 1, (8, 9): 0.00625,
    # Gallon (gal)
    (9, 0): 0.00454609, (9, 1): 4.54609, (9, 2): 4546.09, (9, 3): 4546090, (9, 4): 4.54609, (9, 5): 4546.09, (9, 6): (568261250 / 2048383), (9, 7): (284130625 / 1769802912), (9, 8): 160, (9, 9): 1
}
weightConversionFactors = {
    # Gram (g)
    (0, 0): 1, (0, 1): 0.001, (0, 2): 1000, (0, 3): 0.000001, (0, 4): 0.00001, (0, 5): 5, (0, 6): (1600000 / 45359237), (0, 7): (100000 / 45359237), (0, 8): (700000 / 317514659),
    # Kilogram (kg)
    (1, 0): 1000, (1, 1): 1, (1, 2): 1000000, (1, 3): 0.001, (1, 4): 0.01, (1, 5): 5000, (1, 6): (1600000000 / 45359237), (1, 7): (100000000 / 45359237), (1, 8): (700000000 / 317514659),
    # Milligram (mg)
    (2, 0): 0.001, (2, 1): 0.000001, (2, 2): 1, (2, 3): 0.000000001, (2, 4): 0.00000001, (2, 5): 0.0005, (2, 6): (1600 / 45359237), (2, 7): (100 / 45359237), (2, 8): (700 / 317514659),
    # Tonne (t)
    (3, 0): 1000000, (3, 1): 1000, (3, 2): 1000000000, (3, 3): 1, (3, 4): 10, (3, 5): 5000000, (3, 6): (1600000000000 / 45359237), (3, 7): (100000000000 / 45359237), (3, 8): (700000000000 / 317514659),
    # Quintal (q)
    (4, 0): 100000, (4, 1): 100, (4, 2): 100000000, (4, 3): 0.1, (4, 4): 1, (4, 5): 500000, (4, 6): (160000000000 / 45359237), (4, 7): (10000000000 / 45359237), (4, 8): (70000000000 / 317514659),
    # Carat (ct)
    (5, 0): 0.2, (5, 1): 0.0002, (5, 2): 200, (5, 3): 0.0000002, (5, 4): 0.000002, (5, 5): 1, (5, 6): (320000 / 45359237), (5, 7): (20000 / 45359237), (5, 8): (140000 / 317514659),
    # Ounce (oz)
    (6, 0): 28.349523125, (6, 1): 0.028349523125, (6, 2): 28349.523125, (6, 3): 0.000028349523125, (6, 4): 0.00028349523125, (6, 5): (45359237 / 320000), (6, 6): 1, (6, 7): (1 / 16), (6, 8): (1 / 224),
    # Pound (lb)
    (7, 0): 453.59237, (7, 1): 0.45359237, (7, 2): 453592.37, (7, 3): 0.00045359237, (7, 4): 0.0045359237, (7, 5): 2267.96185, (7, 6): 16, (7, 7): 1, (7, 8): (1 / 14),
    # Stone (st)
    (8, 0): (317514659 / 700000), (8, 1): (317514659 / 700000000), (8, 2): (317514659 / 700), (8, 3): (317514659 / 700000000000), (8, 4): (317514659 / 70000000000), (8, 5): (317514659 / 140000), (8, 6): 224, (8, 7): 14, (8, 8): 1
}
speedConversionFactors = {
    # Metres per second (m/s)
    (0, 0): 1, (0, 1): 3.6, (0, 2): (3125 / 1397), (0, 3): (5 / 1718), (0, 4): (1 / 299792458),
    # Kilometres per hour (km/h)
    (1, 0): (5 / 18), (1, 1): 1, (1, 2): (15625 / 25146), (1, 3): (25 / 30924), (1, 4): (5 / 5396264244),
    # Miles per hour (mph)
    (2, 0): (1397 / 3125), (2, 1): 1.609344, (2, 2): 1, (2, 3): (1397 / 1073750), (2, 4): (1397 / 936851431250),
    # Mach (Ma)
    (3, 0): 343.6, (3, 1): 1236.96, (3, 2): (1073750 / 1397), (3, 3): 1, (3, 4): (859 / 749481145),
    # Speed of Light (c)
    (4, 0): 299792458, (4, 1): 1079252848.8, (4, 2): (936851431250 / 1397), (4, 3): (749481145 / 859), (4, 4): 1
}
pressureConversionFactors = {
    # Atmosphere (atm)
    (0, 0): 1, (0, 1): 1.01325, (0, 2): 1013.25, (0, 3): (506625 / 34474), (0, 4): 101325, (0, 5): (506625000 /  49033), (0, 6): 760,
    # Bar (Bar)
    (1, 0): (4000 / 4053), (1, 1): 1, (1, 2): 1000, (1, 3): (250000 / 17237), (1, 4): 100000, (1, 5): (500000000 / 49033), (1, 6): (3040000 / 4053),
    # Millibar (mBar)
    (2, 0): (4 / 4053), (2, 1): 0.001, (2, 2): 1, (2, 3): (250 / 17237), (2, 4): 100, (2, 5): (500000 / 49033), (2, 6): (3040 / 4053),
    # Pounds per square inch (psi)
    (3, 0): (34474 / 506625), (3, 1): 0.068948, (3, 2): 68.948, (3, 3): 1, (3, 4): 6894.8, (3, 5): (34474000 / 49033), (3, 6): (436634756250000 / 45680466691),
    # Pascal (Pa) | Newtons per square metre (N/m²)
    (4, 0): (1 / 101325), (4, 1): 0.00001, (4, 2): 0.01, (4, 3): (5 / 34474), (4, 4): 1, (4, 5): (5000 / 49033), (4, 6): (152 / 20265),
    # Millimetres of H₂O [Water] (mmH₂O)
    (5, 0): (49033 / 506625000), (5, 1): 0.000098066, (5, 2): 0.098066, (5, 3): (49033 / 34474000), (5, 4): 9.8066, (5, 5): 1, (5, 6): (12665625 / 931627),
    # Millimetres of Hg [Mercury] (mmHg)
    (6, 0): (1 / 760), (6, 1): (4053 / 3040000), (6, 2): (4053 / 3040), (6, 3): (45680466691 / 436634756250000), (6, 4): (20265 / 152), (6, 5): (931627 / 12665625), (6, 6): 1
}
powerConversionFactors = {
    # Watt (W) | Joules per second (J/s) | Newton-metres per second (N∙m/s)
    (0, 0): 1, (0, 1): (12500000000000 / 16953513780357), (0, 2): (1 / 4184), (0, 3): (250000000000 / 186488651583927),
    # Foot-pounds per second (ft∙lb/s)
    (1, 0): 1.35628110242856, (1, 1): 1, (1, 2): (16953513780357 / 52300000000000000), (1, 3): 550,
    # Kilocalories per second (kcal/s)
    (2, 0): 4184, (2, 1): (52300000000000000 / 16953513780357), (2, 2): 1, (2, 3): (28765000000000000000 / 16953513780357),
    # Horsepower (HP)
    (3, 0): 745.954606335708, (3, 1): (1 / 550), (3, 2): (16953513780357 / 28765000000000000000), (3, 3): 1
}

CalcWizard = QApplication([])
# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)
window.setWindowIcon(QIcon(iconPath))

# Font Attributes
# Main Label Font
mainLabelFont = QFont()
mainLabelFont.setPixelSize(52)
mainLabelFont.setBold(True)
# Conversion Pages Label Font
conversionsLabelFont = QFont()
conversionsLabelFont.setPixelSize(40)
conversionsLabelFont.setBold(True)
# Conversions Page Buttons Font
goToButtonFonts = QFont()
goToButtonFonts.setPixelSize(80)
goToButtonFonts.setBold(True)
# Conversions Page Labels Font
goToLabelFonts = QFont()
goToLabelFonts.setPixelSize(20)
# Input Field Font
inputFieldFont = QFont()
inputFieldFont.setPixelSize(28)
inputFieldFont.setBold(False)
# Output Field Font
outputFieldFont = QFont()
outputFieldFont.setPixelSize(28)
outputFieldFont.setBold(True)
# Paste Button Font
pasteButtonFont = QFont()
pasteButtonFont.setPixelSize(20)
pasteButtonFont.setBold(True)
# Conversion Paste Button Font
conversionPasteButtonFont = QFont()
conversionPasteButtonFont.setPixelSize(44)
conversionPasteButtonFont.setBold(True)
# Calculator Mode Button Font
calculatorModeButtonFont = QFont()
calculatorModeButtonFont.setPixelSize(48)
calculatorModeButtonFont.setBold(True)
# Number Pad Font
numberPadFont = QFont()
numberPadFont.setPixelSize(36)
numberPadFont.setBold(True)
# Result Buttons Font
resultButtonsFont = QFont()
resultButtonsFont.setPixelSize(60)
resultButtonsFont.setBold(True)
# Operator Buttons Font
operatorButtonFont = QFont()
operatorButtonFont.setPixelSize(44)
operatorButtonFont.setBold(True)
# Trigonometry Buttons Font
trigonometryButtonFont = QFont()
trigonometryButtonFont.setPixelSize(28)
trigonometryButtonFont.setBold(True)
# Constant Buttons Font
constantButtonFont = QFont()
constantButtonFont.setPixelSize(36)
constantButtonFont.setBold(True)
constantButtonFont.setItalic(True)
# ComboBox Font
comboBoxFont = QFont()
comboBoxFont.setPixelSize(13)
comboBoxFont.setBold(True)
comboBoxFont.setItalic(True)

# Pop-ups
# Error Message
errorMessageBox = QMessageBox()
errorMessageBox.setWindowIcon(QIcon(iconPath))
# API Key Dialog Box
apiDialogBox = QInputDialog()
apiDialogBox.setWindowTitle('API Key Input')
apiDialogBox.setWindowIcon(QIcon(iconPath))
apiDialogBox.setLabelText('Enter your API Key (ExchangeRate-API)')

# QStackedWidget Instance
stackedWidget = QStackedWidget(window)
window.setCentralWidget(stackedWidget)
# Calculator Page
# Calculator Widget
calculatorWidget = QWidget()
stackedWidget.addWidget(calculatorWidget)
# Switch to Conversions Button
switchToConversionsButton = QPushButton('⇄', calculatorWidget)
switchToConversionsButton.setFixedSize(60, 60)
switchToConversionsButton.move(510, 30)
switchToConversionsButton.setFont(mainLabelFont)
def switchToConversions():
    stackedWidget.setCurrentWidget(conversionsWidget)
switchToConversionsButton.clicked.connect(switchToConversions)
# Calculator Page Main Label
calculatorLabel = QLabel('CALCULATOR', calculatorWidget)
calculatorLabel.setFixedSize(540, 60)
calculatorLabel.move(30, 120)
calculatorLabel.setFont(mainLabelFont)
calculatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Input Field
calculatorInputField = QLineEdit(calculatorWidget)
calculatorInputField.setPlaceholderText('Input')
calculatorInputField.setFixedSize(540, 60)
calculatorInputField.move(30, 210)
calculatorInputField.setFont(inputFieldFont)
calculatorInputField.setAlignment(Qt.AlignmentFlag.AlignRight)
calculatorInputField.setStyleSheet('border: 2px solid; padding-right: 15px')
calculatorInputField.setReadOnly(True)
# Paste Output to Input
calculatorPasteButton = QPushButton('↑', calculatorWidget)
calculatorPasteButton.setFixedSize(30, 30)
calculatorPasteButton.move(540, 270)
calculatorPasteButton.setFont(pasteButtonFont)
calculatorPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def calculatorPaste():
    if calculatorOutputField.text():
        global calculatorInput
        calculatorInputField.setText(calculatorOutputField.text())
        calculatorInput = str(calculatorOutputField.text())
        calculatorOutputField.setText('')
calculatorPasteButton.clicked.connect(calculatorPaste)
# Output Field
calculatorOutputField = QLineEdit(calculatorWidget)
calculatorOutputField.setFixedSize(540, 60)
calculatorOutputField.move(30, 300)
calculatorOutputField.setFont(outputFieldFont)
calculatorOutputField.setAlignment(Qt.AlignmentFlag.AlignRight)
calculatorOutputField.setStyleSheet('border: 2px solid; padding-right: 15px')
calculatorOutputField.setPlaceholderText('Output')
calculatorOutputField.setReadOnly(True)
# Calculator Mode Button
calculatorModeButton = QPushButton('∞', calculatorWidget)
calculatorModeButton.setFixedSize(90, 90)
calculatorModeButton.move(30, 390)
calculatorModeButton.setFont(calculatorModeButtonFont)
calculatorModeButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 255)')
calculatorModeButton.setCheckable(True)
def calculatorMode():
    if calculatorModeButton.isChecked():                    # Advanced Mode
        calculatorModeButton.setText('±')
        openBracketButton.setVisible(True)
        closeBracketButton.setVisible(True)
        sineButton.setVisible(True)
        cosineButton.setVisible(True)
        tangentButton.setVisible(True)
        angleButton.setVisible(True)
        baseTenLogButton.setVisible(True)
        baseTwoLogButton.setVisible(True)
        naturalLogButton.setVisible(True)
        inverseButton.setVisible(True)
        squareButton.setVisible(True)
        exponentButton.setVisible(True)
        piButton.setVisible(True)
        eulerButton.setVisible(True)
    else:                                                   # Basic Mode
        calculatorModeButton.setText('∞')
        openBracketButton.setVisible(False)
        closeBracketButton.setVisible(False)
        sineButton.setVisible(False)
        cosineButton.setVisible(False)
        tangentButton.setVisible(False)
        sineInverseButton.setVisible(False)
        cosineInverseButton.setVisible(False)
        tangentInverseButton.setVisible(False)
        angleButton.setVisible(False)
        angleButton.setChecked(False)
        baseTenLogButton.setVisible(False)
        baseTwoLogButton.setVisible(False)
        naturalLogButton.setVisible(False)
        powerTenButton.setVisible(False)
        powerTwoButton.setVisible(False)
        powerEulerButton.setVisible(False)
        inverseButton.setVisible(False)
        inverseButton.setChecked(False)
        squareButton.setVisible(False)
        exponentButton.setVisible(False)
        piButton.setVisible(False)
        eulerButton.setVisible(False)
calculatorModeButton.clicked.connect(calculatorMode)
# Number Pad
# Nine [9]
calculatorNineButton = QPushButton('9', calculatorWidget)
calculatorNineButton.setFixedSize(90, 90)
calculatorNineButton.move(300, 570)
calculatorNineButton.setFont(numberPadFont)
calculatorNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorNine():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '9')
    calculatorInput += '9'
calculatorNineButton.clicked.connect(calculatorNine)
# Eight [8]
calculatorEightButton = QPushButton('8', calculatorWidget)
calculatorEightButton.setFixedSize(90, 90)
calculatorEightButton.move(210, 570)
calculatorEightButton.setFont(numberPadFont)
calculatorEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorEight():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '8')
    calculatorInput += '8'
calculatorEightButton.clicked.connect(calculatorEight)
# Seven [7]
calculatorSevenButton = QPushButton('7', calculatorWidget)
calculatorSevenButton.setFixedSize(90, 90)
calculatorSevenButton.move(120, 570)
calculatorSevenButton.setFont(numberPadFont)
calculatorSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorSeven():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '7')
    calculatorInput += '7'
calculatorSevenButton.clicked.connect(calculatorSeven)
# Six [6]
calculatorSixButton = QPushButton('6', calculatorWidget)
calculatorSixButton.setFixedSize(90, 90)
calculatorSixButton.move(300, 660)
calculatorSixButton.setFont(numberPadFont)
calculatorSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorSix():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '6')
    calculatorInput += '6'
calculatorSixButton.clicked.connect(calculatorSix)
# Five [5]
calculatorFiveButton = QPushButton('5', calculatorWidget)
calculatorFiveButton.setFixedSize(90, 90)
calculatorFiveButton.move(210, 660)
calculatorFiveButton.setFont(numberPadFont)
calculatorFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorFive():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '5')
    calculatorInput += '5'
calculatorFiveButton.clicked.connect(calculatorFive)
# Four [4]
calculatorFourButton = QPushButton('4', calculatorWidget)
calculatorFourButton.setFixedSize(90, 90)
calculatorFourButton.move(120, 660)
calculatorFourButton.setFont(numberPadFont)
calculatorFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorFour():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '4')
    calculatorInput += '4'
calculatorFourButton.clicked.connect(calculatorFour)
# Three [3]
calculatorThreeButton = QPushButton('3', calculatorWidget)
calculatorThreeButton.setFixedSize(90, 90)
calculatorThreeButton.move(300, 750)
calculatorThreeButton.setFont(numberPadFont)
calculatorThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorThree():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '3')
    calculatorInput += '3'
calculatorThreeButton.clicked.connect(calculatorThree)
# Two [2]
calculatorTwoButton = QPushButton('2', calculatorWidget)
calculatorTwoButton.setFixedSize(90, 90)
calculatorTwoButton.move(210, 750)
calculatorTwoButton.setFont(numberPadFont)
calculatorTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorTwo():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '2')
    calculatorInput += '2'
calculatorTwoButton.clicked.connect(calculatorTwo)
# One [1]
calculatorOneButton = QPushButton('1', calculatorWidget)
calculatorOneButton.setFixedSize(90, 90)
calculatorOneButton.move(120, 750)
calculatorOneButton.setFont(numberPadFont)
calculatorOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorOne():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '1')
    calculatorInput += '1'
calculatorOneButton.clicked.connect(calculatorOne)
# Zero [0]
calculatorZeroButton = QPushButton('0', calculatorWidget)
calculatorZeroButton.setFixedSize(90, 90)
calculatorZeroButton.move(210, 840)
calculatorZeroButton.setFont(numberPadFont)
calculatorZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def calculatorZero():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '0')
    calculatorInput += '0'
calculatorZeroButton.clicked.connect(calculatorZero)
# Point [.]
calculatorPointButton = QPushButton('.', calculatorWidget)
calculatorPointButton.setFixedSize(90, 90)
calculatorPointButton.move(300, 840)
calculatorPointButton.setFont(numberPadFont)
calculatorPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def calculatorPoint():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '.')
        calculatorInput += '.'
    else:
        calculatorInputField.setText(calculatorInputField.text() + '0.')
        calculatorInput += '0.'
calculatorPointButton.clicked.connect(calculatorPoint)
# Deletion
# All Clear
calculatorAllClearButton = QPushButton('AC', calculatorWidget)
calculatorAllClearButton.setFixedSize(90, 90)
calculatorAllClearButton.move(390, 480)
calculatorAllClearButton.setFont(operatorButtonFont)
calculatorAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def calculatorAllClear():
    global calculatorInput
    calculatorInputField.setText('')
    calculatorOutputField.setText('')
    calculatorInput = ''
calculatorAllClearButton.clicked.connect(calculatorAllClear)
# Clear [Backspace]
calculatorClearButton = QPushButton('C', calculatorWidget)
calculatorClearButton.setFixedSize(90, 90)
calculatorClearButton.move(480, 480)
calculatorClearButton.setFont(operatorButtonFont)
calculatorClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def calculatorClear():
    global calculatorInput
    if calculatorInputField.text():
        if calculatorInputField.text().endswith('sin('):
            calculatorInputField.setText(calculatorInputField.text().replace('sin(', ''))
            calculatorInput = calculatorInput.replace('sin(', '')
        elif calculatorInputField.text().endswith('cos('):
            calculatorInputField.setText(calculatorInputField.text().replace('cos(', ''))
            calculatorInput = calculatorInput.replace('cos(', '')
        elif calculatorInputField.text().endswith('tan('):
            calculatorInputField.setText(calculatorInputField.text().replace('tan(', ''))
            calculatorInput = calculatorInput.replace('tan(', '')
        elif calculatorInputField.text().endswith('sin⁻¹('):
            calculatorInputField.setText(calculatorInputField.text().replace('sin⁻¹(', ''))
            calculatorInput = calculatorInput.replace('atan(', '')
        elif calculatorInputField.text().endswith('log⏨('):
            calculatorInputField.setText(calculatorInputField.text().replace('log⏨(', ''))
            calculatorInput = calculatorInput.replace('log10(', '')
        elif calculatorInputField.text().endswith('log₂('):
            calculatorInputField.setText(calculatorInputField.text().replace('log₂(', ''))
            calculatorInput = calculatorInput.replace('log2(', '')
        elif calculatorInputField.text().endswith('ln('):
            calculatorInputField.setText(calculatorInputField.text().replace('ln(', ''))
            calculatorInput = calculatorInput.replace('log(', '')
        elif calculatorInputField.text().endswith('10^'):
            calculatorInputField.setText(calculatorInputField.text().replace('10^', ''))
            calculatorInput = calculatorInput.replace('10**', '')
        elif calculatorInputField.text().endswith('2^'):
            calculatorInputField.setText(calculatorInputField.text().replace('2^', ''))
            calculatorInput = calculatorInput.replace('2**', '')
        elif calculatorInputField.text().endswith('e^'):
            calculatorInputField.setText(calculatorInputField.text().replace('e^', ''))
            calculatorInput = calculatorInput.replace('e**', '')
        elif calculatorInputField.text().endswith('²'):
            calculatorInputField.setText(calculatorInputField.text().replace('²', ''))
            calculatorInput = calculatorInput.replace('**(2)', '')
        elif calculatorInputField.text().endswith('^'):
            calculatorInputField.setText(calculatorInputField.text().replace('^', ''))
            calculatorInput = calculatorInput.replace('**', '')
        else:
            calculatorInputFieldText = calculatorInputField.text()
            calculatorInputFieldText = calculatorInputFieldText[:-1]
            calculatorInputField.setText(calculatorInputFieldText)
            calculatorInput = calculatorInput[:-1]
calculatorClearButton.clicked.connect(calculatorClear)
# Operators [+ | - | × | ÷]
# Plus [+]
plusButton = QPushButton('+', calculatorWidget)
plusButton.setFixedSize(90, 90)
plusButton.move(390, 660)
plusButton.setFont(operatorButtonFont)
plusButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def plus():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '+')
        calculatorInput += '+'
plusButton.clicked.connect(plus)
# Minus [-]
minusButton = QPushButton('-', calculatorWidget)
minusButton.setFixedSize(90, 90)
minusButton.move(480, 660)
minusButton.setFont(operatorButtonFont)
minusButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def minus():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '-')
        calculatorInput += '-'
minusButton.clicked.connect(minus)
# Multiply [×]
multiplyButton = QPushButton('×', calculatorWidget)
multiplyButton.setFixedSize(90, 90)
multiplyButton.move(390, 750)
multiplyButton.setFont(operatorButtonFont)
multiplyButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def multiply():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '×')
        calculatorInput += '*'
multiplyButton.clicked.connect(multiply)
# Divide [÷]
divideButton = QPushButton('÷', calculatorWidget)
divideButton.setFixedSize(90, 90)
divideButton.move(480, 750)
divideButton.setFont(operatorButtonFont)
divideButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def divide():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '÷')
        calculatorInput += '/'
divideButton.clicked.connect(divide)
# Percent [%]
percentButton = QPushButton('%', calculatorWidget)
percentButton.setFixedSize(90, 90)
percentButton.move(30, 570)
percentButton.setFont(operatorButtonFont)
percentButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def percent():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '%')
        calculatorInput += '/100'
percentButton.clicked.connect(percent)
# Brackets
# Open Bracket [(]
openBracketButton = QPushButton('(', calculatorWidget)
openBracketButton.setFixedSize(90, 90)
openBracketButton.move(390, 570)
openBracketButton.setFont(operatorButtonFont)
openBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
openBracketButton.setVisible(False)
def openBracket():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '(')
    calculatorInput += '('
openBracketButton.clicked.connect(openBracket)
# Close Bracket [)]
closeBracketButton = QPushButton(')', calculatorWidget)
closeBracketButton.setFixedSize(90, 90)
closeBracketButton.move(480, 570)
closeBracketButton.setFont(operatorButtonFont)
closeBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
closeBracketButton.setVisible(False)
def closeBracket():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + ')')
        if angleButton.isChecked():
            calculatorInput += '))'
        else:
            calculatorInput += ')'
closeBracketButton.clicked.connect(closeBracket)
# Trigonometry
# Sine
sineButton = QPushButton('sin', calculatorWidget)
sineButton.setFixedSize(90, 90)
sineButton.move(120, 390)
sineButton.setFont(trigonometryButtonFont)
sineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
sineButton.setVisible(False)
def sine():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'sin(')
    if angleButton.isChecked():
        calculatorInput += 'sin(radians('
    else:
        calculatorInput += 'sin('
sineButton.clicked.connect(sine)
# Cosine
cosineButton = QPushButton('cos', calculatorWidget)
cosineButton.setFixedSize(90, 90)
cosineButton.move(210, 390)
cosineButton.setFont(trigonometryButtonFont)
cosineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
cosineButton.setVisible(False)
def cosine():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'cos(')
    if angleButton.isChecked():
        calculatorInput += 'cos(radians('
    else:
        calculatorInput += 'cos('
cosineButton.clicked.connect(cosine)
# Tangent
tangentButton = QPushButton('tan', calculatorWidget)
tangentButton.setFixedSize(90, 90)
tangentButton.move(300, 390)
tangentButton.setFont(trigonometryButtonFont)
tangentButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
tangentButton.setVisible(False)
def tangent():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'tan(')
    if angleButton.isChecked():
        calculatorInput += 'tan(radians('
    else:
        calculatorInput += 'tan('
tangentButton.clicked.connect(tangent)
# Sine Inverse
sineInverseButton = QPushButton('sin⁻¹', calculatorWidget)
sineInverseButton.setFixedSize(90, 90)
sineInverseButton.move(120, 390)
sineInverseButton.setFont(trigonometryButtonFont)
sineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
sineInverseButton.setVisible(False)
def sineInverse():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'sin⁻¹(')
    if angleButton.isChecked():
        calculatorInput += 'asin(radians('
    else:
        calculatorInput += 'asin('
sineInverseButton.clicked.connect(sineInverse)
# Cosine Inverse
cosineInverseButton = QPushButton('cos⁻¹', calculatorWidget)
cosineInverseButton.setFixedSize(90, 90)
cosineInverseButton.move(210, 390)
cosineInverseButton.setFont(trigonometryButtonFont)
cosineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
cosineInverseButton.setVisible(False)
def cosineInverse():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'cos⁻¹(')
    if angleButton.isChecked():
        calculatorInput += 'acos(radians('
    else:
        calculatorInput += 'acos('
cosineInverseButton.clicked.connect(cosineInverse)
# Tangent Inverse
tangentInverseButton = QPushButton('tan⁻¹', calculatorWidget)
tangentInverseButton.setFixedSize(90, 90)
tangentInverseButton.move(300, 390)
tangentInverseButton.setFont(trigonometryButtonFont)
tangentInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
tangentInverseButton.setVisible(False)
def tangentInverse():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'tan⁻¹(')
    if angleButton.isChecked():
        calculatorInput += 'atan(radians('
    else:
        calculatorInput += 'atan('
tangentInverseButton.clicked.connect(tangentInverse)
# Angle Button
angleButton = QPushButton('RAD', calculatorWidget)
angleButton.setFixedSize(180, 90)
angleButton.move(390, 390)
angleButton.setFont(numberPadFont)
angleButton.setStyleSheet('border: 2px solid; background-color: rgb(200, 180, 160)')
angleButton.setVisible(False)
angleButton.setCheckable(True)
def angle():
    if angleButton.isChecked():
        angleButton.setText('DEG')
    else:
        angleButton.setText('RAD')
angleButton.clicked.connect(angle)
# Logarithm
# Base 10 Log
baseTenLogButton = QPushButton('log⏨', calculatorWidget)
baseTenLogButton.setFixedSize(90, 90)
baseTenLogButton.move(120, 480)
baseTenLogButton.setFont(numberPadFont)
baseTenLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
baseTenLogButton.setVisible(False)
def baseTenLog():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'log⏨(')
    calculatorInput += 'log10('
baseTenLogButton.clicked.connect(baseTenLog)
# Base 2 Log
baseTwoLogButton = QPushButton('log₂', calculatorWidget)
baseTwoLogButton.setFixedSize(90, 90)
baseTwoLogButton.move(210, 480)
baseTwoLogButton.setFont(numberPadFont)
baseTwoLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
baseTwoLogButton.setVisible(False)
def baseTwoLog():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'log₂(')
    calculatorInput += 'log2('
baseTwoLogButton.clicked.connect(baseTwoLog)
# Natural Log
naturalLogButton = QPushButton('ln', calculatorWidget)
naturalLogButton.setFixedSize(90, 90)
naturalLogButton.move(300, 480)
naturalLogButton.setFont(numberPadFont)
naturalLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
naturalLogButton.setVisible(False)
def naturalLog():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'ln(')
    calculatorInput += 'log('
naturalLogButton.clicked.connect(naturalLog)
# Logarithm Buttons Inverse
# Exponents of 10
powerTenButton = QPushButton('10ˣ', calculatorWidget)
powerTenButton.setFixedSize(90, 90)
powerTenButton.move(120, 480)
powerTenButton.setFont(numberPadFont)
powerTenButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerTenButton.setVisible(False)
def powerTen():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '10^')
    calculatorInput += '10**'
powerTenButton.clicked.connect(powerTen)
# Exponent of 2
powerTwoButton = QPushButton('2ˣ', calculatorWidget)
powerTwoButton.setFixedSize(90, 90)
powerTwoButton.move(210, 480)
powerTwoButton.setFont(numberPadFont)
powerTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerTwoButton.setVisible(False)
def powerTwo():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + '2^')
    calculatorInput += '2**'
powerTwoButton.clicked.connect(powerTwo)
# Exponents of e
powerEulerButton = QPushButton('eˣ', calculatorWidget)
powerEulerButton.setFixedSize(90, 90)
powerEulerButton.move(300, 480)
powerEulerButton.setFont(numberPadFont)
powerEulerButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerEulerButton.setVisible(False)
def powerEuler():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'e^')
    calculatorInput += 'e**'
powerEulerButton.clicked.connect(powerEuler)
# Inverse Button
inverseButton = QPushButton('INV', calculatorWidget)
inverseButton.setFixedSize(90, 90)
inverseButton.move(30, 480)
inverseButton.setFont(numberPadFont)
inverseButton.setStyleSheet('border: 2px solid; background-color: rgb(128, 128, 128)')
inverseButton.setVisible(False)
inverseButton.setCheckable(True)
def inverse():
    if inverseButton.isChecked():
        sineButton.setVisible(False)
        cosineButton.setVisible(False)
        tangentButton.setVisible(False)
        baseTenLogButton.setVisible(False)
        baseTwoLogButton.setVisible(False)
        naturalLogButton.setVisible(False)
        sineInverseButton.setVisible(True)
        cosineInverseButton.setVisible(True)
        tangentInverseButton.setVisible(True)
        powerTenButton.setVisible(True)
        powerTwoButton.setVisible(True)
        powerEulerButton.setVisible(True)
    else:
        sineButton.setVisible(True)
        cosineButton.setVisible(True)
        tangentButton.setVisible(True)
        baseTenLogButton.setVisible(True)
        baseTwoLogButton.setVisible(True)
        naturalLogButton.setVisible(True)
        sineInverseButton.setVisible(False)
        cosineInverseButton.setVisible(False)
        tangentInverseButton.setVisible(False)
        powerTenButton.setVisible(False)
        powerTwoButton.setVisible(False)
        powerEulerButton.setVisible(False)
inverseButton.clicked.connect(inverse)
# Square [x²]
squareButton = QPushButton('x²', calculatorWidget)
squareButton.setFixedSize(90, 90)
squareButton.move(30, 660)
squareButton.setFont(numberPadFont)
squareButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
squareButton.setVisible(False)
def square():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '²')
        calculatorInput += '**(2)'
squareButton.clicked.connect(square)
# Exponent
exponentButton = QPushButton('^', calculatorWidget)
exponentButton.setFixedSize(90, 90)
exponentButton.move(30, 750)
exponentButton.setFont(numberPadFont)
exponentButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
exponentButton.setVisible(False)
def exponent():
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + '^')
        calculatorInput += '**'
exponentButton.clicked.connect(exponent)
# Constants [π | e]
# pi [π]
piButton = QPushButton('π', calculatorWidget)
piButton.setFixedSize(90, 90)
piButton.move(30, 840)
piButton.setFont(constantButtonFont)
piButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
piButton.setVisible(False)
def piCharacter():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'π')
    calculatorInput += 'pi'
piButton.clicked.connect(piCharacter)
# Euler's Number [e]
eulerButton = QPushButton('e', calculatorWidget)
eulerButton.setFixedSize(90, 90)
eulerButton.move(120, 840)
eulerButton.setFont(constantButtonFont)
eulerButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
eulerButton.setVisible(False)
def eulerNumber():
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + 'e')
    calculatorInput += 'e'
eulerButton.clicked.connect(eulerNumber)
# Result [=]
calculatorResultButton = QPushButton('=', calculatorWidget)
calculatorResultButton.setFixedSize(180, 90)
calculatorResultButton.move(390, 840)
calculatorResultButton.setFont(resultButtonsFont)
calculatorResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def calculatorResult():
    global calculatorInput
    try:
        if calculatorInputField.text():
            if calculatorInputField.text().endswith('.'):
                calculatorInputField.setText(calculatorInputField.text().replace('.', ''))
                calculatorInput = calculatorInput.replace('.', '')
            calculatorOutputField.setText(str(eval(calculatorInput)))
    except Exception as err:
        errorMessage = str(err)
        errorMessage = errorMessage.replace('(<string>, line 1)', '')
        errorMessageBox.critical(calculatorWidget, 'Error', f'An error occurred: {errorMessage}\nScript: {calculatorInput}')
calculatorResultButton.clicked.connect(calculatorResult)

# Conversions Page
# Conversions Widget
conversionsWidget = QWidget()
stackedWidget.addWidget(conversionsWidget)
# Switch to Calculator Button
conversionsSwitchToCalculatorButton = QPushButton('⇄', conversionsWidget)
conversionsSwitchToCalculatorButton.setFixedSize(60, 60)
conversionsSwitchToCalculatorButton.move(510, 30)
conversionsSwitchToCalculatorButton.setFont(mainLabelFont)
def conversionsSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
conversionsSwitchToCalculatorButton.clicked.connect(conversionsSwitchToCalculator)
# Conversions Page Main Label
conversionsLabel = QLabel('CONVERSIONS', conversionsWidget)
conversionsLabel.setFixedSize(540, 60)
conversionsLabel.move(30, 120)
conversionsLabel.setFont(mainLabelFont)
conversionsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Currency Conversion Button
goToCurrencyConversionButton = QPushButton('💲', conversionsWidget)
goToCurrencyConversionButton.setFixedSize(120, 120)
goToCurrencyConversionButton.move(60, 240)
goToCurrencyConversionButton.setFont(goToButtonFonts)
goToCurrencyConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToCurrencyConversion():
    stackedWidget.setCurrentWidget(currencyConversionWidget)
goToCurrencyConversionButton.clicked.connect(goToCurrencyConversion)
# Currency Conversion Label
goToCurrencyConversionLabel = QLabel('Currency', conversionsWidget)
goToCurrencyConversionLabel.setFixedSize(120, 30)
goToCurrencyConversionLabel.move(60, 360)
goToCurrencyConversionLabel.setFont(goToLabelFonts)
goToCurrencyConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Length Conversion Button
goToLengthConversionButton = QPushButton('📏', conversionsWidget)
goToLengthConversionButton.setFixedSize(120, 120)
goToLengthConversionButton.move(240, 240)
goToLengthConversionButton.setFont(goToButtonFonts)
goToLengthConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToLengthConversion():
    stackedWidget.setCurrentWidget(lengthConversionWidget)
goToLengthConversionButton.clicked.connect(goToLengthConversion)
# Length Conversion Label
goToLengthConversionLabel = QLabel('Length', conversionsWidget)
goToLengthConversionLabel.setFixedSize(120, 30)
goToLengthConversionLabel.move(240, 360)
goToLengthConversionLabel.setFont(goToLabelFonts)
goToLengthConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Area Conversion Button
goToAreaConversionButton = QPushButton('🏁', conversionsWidget)
goToAreaConversionButton.setFixedSize(120, 120)
goToAreaConversionButton.move(420, 240)
goToAreaConversionButton.setFont(goToButtonFonts)
goToAreaConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToAreaConversion():
    stackedWidget.setCurrentWidget(areaConversionWidget)
goToAreaConversionButton.clicked.connect(goToAreaConversion)
# Area Conversion Label
goToAreaConversionLabel = QLabel('Area', conversionsWidget)
goToAreaConversionLabel.setFixedSize(120, 30)
goToAreaConversionLabel.move(420, 360)
goToAreaConversionLabel.setFont(goToLabelFonts)
goToAreaConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Volume Conversion Button
goToVolumeConversionButton = QPushButton('🧊', conversionsWidget)
goToVolumeConversionButton.setFixedSize(120, 120)
goToVolumeConversionButton.move(60, 450)
goToVolumeConversionButton.setFont(goToButtonFonts)
goToVolumeConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToVolumeConversion():
    stackedWidget.setCurrentWidget(volumeConversionWidget)
goToVolumeConversionButton.clicked.connect(goToVolumeConversion)
# Volume Conversion Label
goToVolumeConversionLabel = QLabel('Volume', conversionsWidget)
goToVolumeConversionLabel.setFixedSize(120, 30)
goToVolumeConversionLabel.move(60, 570)
goToVolumeConversionLabel.setFont(goToLabelFonts)
goToVolumeConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Weight Conversion Button
goToWeightConversionButton = QPushButton('⚖️', conversionsWidget)
goToWeightConversionButton.setFixedSize(120, 120)
goToWeightConversionButton.move(240, 450)
goToWeightConversionButton.setFont(goToButtonFonts)
goToWeightConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToWeightConversion():
    stackedWidget.setCurrentWidget(weightConversionWidget)
goToWeightConversionButton.clicked.connect(goToWeightConversion)
# Weight Conversion Label
goToWeightConversionLabel = QLabel('Weight', conversionsWidget)
goToWeightConversionLabel.setFixedSize(120, 30)
goToWeightConversionLabel.move(240, 570)
goToWeightConversionLabel.setFont(goToLabelFonts)
goToWeightConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Temperature Conversion Button
goToTemperatureConversionButton = QPushButton('🌡️', conversionsWidget)
goToTemperatureConversionButton.setFixedSize(120, 120)
goToTemperatureConversionButton.move(420, 450)
goToTemperatureConversionButton.setFont(goToButtonFonts)
goToTemperatureConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToTemperatureConversion():
    stackedWidget.setCurrentWidget(temperatureConversionWidget)
goToTemperatureConversionButton.clicked.connect(goToTemperatureConversion)
# Temperature Conversion Label
goToTemperatureConversionLabel = QLabel('Temperature', conversionsWidget)
goToTemperatureConversionLabel.setFixedSize(120, 30)
goToTemperatureConversionLabel.move(420, 570)
goToTemperatureConversionLabel.setFont(goToLabelFonts)
goToTemperatureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Speed Conversion Button
goToSpeedConversionButton = QPushButton('🏎️', conversionsWidget)
goToSpeedConversionButton.setFixedSize(120, 120)
goToSpeedConversionButton.move(60, 660)
goToSpeedConversionButton.setFont(goToButtonFonts)
goToSpeedConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToSpeedConversion():
    stackedWidget.setCurrentWidget(speedConversionWidget)
goToSpeedConversionButton.clicked.connect(goToSpeedConversion)
# Speed Conversion Label
goToSpeedConversionLabel = QLabel('Speed', conversionsWidget)
goToSpeedConversionLabel.setFixedSize(120, 30)
goToSpeedConversionLabel.move(60, 780)
goToSpeedConversionLabel.setFont(goToLabelFonts)
goToSpeedConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Pressure Conversion Button
goToPressureConversionButton = QPushButton('⏱️', conversionsWidget)
goToPressureConversionButton.setFixedSize(120, 120)
goToPressureConversionButton.move(240, 660)
goToPressureConversionButton.setFont(goToButtonFonts)
goToPressureConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToPressureConversion():
    stackedWidget.setCurrentWidget(pressureConversionWidget)
goToPressureConversionButton.clicked.connect(goToPressureConversion)
# Pressure Conversion Label
goToPressureConversionLabel = QLabel('Pressure', conversionsWidget)
goToPressureConversionLabel.setFixedSize(120, 30)
goToPressureConversionLabel.move(240, 780)
goToPressureConversionLabel.setFont(goToLabelFonts)
goToPressureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Power Conversion Button
goToPowerConversionButton = QPushButton('💪', conversionsWidget)
goToPowerConversionButton.setFixedSize(120, 120)
goToPowerConversionButton.move(420, 660)
goToPowerConversionButton.setFont(goToButtonFonts)
goToPowerConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')
def goToPowerConversion():
    stackedWidget.setCurrentWidget(powerConversionWidget)
goToPowerConversionButton.clicked.connect(goToPowerConversion)
# Power Conversion Label
goToPowerConversionLabel = QLabel('Power', conversionsWidget)
goToPowerConversionLabel.setFixedSize(120, 30)
goToPowerConversionLabel.move(420, 780)
goToPowerConversionLabel.setFont(goToLabelFonts)
goToPowerConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Note for Currency Conversion
noteLabel = QLabel('<b>⚠️ NOTE:</b> Currency Conversion requires Internet Connection', conversionsWidget)
noteLabel.setFixedSize(540, 30)
noteLabel.move(30, 900)
noteLabel.setFont(goToLabelFonts)
noteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Currency Conversion Page
# Currency Conversion Widget
currencyConversionWidget = QWidget()
stackedWidget.addWidget(currencyConversionWidget)
# Back Button
currencyBackButton = QPushButton('←', currencyConversionWidget)
currencyBackButton.setFixedSize(60, 60)
currencyBackButton.move(30, 30)
currencyBackButton.setFont(mainLabelFont)
def currencyBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
currencyBackButton.clicked.connect(currencyBack)
# Switch to Calculator Button
currencySwitchToCalculatorButton = QPushButton('⇄', currencyConversionWidget)
currencySwitchToCalculatorButton.setFixedSize(60, 60)
currencySwitchToCalculatorButton.move(510, 30)
currencySwitchToCalculatorButton.setFont(mainLabelFont)
def currencySwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
currencySwitchToCalculatorButton.clicked.connect(currencySwitchToCalculator)
# Currency Conversion Page Main Label
currencyConversionLabel = QLabel('Currency Conversion', currencyConversionWidget)
currencyConversionLabel.setFixedSize(540, 60)
currencyConversionLabel.move(30, 120)
currencyConversionLabel.setFont(conversionsLabelFont)
currencyConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
currencyConversionFromComboBox = QComboBox(currencyConversionWidget)
currencyConversionFromComboBox.setFixedSize(480, 60)
currencyConversionFromComboBox.move(30, 210)
currencyConversionFromComboBox.setFont(comboBoxFont)
currencyConversionFromComboBox.setStyleSheet('padding-left: 10px')
currencyConversionFromComboBox.addItem('AED - UAE Dirham (United Arab Emirates)')
currencyConversionFromComboBox.addItem('AFN - Afghan Afghani (Afghanistan)')
currencyConversionFromComboBox.addItem('ALL - Albanian Lek (Albania)')
currencyConversionFromComboBox.addItem('AMD - Armenian Dram (Armenia)')
currencyConversionFromComboBox.addItem('ANG - Netherlands Antillian Guilder (Netherlands Antilles)')
currencyConversionFromComboBox.addItem('AOA - Angolan Kwanza (Angola)')
currencyConversionFromComboBox.addItem('ARS - Argentine Peso (Argentina)')
currencyConversionFromComboBox.addItem('AUD - Australian Dollar (Australia)')
currencyConversionFromComboBox.addItem('AWG - Aruban Florin (Aruba)')
currencyConversionFromComboBox.addItem('AZN - Azerbaijani Manat (Azerbaijan)')
currencyConversionFromComboBox.addItem('BAM - Bosnia and Herzegovina Mark (Bosnia and Herzegovina)')
currencyConversionFromComboBox.addItem('BBD - Barbados Dollar (Barbados)')
currencyConversionFromComboBox.addItem('BDT - Bangladeshi Taka (Bangladesh)')
currencyConversionFromComboBox.addItem('BGN - Bulgarian Lev (Bulgaria)')
currencyConversionFromComboBox.addItem('BHD - Bahraini Dinar (Bahrain)')
currencyConversionFromComboBox.addItem('BIF - Burundian Franc (Burundi)')
currencyConversionFromComboBox.addItem('BMD - Bermudian Dollar (Bermuda)')
currencyConversionFromComboBox.addItem('BND - Brunei Dollar (Brunei)')
currencyConversionFromComboBox.addItem('BOB - Bolivian Boliviano (Bolivia)')
currencyConversionFromComboBox.addItem('BRL - Brazilian Real (Brazil)')
currencyConversionFromComboBox.addItem('BSD - Bahamian Dollar (Bahamas)')
currencyConversionFromComboBox.addItem('BTN - Bhutanese Ngultrum (Bhutan)')
currencyConversionFromComboBox.addItem('BWP - Botswana Pula (Botswana)')
currencyConversionFromComboBox.addItem('BYN - Belarusian Ruble (Belarus)')
currencyConversionFromComboBox.addItem('BZD - Belize Dollar (Belize)')
currencyConversionFromComboBox.addItem('CAD - Canadian Dollar (Canada)')
currencyConversionFromComboBox.addItem('CDF - Congolese Franc (Democratic Republic of the Congo)')
currencyConversionFromComboBox.addItem('CHF - Swiss Franc (Switzerland)')
currencyConversionFromComboBox.addItem('CLP - Chilean Peso (Chile)')
currencyConversionFromComboBox.addItem('CNY - Chinese Renminbi (China)')
currencyConversionFromComboBox.addItem('COP - Colombian Peso (Colombia)')
currencyConversionFromComboBox.addItem('CRC - Costa Rican Colon (Costa Rica)')
currencyConversionFromComboBox.addItem('CUP - Cuban Peso (Cuba)')
currencyConversionFromComboBox.addItem('CVE - Cape Verdean Escudo (Cape Verde)')
currencyConversionFromComboBox.addItem('CZK - Czech Koruna (Czech Republic)')
currencyConversionFromComboBox.addItem('DJF - Djiboutian Franc (Djibouti)')
currencyConversionFromComboBox.addItem('DKK - Danish Krone (Denmark)')
currencyConversionFromComboBox.addItem('DOP - Dominican Peso (Dominican Republic)')
currencyConversionFromComboBox.addItem('DZD - Algerian Dinar (Algeria)')
currencyConversionFromComboBox.addItem('EGP - Egyptian Pound (Egypt)')
currencyConversionFromComboBox.addItem('ERN - Eritrean Nakfa (Eritrea)')
currencyConversionFromComboBox.addItem('ETB - Ethiopian Birr (Ethiopia)')
currencyConversionFromComboBox.addItem('EUR - Euro (European Union)')
currencyConversionFromComboBox.addItem('FJD - Fiji Dollar (Fiji)')
currencyConversionFromComboBox.addItem('FKP - Falkland Islands Pound (Falkland Islands)')
currencyConversionFromComboBox.addItem('FOK - Faroese Króna (Faroe Islands)')
currencyConversionFromComboBox.addItem('GBP - Pound Sterling (United Kingdom)')
currencyConversionFromComboBox.addItem('GEL - Georgian Lari (Georgia)')
currencyConversionFromComboBox.addItem('GGP - Guernsey Pound (Guernsey)')
currencyConversionFromComboBox.addItem('GHS - Ghanaian Cedi (Ghana)')
currencyConversionFromComboBox.addItem('GIP - Gibraltar Pound (Gibraltar)')
currencyConversionFromComboBox.addItem('GMD - Gambian Dalasi The (Gambia)')
currencyConversionFromComboBox.addItem('GNF - Guinean Franc (Guinea)')
currencyConversionFromComboBox.addItem('GTQ - Guatemalan Quetzal (Guatemala)')
currencyConversionFromComboBox.addItem('GYD - Guyanese Dollar (Guyana)')
currencyConversionFromComboBox.addItem('HKD - Hong Kong Dollar (Hong Kong)')
currencyConversionFromComboBox.addItem('HNL - Honduran Lempira (Honduras)')
currencyConversionFromComboBox.addItem('HRK - Croatian Kuna (Croatia)')
currencyConversionFromComboBox.addItem('HTG - Haitian Gourde (Haiti)')
currencyConversionFromComboBox.addItem('HUF - Hungarian Forint (Hungary)')
currencyConversionFromComboBox.addItem('IDR - Indonesian Rupiah (Indonesia)')
currencyConversionFromComboBox.addItem('ILS - Israeli New Shekel (Israel)')
currencyConversionFromComboBox.addItem('IMP - Manx Pound (Isle of Man)')
currencyConversionFromComboBox.addItem('INR - Indian Rupee (India)')
currencyConversionFromComboBox.addItem('IQD - Iraqi Dinar (Iraq)')
currencyConversionFromComboBox.addItem('IRR - Iranian Rial (Iran)')
currencyConversionFromComboBox.addItem('ISK - Icelandic Króna (Iceland)')
currencyConversionFromComboBox.addItem('JEP - Jersey Pound (Jersey)')
currencyConversionFromComboBox.addItem('JMD - Jamaican Dollar (Jamaica)')
currencyConversionFromComboBox.addItem('JOD - Jordanian Dinar (Jordan)')
currencyConversionFromComboBox.addItem('JPY - Japanese Yen (Japan)')
currencyConversionFromComboBox.addItem('KES - Kenyan Shilling (Kenya)')
currencyConversionFromComboBox.addItem('KGS - Kyrgyzstani Som (Kyrgyzstan)')
currencyConversionFromComboBox.addItem('KHR - Cambodian Riel (Cambodia)')
currencyConversionFromComboBox.addItem('KID - Kiribati Dollar (Kiribati)')
currencyConversionFromComboBox.addItem('KMF - Comorian Franc (Comoros)')
currencyConversionFromComboBox.addItem('KRW - South Korean Won (South Korea)')
currencyConversionFromComboBox.addItem('KWD - Kuwaiti Dinar (Kuwait)')
currencyConversionFromComboBox.addItem('KYD - Cayman Islands Dollar (Cayman Islands)')
currencyConversionFromComboBox.addItem('KZT - Kazakhstani Tenge (Kazakhstan)')
currencyConversionFromComboBox.addItem('LAK - Lao Kip (Laos)')
currencyConversionFromComboBox.addItem('LBP - Lebanese Pound (Lebanon)')
currencyConversionFromComboBox.addItem('LKR - Sri Lanka Rupee (Sri Lanka)')
currencyConversionFromComboBox.addItem('LRD - Liberian Dollar (Liberia)')
currencyConversionFromComboBox.addItem('LSL - Lesotho Loti (Lesotho)')
currencyConversionFromComboBox.addItem('LYD - Libyan Dinar (Libya)')
currencyConversionFromComboBox.addItem('MAD - Moroccan Dirham (Morocco)')
currencyConversionFromComboBox.addItem('MDL - Moldovan Leu (Moldova)')
currencyConversionFromComboBox.addItem('MGA - Malagasy Ariary (Madagascar)')
currencyConversionFromComboBox.addItem('MKD - Macedonian Denar (North Macedonia)')
currencyConversionFromComboBox.addItem('MMK - Burmese Kyat (Myanmar)')
currencyConversionFromComboBox.addItem('MNT - Mongolian Tögrög (Mongolia)')
currencyConversionFromComboBox.addItem('MOP - Macanese Pataca (Macau)')
currencyConversionFromComboBox.addItem('MRU - Mauritanian Ouguiya (Mauritania)')
currencyConversionFromComboBox.addItem('MUR - Mauritian Rupee (Mauritius)')
currencyConversionFromComboBox.addItem('MVR - Maldivian Rufiyaa (Maldives)')
currencyConversionFromComboBox.addItem('MWK - Malawian Kwacha (Malawi)')
currencyConversionFromComboBox.addItem('MXN - Mexican Peso (Mexico)')
currencyConversionFromComboBox.addItem('MYR - Malaysian Ringgit (Malaysia)')
currencyConversionFromComboBox.addItem('MZN - Mozambican Metical (Mozambique)')
currencyConversionFromComboBox.addItem('NAD - Namibian Dollar (Namibia)')
currencyConversionFromComboBox.addItem('NGN - Nigerian Naira (Nigeria)')
currencyConversionFromComboBox.addItem('NIO - Nicaraguan Córdoba (Nicaragua)')
currencyConversionFromComboBox.addItem('NOK - Norwegian Krone (Norway)')
currencyConversionFromComboBox.addItem('NPR - Nepalese Rupee (Nepal)')
currencyConversionFromComboBox.addItem('NZD - New Zealand Dollar (New Zealand)')
currencyConversionFromComboBox.addItem('OMR - Omani Rial (Oman)')
currencyConversionFromComboBox.addItem('PAB - Panamanian Balboa (Panama)')
currencyConversionFromComboBox.addItem('PEN - Peruvian Sol (Peru)')
currencyConversionFromComboBox.addItem('PGK - Papua New Guinean Kina (Papua New Guinea)')
currencyConversionFromComboBox.addItem('PHP - Philippine Peso (Philippines)')
currencyConversionFromComboBox.addItem('PKR - Pakistani Rupee (Pakistan)')
currencyConversionFromComboBox.addItem('PLN - Polish Złoty (Poland)')
currencyConversionFromComboBox.addItem('PYG - Paraguayan Guaraní (Paraguay)')
currencyConversionFromComboBox.addItem('QAR - Qatari Riyal (Qatar)')
currencyConversionFromComboBox.addItem('RON - Romanian Leu (Romania)')
currencyConversionFromComboBox.addItem('RSD - Serbian Dinar (Serbia)')
currencyConversionFromComboBox.addItem('RUB - Russian Ruble (Russia)')
currencyConversionFromComboBox.addItem('RWF - Rwandan Franc (Rwanda)')
currencyConversionFromComboBox.addItem('SAR - Saudi Riyal (Saudi Arabia)')
currencyConversionFromComboBox.addItem('SBD - Solomon Islands Dollar (Solomon Islands)')
currencyConversionFromComboBox.addItem('SCR - Seychellois Rupee (Seychelles)')
currencyConversionFromComboBox.addItem('SDG - Sudanese Pound (Sudan)')
currencyConversionFromComboBox.addItem('SEK - Swedish Krona (Sweden)')
currencyConversionFromComboBox.addItem('SGD - Singapore Dollar (Singapore)')
currencyConversionFromComboBox.addItem('SHP - Saint Helena Pound (Saint Helena)')
currencyConversionFromComboBox.addItem('SLE - Sierra Leonean Leone (Sierra Leone)')
currencyConversionFromComboBox.addItem('SOS - Somali Shilling (Somalia)')
currencyConversionFromComboBox.addItem('SRD - Surinamese Dollar (Suriname)')
currencyConversionFromComboBox.addItem('SSP - South Sudanese Pound (South Sudan)')
currencyConversionFromComboBox.addItem('STN - São Tomé and Príncipe Dobra (São Tomé and Príncipe)')
currencyConversionFromComboBox.addItem('SYP - Syrian Pound (Syria)')
currencyConversionFromComboBox.addItem('SZL - Eswatini Lilangeni (Eswatini)')
currencyConversionFromComboBox.addItem('THB - Thai Baht (Thailand)')
currencyConversionFromComboBox.addItem('TJS - Tajikistani Somoni (Tajikistan)')
currencyConversionFromComboBox.addItem('TMT - Turkmenistan Manat (Turkmenistan)')
currencyConversionFromComboBox.addItem('TND - Tunisian Dinar (Tunisia)')
currencyConversionFromComboBox.addItem('TOP - Tongan Paʻanga (Tonga)')
currencyConversionFromComboBox.addItem('TRY - Turkish Lira (Turkey)')
currencyConversionFromComboBox.addItem('TTD - Trinidad and Tobago Dollar (Trinidad and Tobago)')
currencyConversionFromComboBox.addItem('TVD - Tuvaluan Dollar (Tuvalu)')
currencyConversionFromComboBox.addItem('TWD - New Taiwan Dollar (Taiwan)')
currencyConversionFromComboBox.addItem('TZS - Tanzanian Shilling (Tanzania)')
currencyConversionFromComboBox.addItem('UAH - Ukrainian Hryvnia (Ukraine)')
currencyConversionFromComboBox.addItem('UGX - Ugandan Shilling (Uganda)')
currencyConversionFromComboBox.addItem('USD - United States Dollar (United States)')
currencyConversionFromComboBox.addItem('UYU - Uruguayan Peso (Uruguay)')
currencyConversionFromComboBox.addItem('UZS - Uzbekistani So\'m (Uzbekistan)')
currencyConversionFromComboBox.addItem('VES - Venezuelan Bolívar Soberano (Venezuela)')
currencyConversionFromComboBox.addItem('VND - Vietnamese Đồng (Vietnam)')
currencyConversionFromComboBox.addItem('VUV - Vanuatu Vatu (Vanuatu)')
currencyConversionFromComboBox.addItem('WST - Samoan Tālā (Samoa)')
currencyConversionFromComboBox.addItem('XAF - Central African CFA Franc (CEMAC)')
currencyConversionFromComboBox.addItem('XCD - East Caribbean Dollar (Organisation of Eastern Caribbean States)')
currencyConversionFromComboBox.addItem('XDR - Special Drawing Rights (International Monetary Fund)')
currencyConversionFromComboBox.addItem('XOF - West African CFA franc (CFA)')
currencyConversionFromComboBox.addItem('XPF - CFP Franc (Collectivités d\'Outre-Mer)')
currencyConversionFromComboBox.addItem('YER - Yemeni Rial (Yemen)')
currencyConversionFromComboBox.addItem('ZAR - South African Rand (South Africa)')
currencyConversionFromComboBox.addItem('ZMW - Zambian Kwacha (Zambia)')
currencyConversionFromComboBox.addItem('ZWL - Zimbabwean Dollar (Zimbabwe)')
# Input Field
currencyConversionInputField = QLineEdit(currencyConversionWidget)
currencyConversionInputField.setPlaceholderText('Input')
currencyConversionInputField.setFixedSize(480, 60)
currencyConversionInputField.move(30, 270)
currencyConversionInputField.setFont(inputFieldFont)
currencyConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
currencyConversionInputField.setReadOnly(True)
# To Combo Box
currencyConversionToComboBox = QComboBox(currencyConversionWidget)
currencyConversionToComboBox.setFixedSize(480, 60)
currencyConversionToComboBox.move(30, 360)
currencyConversionToComboBox.setFont(comboBoxFont)
currencyConversionToComboBox.setStyleSheet('padding-left: 10px')
currencyConversionToComboBox.addItem('AED - UAE Dirham (United Arab Emirates)')
currencyConversionToComboBox.addItem('AFN - Afghan Afghani (Afghanistan)')
currencyConversionToComboBox.addItem('ALL - Albanian Lek (Albania)')
currencyConversionToComboBox.addItem('AMD - Armenian Dram (Armenia)')
currencyConversionToComboBox.addItem('ANG - Netherlands Antillian Guilder (Netherlands Antilles)')
currencyConversionToComboBox.addItem('AOA - Angolan Kwanza (Angola)')
currencyConversionToComboBox.addItem('ARS - Argentine Peso (Argentina)')
currencyConversionToComboBox.addItem('AUD - Australian Dollar (Australia)')
currencyConversionToComboBox.addItem('AWG - Aruban Florin (Aruba)')
currencyConversionToComboBox.addItem('AZN - Azerbaijani Manat (Azerbaijan)')
currencyConversionToComboBox.addItem('BAM - Bosnia and Herzegovina Mark (Bosnia and Herzegovina)')
currencyConversionToComboBox.addItem('BBD - Barbados Dollar (Barbados)')
currencyConversionToComboBox.addItem('BDT - Bangladeshi Taka (Bangladesh)')
currencyConversionToComboBox.addItem('BGN - Bulgarian Lev (Bulgaria)')
currencyConversionToComboBox.addItem('BHD - Bahraini Dinar (Bahrain)')
currencyConversionToComboBox.addItem('BIF - Burundian Franc (Burundi)')
currencyConversionToComboBox.addItem('BMD - Bermudian Dollar (Bermuda)')
currencyConversionToComboBox.addItem('BND - Brunei Dollar (Brunei)')
currencyConversionToComboBox.addItem('BOB - Bolivian Boliviano (Bolivia)')
currencyConversionToComboBox.addItem('BRL - Brazilian Real (Brazil)')
currencyConversionToComboBox.addItem('BSD - Bahamian Dollar (Bahamas)')
currencyConversionToComboBox.addItem('BTN - Bhutanese Ngultrum (Bhutan)')
currencyConversionToComboBox.addItem('BWP - Botswana Pula (Botswana)')
currencyConversionToComboBox.addItem('BYN - Belarusian Ruble (Belarus)')
currencyConversionToComboBox.addItem('BZD - Belize Dollar (Belize)')
currencyConversionToComboBox.addItem('CAD - Canadian Dollar (Canada)')
currencyConversionToComboBox.addItem('CDF - Congolese Franc (Democratic Republic of the Congo)')
currencyConversionToComboBox.addItem('CHF - Swiss Franc (Switzerland)')
currencyConversionToComboBox.addItem('CLP - Chilean Peso (Chile)')
currencyConversionToComboBox.addItem('CNY - Chinese Renminbi (China)')
currencyConversionToComboBox.addItem('COP - Colombian Peso (Colombia)')
currencyConversionToComboBox.addItem('CRC - Costa Rican Colon (Costa Rica)')
currencyConversionToComboBox.addItem('CUP - Cuban Peso (Cuba)')
currencyConversionToComboBox.addItem('CVE - Cape Verdean Escudo (Cape Verde)')
currencyConversionToComboBox.addItem('CZK - Czech Koruna (Czech Republic)')
currencyConversionToComboBox.addItem('DJF - Djiboutian Franc (Djibouti)')
currencyConversionToComboBox.addItem('DKK - Danish Krone (Denmark)')
currencyConversionToComboBox.addItem('DOP - Dominican Peso (Dominican Republic)')
currencyConversionToComboBox.addItem('DZD - Algerian Dinar (Algeria)')
currencyConversionToComboBox.addItem('EGP - Egyptian Pound (Egypt)')
currencyConversionToComboBox.addItem('ERN - Eritrean Nakfa (Eritrea)')
currencyConversionToComboBox.addItem('ETB - Ethiopian Birr (Ethiopia)')
currencyConversionToComboBox.addItem('EUR - Euro (European Union)')
currencyConversionToComboBox.addItem('FJD - Fiji Dollar (Fiji)')
currencyConversionToComboBox.addItem('FKP - Falkland Islands Pound (Falkland Islands)')
currencyConversionToComboBox.addItem('FOK - Faroese Króna (Faroe Islands)')
currencyConversionToComboBox.addItem('GBP - Pound Sterling (United Kingdom)')
currencyConversionToComboBox.addItem('GEL - Georgian Lari (Georgia)')
currencyConversionToComboBox.addItem('GGP - Guernsey Pound (Guernsey)')
currencyConversionToComboBox.addItem('GHS - Ghanaian Cedi (Ghana)')
currencyConversionToComboBox.addItem('GIP - Gibraltar Pound (Gibraltar)')
currencyConversionToComboBox.addItem('GMD - Gambian Dalasi The (Gambia)')
currencyConversionToComboBox.addItem('GNF - Guinean Franc (Guinea)')
currencyConversionToComboBox.addItem('GTQ - Guatemalan Quetzal (Guatemala)')
currencyConversionToComboBox.addItem('GYD - Guyanese Dollar (Guyana)')
currencyConversionToComboBox.addItem('HKD - Hong Kong Dollar (Hong Kong)')
currencyConversionToComboBox.addItem('HNL - Honduran Lempira (Honduras)')
currencyConversionToComboBox.addItem('HRK - Croatian Kuna (Croatia)')
currencyConversionToComboBox.addItem('HTG - Haitian Gourde (Haiti)')
currencyConversionToComboBox.addItem('HUF - Hungarian Forint (Hungary)')
currencyConversionToComboBox.addItem('IDR - Indonesian Rupiah (Indonesia)')
currencyConversionToComboBox.addItem('ILS - Israeli New Shekel (Israel)')
currencyConversionToComboBox.addItem('IMP - Manx Pound (Isle of Man)')
currencyConversionToComboBox.addItem('INR - Indian Rupee (India)')
currencyConversionToComboBox.addItem('IQD - Iraqi Dinar (Iraq)')
currencyConversionToComboBox.addItem('IRR - Iranian Rial (Iran)')
currencyConversionToComboBox.addItem('ISK - Icelandic Króna (Iceland)')
currencyConversionToComboBox.addItem('JEP - Jersey Pound (Jersey)')
currencyConversionToComboBox.addItem('JMD - Jamaican Dollar (Jamaica)')
currencyConversionToComboBox.addItem('JOD - Jordanian Dinar (Jordan)')
currencyConversionToComboBox.addItem('JPY - Japanese Yen (Japan)')
currencyConversionToComboBox.addItem('KES - Kenyan Shilling (Kenya)')
currencyConversionToComboBox.addItem('KGS - Kyrgyzstani Som (Kyrgyzstan)')
currencyConversionToComboBox.addItem('KHR - Cambodian Riel (Cambodia)')
currencyConversionToComboBox.addItem('KID - Kiribati Dollar (Kiribati)')
currencyConversionToComboBox.addItem('KMF - Comorian Franc (Comoros)')
currencyConversionToComboBox.addItem('KRW - South Korean Won (South Korea)')
currencyConversionToComboBox.addItem('KWD - Kuwaiti Dinar (Kuwait)')
currencyConversionToComboBox.addItem('KYD - Cayman Islands Dollar (Cayman Islands)')
currencyConversionToComboBox.addItem('KZT - Kazakhstani Tenge (Kazakhstan)')
currencyConversionToComboBox.addItem('LAK - Lao Kip (Laos)')
currencyConversionToComboBox.addItem('LBP - Lebanese Pound (Lebanon)')
currencyConversionToComboBox.addItem('LKR - Sri Lanka Rupee (Sri Lanka)')
currencyConversionToComboBox.addItem('LRD - Liberian Dollar (Liberia)')
currencyConversionToComboBox.addItem('LSL - Lesotho Loti (Lesotho)')
currencyConversionToComboBox.addItem('LYD - Libyan Dinar (Libya)')
currencyConversionToComboBox.addItem('MAD - Moroccan Dirham (Morocco)')
currencyConversionToComboBox.addItem('MDL - Moldovan Leu (Moldova)')
currencyConversionToComboBox.addItem('MGA - Malagasy Ariary (Madagascar)')
currencyConversionToComboBox.addItem('MKD - Macedonian Denar (North Macedonia)')
currencyConversionToComboBox.addItem('MMK - Burmese Kyat (Myanmar)')
currencyConversionToComboBox.addItem('MNT - Mongolian Tögrög (Mongolia)')
currencyConversionToComboBox.addItem('MOP - Macanese Pataca (Macau)')
currencyConversionToComboBox.addItem('MRU - Mauritanian Ouguiya (Mauritania)')
currencyConversionToComboBox.addItem('MUR - Mauritian Rupee (Mauritius)')
currencyConversionToComboBox.addItem('MVR - Maldivian Rufiyaa (Maldives)')
currencyConversionToComboBox.addItem('MWK - Malawian Kwacha (Malawi)')
currencyConversionToComboBox.addItem('MXN - Mexican Peso (Mexico)')
currencyConversionToComboBox.addItem('MYR - Malaysian Ringgit (Malaysia)')
currencyConversionToComboBox.addItem('MZN - Mozambican Metical (Mozambique)')
currencyConversionToComboBox.addItem('NAD - Namibian Dollar (Namibia)')
currencyConversionToComboBox.addItem('NGN - Nigerian Naira (Nigeria)')
currencyConversionToComboBox.addItem('NIO - Nicaraguan Córdoba (Nicaragua)')
currencyConversionToComboBox.addItem('NOK - Norwegian Krone (Norway)')
currencyConversionToComboBox.addItem('NPR - Nepalese Rupee (Nepal)')
currencyConversionToComboBox.addItem('NZD - New Zealand Dollar (New Zealand)')
currencyConversionToComboBox.addItem('OMR - Omani Rial (Oman)')
currencyConversionToComboBox.addItem('PAB - Panamanian Balboa (Panama)')
currencyConversionToComboBox.addItem('PEN - Peruvian Sol (Peru)')
currencyConversionToComboBox.addItem('PGK - Papua New Guinean Kina (Papua New Guinea)')
currencyConversionToComboBox.addItem('PHP - Philippine Peso (Philippines)')
currencyConversionToComboBox.addItem('PKR - Pakistani Rupee (Pakistan)')
currencyConversionToComboBox.addItem('PLN - Polish Złoty (Poland)')
currencyConversionToComboBox.addItem('PYG - Paraguayan Guaraní (Paraguay)')
currencyConversionToComboBox.addItem('QAR - Qatari Riyal (Qatar)')
currencyConversionToComboBox.addItem('RON - Romanian Leu (Romania)')
currencyConversionToComboBox.addItem('RSD - Serbian Dinar (Serbia)')
currencyConversionToComboBox.addItem('RUB - Russian Ruble (Russia)')
currencyConversionToComboBox.addItem('RWF - Rwandan Franc (Rwanda)')
currencyConversionToComboBox.addItem('SAR - Saudi Riyal (Saudi Arabia)')
currencyConversionToComboBox.addItem('SBD - Solomon Islands Dollar (Solomon Islands)')
currencyConversionToComboBox.addItem('SCR - Seychellois Rupee (Seychelles)')
currencyConversionToComboBox.addItem('SDG - Sudanese Pound (Sudan)')
currencyConversionToComboBox.addItem('SEK - Swedish Krona (Sweden)')
currencyConversionToComboBox.addItem('SGD - Singapore Dollar (Singapore)')
currencyConversionToComboBox.addItem('SHP - Saint Helena Pound (Saint Helena)')
currencyConversionToComboBox.addItem('SLE - Sierra Leonean Leone (Sierra Leone)')
currencyConversionToComboBox.addItem('SOS - Somali Shilling (Somalia)')
currencyConversionToComboBox.addItem('SRD - Surinamese Dollar (Suriname)')
currencyConversionToComboBox.addItem('SSP - South Sudanese Pound (South Sudan)')
currencyConversionToComboBox.addItem('STN - São Tomé and Príncipe Dobra (São Tomé and Príncipe)')
currencyConversionToComboBox.addItem('SYP - Syrian Pound (Syria)')
currencyConversionToComboBox.addItem('SZL - Eswatini Lilangeni (Eswatini)')
currencyConversionToComboBox.addItem('THB - Thai Baht (Thailand)')
currencyConversionToComboBox.addItem('TJS - Tajikistani Somoni (Tajikistan)')
currencyConversionToComboBox.addItem('TMT - Turkmenistan Manat (Turkmenistan)')
currencyConversionToComboBox.addItem('TND - Tunisian Dinar (Tunisia)')
currencyConversionToComboBox.addItem('TOP - Tongan Paʻanga (Tonga)')
currencyConversionToComboBox.addItem('TRY - Turkish Lira (Turkey)')
currencyConversionToComboBox.addItem('TTD - Trinidad and Tobago Dollar (Trinidad and Tobago)')
currencyConversionToComboBox.addItem('TVD - Tuvaluan Dollar (Tuvalu)')
currencyConversionToComboBox.addItem('TWD - New Taiwan Dollar (Taiwan)')
currencyConversionToComboBox.addItem('TZS - Tanzanian Shilling (Tanzania)')
currencyConversionToComboBox.addItem('UAH - Ukrainian Hryvnia (Ukraine)')
currencyConversionToComboBox.addItem('UGX - Ugandan Shilling (Uganda)')
currencyConversionToComboBox.addItem('USD - United States Dollar (United States)')
currencyConversionToComboBox.addItem('UYU - Uruguayan Peso (Uruguay)')
currencyConversionToComboBox.addItem('UZS - Uzbekistani So\'m (Uzbekistan)')
currencyConversionToComboBox.addItem('VES - Venezuelan Bolívar Soberano (Venezuela)')
currencyConversionToComboBox.addItem('VND - Vietnamese Đồng (Vietnam)')
currencyConversionToComboBox.addItem('VUV - Vanuatu Vatu (Vanuatu)')
currencyConversionToComboBox.addItem('WST - Samoan Tālā (Samoa)')
currencyConversionToComboBox.addItem('XAF - Central African CFA Franc (CEMAC)')
currencyConversionToComboBox.addItem('XCD - East Caribbean Dollar (Organisation of Eastern Caribbean States)')
currencyConversionToComboBox.addItem('XDR - Special Drawing Rights (International Monetary Fund)')
currencyConversionToComboBox.addItem('XOF - West African CFA franc (CFA)')
currencyConversionToComboBox.addItem('XPF - CFP Franc (Collectivités d\'Outre-Mer)')
currencyConversionToComboBox.addItem('YER - Yemeni Rial (Yemen)')
currencyConversionToComboBox.addItem('ZAR - South African Rand (South Africa)')
currencyConversionToComboBox.addItem('ZMW - Zambian Kwacha (Zambia)')
currencyConversionToComboBox.addItem('ZWL - Zimbabwean Dollar (Zimbabwe)')
# Output Field
currencyConversionOutputField = QLineEdit(currencyConversionWidget)
currencyConversionOutputField.setFixedSize(480, 60)
currencyConversionOutputField.move(30, 420)
currencyConversionOutputField.setFont(outputFieldFont)
currencyConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
currencyConversionOutputField.setPlaceholderText('Output')
currencyConversionOutputField.setReadOnly(True)
# Paste Output to Input
currencyConversionPasteButton = QPushButton('⇅', currencyConversionWidget)
currencyConversionPasteButton.setFixedSize(60, 270)
currencyConversionPasteButton.move(510, 210)
currencyConversionPasteButton.setFont(conversionPasteButtonFont)
currencyConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def currencyConversionPaste():
    global API_KEY, currencyConversionInput
    currencyConversionFromIndex = currencyConversionFromComboBox.currentIndex()
    currencyConversionToIndex = currencyConversionToComboBox.currentIndex()
    currencyConversionFromComboBox.setCurrentIndex(currencyConversionToIndex)
    currencyConversionToComboBox.setCurrentIndex(currencyConversionFromIndex)
    if currencyConversionInputField.text():
        if currencyConversionInputField.text().endswith('.'):
            currencyConversionInputField.setText(currencyConversionInputField.text().replace('.', ''))
            currencyConversionInput = currencyConversionInput.replace('.', '')
        if API_KEY is None:
            ok = apiDialogBox.exec()
            API_KEY = apiDialogBox.textValue()
            if ok:
                currencyConversionFrom = currencyConversionFromComboBox.currentText()
                currencyConversionFrom = currencyConversionFrom[:3]
                currencyConversionTo = currencyConversionToComboBox.currentText()
                currencyConversionTo = currencyConversionTo[:3]
                url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currencyConversionFrom}/{currencyConversionTo}/{currencyConversionInput}'
                try:
                    response = get(url)
                    data = response.json()
                    if "result" in data and data["result"] != "error":
                        saveAPI(API_KEY)
                        currencyConversionOutputField.setText(str(data["conversion_result"]))
                    else:
                        error_message = data.get("error-type", "Unknown error")
                        API_KEY = ''
                        errorMessageBox.critical(currencyConversionWidget, 'Error', f'An error occurred: {error_message}')
                except Exception as e:
                    errorMessageBox.critical(currencyConversionWidget, 'Error', f'Connection error: {str(e)}')
        else:
            currencyConversionFrom = currencyConversionFromComboBox.currentText()
            currencyConversionFrom = currencyConversionFrom[:3]
            currencyConversionTo = currencyConversionToComboBox.currentText()
            currencyConversionTo = currencyConversionTo[:3]
            url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currencyConversionFrom}/{currencyConversionTo}/{currencyConversionInput}'
            response = get(url)
            data = response.json()
            currencyConversionOutputField.setText(str(data["conversion_result"]))
currencyConversionPasteButton.clicked.connect(currencyConversionPaste)
# Number Pad
# Nine [9]
currencyConversionNineButton = QPushButton('9', currencyConversionWidget)
currencyConversionNineButton.setFixedSize(90, 90)
currencyConversionNineButton.move(300, 510)
currencyConversionNineButton.setFont(numberPadFont)
currencyConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionNine():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '9')
    currencyConversionInput += '9'
currencyConversionNineButton.clicked.connect(currencyConversionNine)
# Eight [8]
currencyConversionEightButton = QPushButton('8', currencyConversionWidget)
currencyConversionEightButton.setFixedSize(90, 90)
currencyConversionEightButton.move(210, 510)
currencyConversionEightButton.setFont(numberPadFont)
currencyConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionEight():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '8')
    currencyConversionInput += '8'
currencyConversionEightButton.clicked.connect(currencyConversionEight)
# Seven [7]
currencyConversionSevenButton = QPushButton('7', currencyConversionWidget)
currencyConversionSevenButton.setFixedSize(90, 90)
currencyConversionSevenButton.move(120, 510)
currencyConversionSevenButton.setFont(numberPadFont)
currencyConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionSeven():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '7')
    currencyConversionInput += '7'
currencyConversionSevenButton.clicked.connect(currencyConversionSeven)
# Six [6]
currencyConversionSixButton = QPushButton('6', currencyConversionWidget)
currencyConversionSixButton.setFixedSize(90, 90)
currencyConversionSixButton.move(300, 600)
currencyConversionSixButton.setFont(numberPadFont)
currencyConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionSix():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '6')
    currencyConversionInput += '6'
currencyConversionSixButton.clicked.connect(currencyConversionSix)
# Five [5]
currencyConversionFiveButton = QPushButton('5', currencyConversionWidget)
currencyConversionFiveButton.setFixedSize(90, 90)
currencyConversionFiveButton.move(210, 600)
currencyConversionFiveButton.setFont(numberPadFont)
currencyConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionFive():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '5')
    currencyConversionInput += '5'
currencyConversionFiveButton.clicked.connect(currencyConversionFive)
# Four [4]
currencyConversionFourButton = QPushButton('4', currencyConversionWidget)
currencyConversionFourButton.setFixedSize(90, 90)
currencyConversionFourButton.move(120, 600)
currencyConversionFourButton.setFont(numberPadFont)
currencyConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionFour():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '4')
    currencyConversionInput += '4'
currencyConversionFourButton.clicked.connect(currencyConversionFour)
# Three [3]
currencyConversionThreeButton = QPushButton('3', currencyConversionWidget)
currencyConversionThreeButton.setFixedSize(90, 90)
currencyConversionThreeButton.move(300, 690)
currencyConversionThreeButton.setFont(numberPadFont)
currencyConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionThree():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '3')
    currencyConversionInput += '3'
currencyConversionThreeButton.clicked.connect(currencyConversionThree)
# Two [2]
currencyConversionTwoButton = QPushButton('2', currencyConversionWidget)
currencyConversionTwoButton.setFixedSize(90, 90)
currencyConversionTwoButton.move(210, 690)
currencyConversionTwoButton.setFont(numberPadFont)
currencyConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionTwo():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '2')
    currencyConversionInput += '2'
currencyConversionTwoButton.clicked.connect(currencyConversionTwo)
# One [1]
currencyConversionOneButton = QPushButton('1', currencyConversionWidget)
currencyConversionOneButton.setFixedSize(90, 90)
currencyConversionOneButton.move(120, 690)
currencyConversionOneButton.setFont(numberPadFont)
currencyConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionOne():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '1')
    currencyConversionInput += '1'
currencyConversionOneButton.clicked.connect(currencyConversionOne)
# Zero [0]
currencyConversionZeroButton = QPushButton('0', currencyConversionWidget)
currencyConversionZeroButton.setFixedSize(90, 90)
currencyConversionZeroButton.move(210, 780)
currencyConversionZeroButton.setFont(numberPadFont)
currencyConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionZero():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '0')
    currencyConversionInput += '0'
currencyConversionZeroButton.clicked.connect(currencyConversionZero)
# Double Zero [00]
currencyConversionDoubleZeroButton = QPushButton('00', currencyConversionWidget)
currencyConversionDoubleZeroButton.setFixedSize(90, 90)
currencyConversionDoubleZeroButton.move(120, 780)
currencyConversionDoubleZeroButton.setFont(numberPadFont)
currencyConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def currencyConversionDoubleZero():
    global currencyConversionInput
    currencyConversionInputField.setText(currencyConversionInputField.text() + '00')
    currencyConversionInput += '00'
currencyConversionDoubleZeroButton.clicked.connect(currencyConversionDoubleZero)
# Point [.]
currencyConversionPointButton = QPushButton('.', currencyConversionWidget)
currencyConversionPointButton.setFixedSize(90, 90)
currencyConversionPointButton.move(300, 780)
currencyConversionPointButton.setFont(numberPadFont)
currencyConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def currencyConversionPoint():
    global currencyConversionInput
    if currencyConversionInputField.text():
        currencyConversionInputField.setText(currencyConversionInputField.text() + '.')
        currencyConversionInput += '.'
    else:
        currencyConversionInputField.setText(currencyConversionInputField.text() + '0.')
        currencyConversionInput += '0.'
currencyConversionPointButton.clicked.connect(currencyConversionPoint)
# Deletion
# All Clear
currencyConversionAllClearButton = QPushButton('AC', currencyConversionWidget)
currencyConversionAllClearButton.setFixedSize(90, 90)
currencyConversionAllClearButton.move(390, 510)
currencyConversionAllClearButton.setFont(operatorButtonFont)
currencyConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def currencyConversionAllClear():
    global currencyConversionInput
    currencyConversionInputField.setText('')
    currencyConversionOutputField.setText('')
    currencyConversionInput = ''
currencyConversionAllClearButton.clicked.connect(currencyConversionAllClear)
# Clear [Backspace]
currencyConversionClearButton = QPushButton('C', currencyConversionWidget)
currencyConversionClearButton.setFixedSize(90, 90)
currencyConversionClearButton.move(390, 600)
currencyConversionClearButton.setFont(operatorButtonFont)
currencyConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def currencyConversionClear():
    global currencyConversionInput
    currencyConversionInputFieldText = currencyConversionInputField.text()
    currencyConversionInputFieldText = currencyConversionInputFieldText[:-1]
    currencyConversionInputField.setText(currencyConversionInputFieldText)
    currencyConversionInput = currencyConversionInput[:-1]
currencyConversionClearButton.clicked.connect(currencyConversionClear)
# Result [=]
currencyConversionResultButton = QPushButton('=', currencyConversionWidget)
currencyConversionResultButton.setFixedSize(90, 180)
currencyConversionResultButton.move(390, 690)
currencyConversionResultButton.setFont(resultButtonsFont)
currencyConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def currencyConversionResult():
    global API_KEY, currencyConversionInput
    if currencyConversionInputField.text():
        if currencyConversionInputField.text().endswith('.'):
            currencyConversionInputField.setText(currencyConversionInputField.text().replace('.', ''))
            currencyConversionInput = currencyConversionInput.replace('.', '')
        if API_KEY == None:
            ok = apiDialogBox.exec()
            API_KEY = apiDialogBox.textValue()
            if ok:
                currencyConversionFrom = currencyConversionFromComboBox.currentText()
                currencyConversionFrom = currencyConversionFrom[:3]
                currencyConversionTo = currencyConversionToComboBox.currentText()
                currencyConversionTo = currencyConversionTo[:3]
                url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currencyConversionFrom}/{currencyConversionTo}/{currencyConversionInput}'
                try:
                    response = get(url)
                    data = response.json()
                    if "result" in data and data["result"] != "error":
                        saveAPI(API_KEY)
                        currencyConversionOutputField.setText(str(data["conversion_result"]))
                    else:
                        error_message = data.get("error-type", "Unknown error")
                        API_KEY = ''
                        errorMessageBox.critical(currencyConversionWidget, 'Error', f'An error occurred: {error_message}')
                except Exception as e:
                    errorMessageBox.critical(currencyConversionWidget, 'Error', f'Connection error: {str(e)}')
        else:
            currencyConversionFrom = currencyConversionFromComboBox.currentText()
            currencyConversionFrom = currencyConversionFrom[:3]
            currencyConversionTo = currencyConversionToComboBox.currentText()
            currencyConversionTo = currencyConversionTo[:3]
            url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currencyConversionFrom}/{currencyConversionTo}/{currencyConversionInput}'
            response = get(url)
            data = response.json()
            currencyConversionOutputField.setText(str(data["conversion_result"]))
currencyConversionResultButton.clicked.connect(currencyConversionResult)
# Note for Currency Conversion
noteLabel = QLabel('<b>⚠️ NOTE:</b> Currency Conversion requires Internet Connection', currencyConversionWidget)
noteLabel.setFixedSize(540, 30)
noteLabel.move(30, 900)
noteLabel.setFont(goToLabelFonts)
noteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Length Conversion Page
# Length Conversion Widget
lengthConversionWidget = QWidget()
stackedWidget.addWidget(lengthConversionWidget)
# Back Button
lengthBackButton = QPushButton('←', lengthConversionWidget)
lengthBackButton.setFixedSize(60, 60)
lengthBackButton.move(30, 30)
lengthBackButton.setFont(mainLabelFont)
def lengthBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
lengthBackButton.clicked.connect(lengthBack)
# Switch to Calculator Button
lengthSwitchToCalculatorButton = QPushButton('⇄', lengthConversionWidget)
lengthSwitchToCalculatorButton.setFixedSize(60, 60)
lengthSwitchToCalculatorButton.move(510, 30)
lengthSwitchToCalculatorButton.setFont(mainLabelFont)
def lengthSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
lengthSwitchToCalculatorButton.clicked.connect(lengthSwitchToCalculator)
# Length Conversion Page Main Label
lengthConversionLabel = QLabel('Length Conversion', lengthConversionWidget)
lengthConversionLabel.setFixedSize(540, 60)
lengthConversionLabel.move(30, 120)
lengthConversionLabel.setFont(conversionsLabelFont)
lengthConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
lengthConversionFromComboBox = QComboBox(lengthConversionWidget)
lengthConversionFromComboBox.setFixedSize(480, 60)
lengthConversionFromComboBox.move(30, 210)
lengthConversionFromComboBox.setFont(comboBoxFont)
lengthConversionFromComboBox.setStyleSheet('padding-left: 10px')
lengthConversionFromComboBox.addItem('Metre (m)')                                                                   # 0
lengthConversionFromComboBox.addItem('Millimetre (mm)')                                                             # 1
lengthConversionFromComboBox.addItem('Centimetre (cm)')                                                             # 2
lengthConversionFromComboBox.addItem('Decimetre (dm)')                                                              # 3
lengthConversionFromComboBox.addItem('Kilometre (km)')                                                              # 4
lengthConversionFromComboBox.addItem('Micrometre (μm)')                                                             # 5
lengthConversionFromComboBox.addItem('Nanometre (nm)')                                                              # 6
lengthConversionFromComboBox.addItem('Picometre (pm)')                                                              # 7
lengthConversionFromComboBox.addItem('Inch (in)')                                                                   # 8
lengthConversionFromComboBox.addItem('Foot (ft)')                                                                   # 9
lengthConversionFromComboBox.addItem('Yard (yd)')                                                                   # 10
lengthConversionFromComboBox.addItem('Mile (mi)')                                                                   # 11
lengthConversionFromComboBox.addItem('Nautical Mile (nmi)')                                                         # 12
# Input Field
lengthConversionInputField = QLineEdit(lengthConversionWidget)
lengthConversionInputField.setPlaceholderText('Input')
lengthConversionInputField.setFixedSize(480, 60)
lengthConversionInputField.move(30, 270)
lengthConversionInputField.setFont(inputFieldFont)
lengthConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
lengthConversionInputField.setReadOnly(True)
# To Combo Box
lengthConversionToComboBox = QComboBox(lengthConversionWidget)
lengthConversionToComboBox.setFixedSize(480, 60)
lengthConversionToComboBox.move(30, 360)
lengthConversionToComboBox.setFont(comboBoxFont)
lengthConversionToComboBox.setStyleSheet('padding-left: 10px')
lengthConversionToComboBox.addItem('Metre (m)')                                                                     # 0
lengthConversionToComboBox.addItem('Millimetre (mm)')                                                               # 1
lengthConversionToComboBox.addItem('Centimetre (cm)')                                                               # 2
lengthConversionToComboBox.addItem('Decimetre (dm)')                                                                # 3
lengthConversionToComboBox.addItem('Kilometre (km)')                                                                # 4
lengthConversionToComboBox.addItem('Micrometre (μm)')                                                               # 5
lengthConversionToComboBox.addItem('Nanometre (nm)')                                                                # 6
lengthConversionToComboBox.addItem('Picometre (pm)')                                                                # 7
lengthConversionToComboBox.addItem('Inch (in)')                                                                     # 8
lengthConversionToComboBox.addItem('Foot (ft)')                                                                     # 9
lengthConversionToComboBox.addItem('Yard (yd)')                                                                     # 10
lengthConversionToComboBox.addItem('Mile (mi)')                                                                     # 11
lengthConversionToComboBox.addItem('Nautical Mile (nmi)')                                                           # 12
# Output Field
lengthConversionOutputField = QLineEdit(lengthConversionWidget)
lengthConversionOutputField.setFixedSize(480, 60)
lengthConversionOutputField.move(30, 420)
lengthConversionOutputField.setFont(outputFieldFont)
lengthConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
lengthConversionOutputField.setPlaceholderText('Output')
lengthConversionOutputField.setReadOnly(True)
# Paste Output to Input
lengthConversionPasteButton = QPushButton('⇅', lengthConversionWidget)
lengthConversionPasteButton.setFixedSize(60, 270)
lengthConversionPasteButton.move(510, 210)
lengthConversionPasteButton.setFont(conversionPasteButtonFont)
lengthConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def lengthConversionPaste():
    global lengthConversionInput
    lengthConversionFromIndex = lengthConversionFromComboBox.currentIndex()
    lengthConversionToIndex = lengthConversionToComboBox.currentIndex()
    lengthConversionFromComboBox.setCurrentIndex(lengthConversionToIndex)
    lengthConversionToComboBox.setCurrentIndex(lengthConversionFromIndex)
    if lengthConversionInputField.text():
        if lengthConversionInputField.text().endswith('.'):
            lengthConversionInputField.setText(lengthConversionInputField.text().replace('.', ''))
            lengthConversionInput = lengthConversionInput.replace('.', '')
        lengthConversionFrom = lengthConversionFromComboBox.currentIndex()
        lengthConversionTo = lengthConversionToComboBox.currentIndex()
        lengthConversionKey = (lengthConversionFrom, lengthConversionTo)
        lengthConversionFactor = lengthConversionFactors[lengthConversionKey]
        lengthConversionOutput = float(lengthConversionInput) * lengthConversionFactor
        lengthConversionOutputField.setText(str(lengthConversionOutput))
lengthConversionPasteButton.clicked.connect(lengthConversionPaste)
# Number Pad
# Nine [9]
lengthConversionNineButton = QPushButton('9', lengthConversionWidget)
lengthConversionNineButton.setFixedSize(90, 90)
lengthConversionNineButton.move(300, 510)
lengthConversionNineButton.setFont(numberPadFont)
lengthConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionNine():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '9')
    lengthConversionInput += '9'
lengthConversionNineButton.clicked.connect(lengthConversionNine)
# Eight [8]
lengthConversionEightButton = QPushButton('8', lengthConversionWidget)
lengthConversionEightButton.setFixedSize(90, 90)
lengthConversionEightButton.move(210, 510)
lengthConversionEightButton.setFont(numberPadFont)
lengthConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionEight():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '8')
    lengthConversionInput += '8'
lengthConversionEightButton.clicked.connect(lengthConversionEight)
# Seven [7]
lengthConversionSevenButton = QPushButton('7', lengthConversionWidget)
lengthConversionSevenButton.setFixedSize(90, 90)
lengthConversionSevenButton.move(120, 510)
lengthConversionSevenButton.setFont(numberPadFont)
lengthConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionSeven():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '7')
    lengthConversionInput += '7'
lengthConversionSevenButton.clicked.connect(lengthConversionSeven)
# Six [6]
lengthConversionSixButton = QPushButton('6', lengthConversionWidget)
lengthConversionSixButton.setFixedSize(90, 90)
lengthConversionSixButton.move(300, 600)
lengthConversionSixButton.setFont(numberPadFont)
lengthConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionSix():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '6')
    lengthConversionInput += '6'
lengthConversionSixButton.clicked.connect(lengthConversionSix)
# Five [5]
lengthConversionFiveButton = QPushButton('5', lengthConversionWidget)
lengthConversionFiveButton.setFixedSize(90, 90)
lengthConversionFiveButton.move(210, 600)
lengthConversionFiveButton.setFont(numberPadFont)
lengthConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionFive():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '5')
    lengthConversionInput += '5'
lengthConversionFiveButton.clicked.connect(lengthConversionFive)
# Four [4]
lengthConversionFourButton = QPushButton('4', lengthConversionWidget)
lengthConversionFourButton.setFixedSize(90, 90)
lengthConversionFourButton.move(120, 600)
lengthConversionFourButton.setFont(numberPadFont)
lengthConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionFour():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '4')
    lengthConversionInput += '4'
lengthConversionFourButton.clicked.connect(lengthConversionFour)
# Three [3]
lengthConversionThreeButton = QPushButton('3', lengthConversionWidget)
lengthConversionThreeButton.setFixedSize(90, 90)
lengthConversionThreeButton.move(300, 690)
lengthConversionThreeButton.setFont(numberPadFont)
lengthConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionThree():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '3')
    lengthConversionInput += '3'
lengthConversionThreeButton.clicked.connect(lengthConversionThree)
# Two [2]
lengthConversionTwoButton = QPushButton('2', lengthConversionWidget)
lengthConversionTwoButton.setFixedSize(90, 90)
lengthConversionTwoButton.move(210, 690)
lengthConversionTwoButton.setFont(numberPadFont)
lengthConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionTwo():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '2')
    lengthConversionInput += '2'
lengthConversionTwoButton.clicked.connect(lengthConversionTwo)
# One [1]
lengthConversionOneButton = QPushButton('1', lengthConversionWidget)
lengthConversionOneButton.setFixedSize(90, 90)
lengthConversionOneButton.move(120, 690)
lengthConversionOneButton.setFont(numberPadFont)
lengthConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionOne():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '1')
    lengthConversionInput += '1'
lengthConversionOneButton.clicked.connect(lengthConversionOne)
# Zero [0]
lengthConversionZeroButton = QPushButton('0', lengthConversionWidget)
lengthConversionZeroButton.setFixedSize(90, 90)
lengthConversionZeroButton.move(210, 780)
lengthConversionZeroButton.setFont(numberPadFont)
lengthConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionZero():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '0')
    lengthConversionInput += '0'
lengthConversionZeroButton.clicked.connect(lengthConversionZero)
# Double Zero [00]
lengthConversionDoubleZeroButton = QPushButton('00', lengthConversionWidget)
lengthConversionDoubleZeroButton.setFixedSize(90, 90)
lengthConversionDoubleZeroButton.move(120, 780)
lengthConversionDoubleZeroButton.setFont(numberPadFont)
lengthConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def lengthConversionDoubleZero():
    global lengthConversionInput
    lengthConversionInputField.setText(lengthConversionInputField.text() + '00')
    lengthConversionInput += '00'
lengthConversionDoubleZeroButton.clicked.connect(lengthConversionDoubleZero)
# Point [.]
lengthConversionPointButton = QPushButton('.', lengthConversionWidget)
lengthConversionPointButton.setFixedSize(90, 90)
lengthConversionPointButton.move(300, 780)
lengthConversionPointButton.setFont(numberPadFont)
lengthConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def lengthConversionPoint():
    global lengthConversionInput
    if lengthConversionInputField.text():
        lengthConversionInputField.setText(lengthConversionInputField.text() + '.')
        lengthConversionInput += '.'
    else:
        lengthConversionInputField.setText(lengthConversionInputField.text() + '0.')
        lengthConversionInput += '0.'
lengthConversionPointButton.clicked.connect(lengthConversionPoint)
# Deletion
# All Clear
lengthConversionAllClearButton = QPushButton('AC', lengthConversionWidget)
lengthConversionAllClearButton.setFixedSize(90, 90)
lengthConversionAllClearButton.move(390, 510)
lengthConversionAllClearButton.setFont(operatorButtonFont)
lengthConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def lengthConversionAllClear():
    global lengthConversionInput
    lengthConversionInputField.setText('')
    lengthConversionOutputField.setText('')
    lengthConversionInput = ''
lengthConversionAllClearButton.clicked.connect(lengthConversionAllClear)
# Clear [Backspace]
lengthConversionClearButton = QPushButton('C', lengthConversionWidget)
lengthConversionClearButton.setFixedSize(90, 90)
lengthConversionClearButton.move(390, 600)
lengthConversionClearButton.setFont(operatorButtonFont)
lengthConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def lengthConversionClear():
    global lengthConversionInput
    lengthConversionInputFieldText = lengthConversionInputField.text()
    lengthConversionInputFieldText = lengthConversionInputFieldText[:-1]
    lengthConversionInputField.setText(lengthConversionInputFieldText)
    lengthConversionInput = lengthConversionInput[:-1]
lengthConversionClearButton.clicked.connect(lengthConversionClear)
# Result [=]
lengthConversionResultButton = QPushButton('=', lengthConversionWidget)
lengthConversionResultButton.setFixedSize(90, 180)
lengthConversionResultButton.move(390, 690)
lengthConversionResultButton.setFont(resultButtonsFont)
lengthConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def lengthConversionResult():
    global lengthConversionInput
    if lengthConversionInputField.text():
        if lengthConversionInputField.text().endswith('.'):
            lengthConversionInputField.setText(lengthConversionInputField.text().replace('.', ''))
            lengthConversionInput = lengthConversionInput.replace('.', '')
        lengthConversionFrom = lengthConversionFromComboBox.currentIndex()
        lengthConversionTo = lengthConversionToComboBox.currentIndex()
        lengthConversionKey = (lengthConversionFrom, lengthConversionTo)
        lengthConversionFactor = lengthConversionFactors[lengthConversionKey]
        lengthConversionOutput = float(lengthConversionInput) * lengthConversionFactor
        lengthConversionOutputField.setText(str(lengthConversionOutput))
lengthConversionResultButton.clicked.connect(lengthConversionResult)

# Area Conversion Page
# Area Conversion Widget
areaConversionWidget = QWidget()
stackedWidget.addWidget(areaConversionWidget)
# Back Button
areaBackButton = QPushButton('←', areaConversionWidget)
areaBackButton.setFixedSize(60, 60)
areaBackButton.move(30, 30)
areaBackButton.setFont(mainLabelFont)
def areaBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
areaBackButton.clicked.connect(areaBack)
# Switch to Calculator Button
areaSwitchToCalculatorButton = QPushButton('⇄', areaConversionWidget)
areaSwitchToCalculatorButton.setFixedSize(60, 60)
areaSwitchToCalculatorButton.move(510, 30)
areaSwitchToCalculatorButton.setFont(mainLabelFont)
def areaSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
areaSwitchToCalculatorButton.clicked.connect(areaSwitchToCalculator)
# Area Conversion Page Main Label
areaConversionLabel = QLabel('Area Conversion', areaConversionWidget)
areaConversionLabel.setFixedSize(540, 60)
areaConversionLabel.move(30, 120)
areaConversionLabel.setFont(conversionsLabelFont)
areaConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
areaConversionFromComboBox = QComboBox(areaConversionWidget)
areaConversionFromComboBox.setFixedSize(480, 60)
areaConversionFromComboBox.move(30, 210)
areaConversionFromComboBox.setFont(comboBoxFont)
areaConversionFromComboBox.setStyleSheet('padding-left: 10px')
areaConversionFromComboBox.addItem('Square Metre (m²)')                                                             # 0
areaConversionFromComboBox.addItem('Square Decimetre (dm²)')                                                        # 1
areaConversionFromComboBox.addItem('Square Centimetre (cm²)')                                                       # 2
areaConversionFromComboBox.addItem('Square Millimetre (mm²)')                                                       # 3
areaConversionFromComboBox.addItem('Square Kilometre (km²)')                                                        # 4
areaConversionFromComboBox.addItem('Square Inch (in²)')                                                             # 5
areaConversionFromComboBox.addItem('Square Foot (ft²)')                                                             # 6
areaConversionFromComboBox.addItem('Square Mile (mi²)')                                                             # 7
areaConversionFromComboBox.addItem('Acre (ac)')                                                                     # 8
areaConversionFromComboBox.addItem('Hectare (ha)')                                                                  # 9
# Input Field
areaConversionInputField = QLineEdit(areaConversionWidget)
areaConversionInputField.setPlaceholderText('Input')
areaConversionInputField.setFixedSize(480, 60)
areaConversionInputField.move(30, 270)
areaConversionInputField.setFont(inputFieldFont)
areaConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
areaConversionInputField.setReadOnly(True)
# To Combo Box
areaConversionToComboBox = QComboBox(areaConversionWidget)
areaConversionToComboBox.setFixedSize(480, 60)
areaConversionToComboBox.move(30, 360)
areaConversionToComboBox.setFont(comboBoxFont)
areaConversionToComboBox.setStyleSheet('padding-left: 10px')
areaConversionToComboBox.addItem('Square Metre (m²)')                                                               # 0
areaConversionToComboBox.addItem('Square Decimetre (dm²)')                                                          # 1
areaConversionToComboBox.addItem('Square Centimetre (cm²)')                                                         # 2
areaConversionToComboBox.addItem('Square Millimetre (mm²)')                                                         # 3
areaConversionToComboBox.addItem('Square Kilometre (km²)')                                                          # 4
areaConversionToComboBox.addItem('Square Inch (in²)')                                                               # 5
areaConversionToComboBox.addItem('Square Foot (ft²)')                                                               # 6
areaConversionToComboBox.addItem('Square Mile (mi²)')                                                               # 7
areaConversionToComboBox.addItem('Acre (ac)')                                                                       # 8
areaConversionToComboBox.addItem('Hectare (ha)')                                                                    # 9
# Output Field
areaConversionOutputField = QLineEdit(areaConversionWidget)
areaConversionOutputField.setFixedSize(480, 60)
areaConversionOutputField.move(30, 420)
areaConversionOutputField.setFont(outputFieldFont)
areaConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
areaConversionOutputField.setPlaceholderText('Output')
areaConversionOutputField.setReadOnly(True)
# Paste Output to Input
areaConversionPasteButton = QPushButton('⇅', areaConversionWidget)
areaConversionPasteButton.setFixedSize(60, 270)
areaConversionPasteButton.move(510, 210)
areaConversionPasteButton.setFont(conversionPasteButtonFont)
areaConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def areaConversionPaste():
    global areaConversionInput
    areaConversionFromIndex = areaConversionFromComboBox.currentIndex()
    areaConversionToIndex = areaConversionToComboBox.currentIndex()
    areaConversionFromComboBox.setCurrentIndex(areaConversionToIndex)
    areaConversionToComboBox.setCurrentIndex(areaConversionFromIndex)
    if areaConversionInputField.text():
        if areaConversionInputField.text().endswith('.'):
            areaConversionInputField.setText(areaConversionInputField.text().replace('.', ''))
            areaConversionInput = areaConversionInput.replace('.', '')
        areaConversionFrom = areaConversionFromComboBox.currentIndex()
        areaConversionTo = areaConversionToComboBox.currentIndex()
        areaConversionKey = (areaConversionFrom, areaConversionTo)
        areaConversionFactor = areaConversionFactors[areaConversionKey]
        areaConversionOutput = float(areaConversionInput) * areaConversionFactor
        areaConversionOutputField.setText(str(areaConversionOutput))
areaConversionPasteButton.clicked.connect(areaConversionPaste)
# Number Pad
# Nine [9]
areaConversionNineButton = QPushButton('9', areaConversionWidget)
areaConversionNineButton.setFixedSize(90, 90)
areaConversionNineButton.move(300, 510)
areaConversionNineButton.setFont(numberPadFont)
areaConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionNine():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '9')
    areaConversionInput += '9'
areaConversionNineButton.clicked.connect(areaConversionNine)
# Eight [8]
areaConversionEightButton = QPushButton('8', areaConversionWidget)
areaConversionEightButton.setFixedSize(90, 90)
areaConversionEightButton.move(210, 510)
areaConversionEightButton.setFont(numberPadFont)
areaConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionEight():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '8')
    areaConversionInput += '8'
areaConversionEightButton.clicked.connect(areaConversionEight)
# Seven [7]
areaConversionSevenButton = QPushButton('7', areaConversionWidget)
areaConversionSevenButton.setFixedSize(90, 90)
areaConversionSevenButton.move(120, 510)
areaConversionSevenButton.setFont(numberPadFont)
areaConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionSeven():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '7')
    areaConversionInput += '7'
areaConversionSevenButton.clicked.connect(areaConversionSeven)
# Six [6]
areaConversionSixButton = QPushButton('6', areaConversionWidget)
areaConversionSixButton.setFixedSize(90, 90)
areaConversionSixButton.move(300, 600)
areaConversionSixButton.setFont(numberPadFont)
areaConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionSix():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '6')
    areaConversionInput += '6'
areaConversionSixButton.clicked.connect(areaConversionSix)
# Five [5]
areaConversionFiveButton = QPushButton('5', areaConversionWidget)
areaConversionFiveButton.setFixedSize(90, 90)
areaConversionFiveButton.move(210, 600)
areaConversionFiveButton.setFont(numberPadFont)
areaConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionFive():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '5')
    areaConversionInput += '5'
areaConversionFiveButton.clicked.connect(areaConversionFive)
# Four [4]
areaConversionFourButton = QPushButton('4', areaConversionWidget)
areaConversionFourButton.setFixedSize(90, 90)
areaConversionFourButton.move(120, 600)
areaConversionFourButton.setFont(numberPadFont)
areaConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionFour():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '4')
    areaConversionInput += '4'
areaConversionFourButton.clicked.connect(areaConversionFour)
# Three [3]
areaConversionThreeButton = QPushButton('3', areaConversionWidget)
areaConversionThreeButton.setFixedSize(90, 90)
areaConversionThreeButton.move(300, 690)
areaConversionThreeButton.setFont(numberPadFont)
areaConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionThree():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '3')
    areaConversionInput += '3'
areaConversionThreeButton.clicked.connect(areaConversionThree)
# Two [2]
areaConversionTwoButton = QPushButton('2', areaConversionWidget)
areaConversionTwoButton.setFixedSize(90, 90)
areaConversionTwoButton.move(210, 690)
areaConversionTwoButton.setFont(numberPadFont)
areaConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionTwo():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '2')
    areaConversionInput += '2'
areaConversionTwoButton.clicked.connect(areaConversionTwo)
# One [1]
areaConversionOneButton = QPushButton('1', areaConversionWidget)
areaConversionOneButton.setFixedSize(90, 90)
areaConversionOneButton.move(120, 690)
areaConversionOneButton.setFont(numberPadFont)
areaConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionOne():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '1')
    areaConversionInput += '1'
areaConversionOneButton.clicked.connect(areaConversionOne)
# Zero [0]
areaConversionZeroButton = QPushButton('0', areaConversionWidget)
areaConversionZeroButton.setFixedSize(90, 90)
areaConversionZeroButton.move(210, 780)
areaConversionZeroButton.setFont(numberPadFont)
areaConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionZero():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '0')
    areaConversionInput += '0'
areaConversionZeroButton.clicked.connect(areaConversionZero)
# Double Zero [00]
areaConversionDoubleZeroButton = QPushButton('00', areaConversionWidget)
areaConversionDoubleZeroButton.setFixedSize(90, 90)
areaConversionDoubleZeroButton.move(120, 780)
areaConversionDoubleZeroButton.setFont(numberPadFont)
areaConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def areaConversionDoubleZero():
    global areaConversionInput
    areaConversionInputField.setText(areaConversionInputField.text() + '00')
    areaConversionInput += '00'
areaConversionDoubleZeroButton.clicked.connect(areaConversionDoubleZero)
# Point [.]
areaConversionPointButton = QPushButton('.', areaConversionWidget)
areaConversionPointButton.setFixedSize(90, 90)
areaConversionPointButton.move(300, 780)
areaConversionPointButton.setFont(numberPadFont)
areaConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def areaConversionPoint():
    global areaConversionInput
    if areaConversionInputField.text():
        areaConversionInputField.setText(areaConversionInputField.text() + '.')
        areaConversionInput += '.'
    else:
        areaConversionInputField.setText(areaConversionInputField.text() + '0.')
        areaConversionInput += '0.'
areaConversionPointButton.clicked.connect(areaConversionPoint)
# Deletion
# All Clear
areaConversionAllClearButton = QPushButton('AC', areaConversionWidget)
areaConversionAllClearButton.setFixedSize(90, 90)
areaConversionAllClearButton.move(390, 510)
areaConversionAllClearButton.setFont(operatorButtonFont)
areaConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def areaConversionAllClear():
    global areaConversionInput
    areaConversionInputField.setText('')
    areaConversionOutputField.setText('')
    areaConversionInput = ''
areaConversionAllClearButton.clicked.connect(areaConversionAllClear)
# Clear [Backspace]
areaConversionClearButton = QPushButton('C', areaConversionWidget)
areaConversionClearButton.setFixedSize(90, 90)
areaConversionClearButton.move(390, 600)
areaConversionClearButton.setFont(operatorButtonFont)
areaConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def areaConversionClear():
    global areaConversionInput
    areaConversionInputFieldText = areaConversionInputField.text()
    areaConversionInputFieldText = areaConversionInputFieldText[:-1]
    areaConversionInputField.setText(areaConversionInputFieldText)
    areaConversionInput = areaConversionInput[:-1]
areaConversionClearButton.clicked.connect(areaConversionClear)
# Result [=]
areaConversionResultButton = QPushButton('=', areaConversionWidget)
areaConversionResultButton.setFixedSize(90, 180)
areaConversionResultButton.move(390, 690)
areaConversionResultButton.setFont(resultButtonsFont)
areaConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def areaConversionResult():
    global areaConversionInput
    if areaConversionInputField.text():
        if areaConversionInputField.text().endswith('.'):
            areaConversionInputField.setText(areaConversionInputField.text().replace('.', ''))
            areaConversionInput = areaConversionInput.replace('.', '')
        areaConversionFrom = areaConversionFromComboBox.currentIndex()
        areaConversionTo = areaConversionToComboBox.currentIndex()
        areaConversionKey = (areaConversionFrom, areaConversionTo)
        areaConversionFactor = areaConversionFactors[areaConversionKey]
        areaConversionOutput = float(areaConversionInput) * areaConversionFactor
        areaConversionOutputField.setText(str(areaConversionOutput))
areaConversionResultButton.clicked.connect(areaConversionResult)

# Volume Conversion Page
# Volume Conversion Widget
volumeConversionWidget = QWidget()
stackedWidget.addWidget(volumeConversionWidget)
# Back Button
volumeBackButton = QPushButton('←', volumeConversionWidget)
volumeBackButton.setFixedSize(60, 60)
volumeBackButton.move(30, 30)
volumeBackButton.setFont(mainLabelFont)
def volumeBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
volumeBackButton.clicked.connect(volumeBack)
# Switch to Calculator Button
volumeSwitchToCalculatorButton = QPushButton('⇄', volumeConversionWidget)
volumeSwitchToCalculatorButton.setFixedSize(60, 60)
volumeSwitchToCalculatorButton.move(510, 30)
volumeSwitchToCalculatorButton.setFont(mainLabelFont)
def volumeSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
volumeSwitchToCalculatorButton.clicked.connect(volumeSwitchToCalculator)
# Volume Conversion Page Main Label
volumeConversionLabel = QLabel('Volume Conversion', volumeConversionWidget)
volumeConversionLabel.setFixedSize(540, 60)
volumeConversionLabel.move(30, 120)
volumeConversionLabel.setFont(conversionsLabelFont)
volumeConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
volumeConversionFromComboBox = QComboBox(volumeConversionWidget)
volumeConversionFromComboBox.setFixedSize(480, 60)
volumeConversionFromComboBox.move(30, 210)
volumeConversionFromComboBox.setFont(comboBoxFont)
volumeConversionFromComboBox.setStyleSheet('padding-left: 10px')
volumeConversionFromComboBox.addItem('Cubic Metre (m³)')                                                            # 0
volumeConversionFromComboBox.addItem('Cubic Decimetre (dm³)')                                                       # 1
volumeConversionFromComboBox.addItem('Cubic Centimetre (cm³)')                                                      # 2
volumeConversionFromComboBox.addItem('Cubic Millimetre (mm³)')                                                      # 3
volumeConversionFromComboBox.addItem('Litre (L)')                                                                   # 4
volumeConversionFromComboBox.addItem('Millilitre (mL)')                                                             # 5
volumeConversionFromComboBox.addItem('Cubic Inch (in³)')                                                            # 6
volumeConversionFromComboBox.addItem('Cubic Foot (ft³)')                                                            # 7
volumeConversionFromComboBox.addItem('Fluid Ounce (fl. oz)')                                                        # 8
volumeConversionFromComboBox.addItem('Gallon (gal)')                                                                # 9
# Input Field
volumeConversionInputField = QLineEdit(volumeConversionWidget)
volumeConversionInputField.setPlaceholderText('Input')
volumeConversionInputField.setFixedSize(480, 60)
volumeConversionInputField.move(30, 270)
volumeConversionInputField.setFont(inputFieldFont)
volumeConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
volumeConversionInputField.setReadOnly(True)
# To Combo Box
volumeConversionToComboBox = QComboBox(volumeConversionWidget)
volumeConversionToComboBox.setFixedSize(480, 60)
volumeConversionToComboBox.move(30, 360)
volumeConversionToComboBox.setFont(comboBoxFont)
volumeConversionToComboBox.setStyleSheet('padding-left: 10px')
volumeConversionToComboBox.addItem('Cubic Metre (m³)')                                                              # 0
volumeConversionToComboBox.addItem('Cubic Decimetre (dm³)')                                                         # 1
volumeConversionToComboBox.addItem('Cubic Centimetre (cm³)')                                                        # 2
volumeConversionToComboBox.addItem('Cubic Millimetre (mm³)')                                                        # 3
volumeConversionToComboBox.addItem('Litre (L)')                                                                     # 4
volumeConversionToComboBox.addItem('Millilitre (mL)')                                                               # 5
volumeConversionToComboBox.addItem('Cubic Inch (in³)')                                                              # 6
volumeConversionToComboBox.addItem('Cubic Foot (ft³)')                                                              # 7
volumeConversionToComboBox.addItem('Fluid Ounce (fl. oz)')                                                          # 8
volumeConversionToComboBox.addItem('Gallon (gal)')                                                                  # 9
# Output Field
volumeConversionOutputField = QLineEdit(volumeConversionWidget)
volumeConversionOutputField.setFixedSize(480, 60)
volumeConversionOutputField.move(30, 420)
volumeConversionOutputField.setFont(outputFieldFont)
volumeConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
volumeConversionOutputField.setPlaceholderText('Output')
volumeConversionOutputField.setReadOnly(True)
# Paste Output to Input
volumeConversionPasteButton = QPushButton('⇅', volumeConversionWidget)
volumeConversionPasteButton.setFixedSize(60, 270)
volumeConversionPasteButton.move(510, 210)
volumeConversionPasteButton.setFont(conversionPasteButtonFont)
volumeConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def volumeConversionPaste():
    global volumeConversionInput
    volumeConversionFromIndex = volumeConversionFromComboBox.currentIndex()
    volumeConversionToIndex = volumeConversionToComboBox.currentIndex()
    volumeConversionFromComboBox.setCurrentIndex(volumeConversionToIndex)
    volumeConversionToComboBox.setCurrentIndex(volumeConversionFromIndex)
    if volumeConversionInputField.text():
        if volumeConversionInputField.text().endswith('.'):
            volumeConversionInputField.setText(volumeConversionInputField.text().replace('.', ''))
            volumeConversionInput = volumeConversionInput.replace('.', '')
        volumeConversionFrom = volumeConversionFromComboBox.currentIndex()
        volumeConversionTo = volumeConversionToComboBox.currentIndex()
        volumeConversionKey = (volumeConversionFrom, volumeConversionTo)
        volumeConversionFactor = volumeConversionFactors[volumeConversionKey]
        volumeConversionOutput = float(volumeConversionInput) * volumeConversionFactor
        volumeConversionOutputField.setText(str(volumeConversionOutput))
volumeConversionPasteButton.clicked.connect(volumeConversionPaste)
# Number Pad
# Nine [9]
volumeConversionNineButton = QPushButton('9', volumeConversionWidget)
volumeConversionNineButton.setFixedSize(90, 90)
volumeConversionNineButton.move(300, 510)
volumeConversionNineButton.setFont(numberPadFont)
volumeConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionNine():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '9')
    volumeConversionInput += '9'
volumeConversionNineButton.clicked.connect(volumeConversionNine)
# Eight [8]
volumeConversionEightButton = QPushButton('8', volumeConversionWidget)
volumeConversionEightButton.setFixedSize(90, 90)
volumeConversionEightButton.move(210, 510)
volumeConversionEightButton.setFont(numberPadFont)
volumeConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionEight():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '8')
    volumeConversionInput += '8'
volumeConversionEightButton.clicked.connect(volumeConversionEight)
# Seven [7]
volumeConversionSevenButton = QPushButton('7', volumeConversionWidget)
volumeConversionSevenButton.setFixedSize(90, 90)
volumeConversionSevenButton.move(120, 510)
volumeConversionSevenButton.setFont(numberPadFont)
volumeConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionSeven():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '7')
    volumeConversionInput += '7'
volumeConversionSevenButton.clicked.connect(volumeConversionSeven)
# Six [6]
volumeConversionSixButton = QPushButton('6', volumeConversionWidget)
volumeConversionSixButton.setFixedSize(90, 90)
volumeConversionSixButton.move(300, 600)
volumeConversionSixButton.setFont(numberPadFont)
volumeConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionSix():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '6')
    volumeConversionInput += '6'
volumeConversionSixButton.clicked.connect(volumeConversionSix)
# Five [5]
volumeConversionFiveButton = QPushButton('5', volumeConversionWidget)
volumeConversionFiveButton.setFixedSize(90, 90)
volumeConversionFiveButton.move(210, 600)
volumeConversionFiveButton.setFont(numberPadFont)
volumeConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionFive():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '5')
    volumeConversionInput += '5'
volumeConversionFiveButton.clicked.connect(volumeConversionFive)
# Four [4]
volumeConversionFourButton = QPushButton('4', volumeConversionWidget)
volumeConversionFourButton.setFixedSize(90, 90)
volumeConversionFourButton.move(120, 600)
volumeConversionFourButton.setFont(numberPadFont)
volumeConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionFour():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '4')
    volumeConversionInput += '4'
volumeConversionFourButton.clicked.connect(volumeConversionFour)
# Three [3]
volumeConversionThreeButton = QPushButton('3', volumeConversionWidget)
volumeConversionThreeButton.setFixedSize(90, 90)
volumeConversionThreeButton.move(300, 690)
volumeConversionThreeButton.setFont(numberPadFont)
volumeConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionThree():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '3')
    volumeConversionInput += '3'
volumeConversionThreeButton.clicked.connect(volumeConversionThree)
# Two [2]
volumeConversionTwoButton = QPushButton('2', volumeConversionWidget)
volumeConversionTwoButton.setFixedSize(90, 90)
volumeConversionTwoButton.move(210, 690)
volumeConversionTwoButton.setFont(numberPadFont)
volumeConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionTwo():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '2')
    volumeConversionInput += '2'
volumeConversionTwoButton.clicked.connect(volumeConversionTwo)
# One [1]
volumeConversionOneButton = QPushButton('1', volumeConversionWidget)
volumeConversionOneButton.setFixedSize(90, 90)
volumeConversionOneButton.move(120, 690)
volumeConversionOneButton.setFont(numberPadFont)
volumeConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionOne():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '1')
    volumeConversionInput += '1'
volumeConversionOneButton.clicked.connect(volumeConversionOne)
# Zero [0]
volumeConversionZeroButton = QPushButton('0', volumeConversionWidget)
volumeConversionZeroButton.setFixedSize(90, 90)
volumeConversionZeroButton.move(210, 780)
volumeConversionZeroButton.setFont(numberPadFont)
volumeConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionZero():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '0')
    volumeConversionInput += '0'
volumeConversionZeroButton.clicked.connect(volumeConversionZero)
# Double Zero [00]
volumeConversionDoubleZeroButton = QPushButton('00', volumeConversionWidget)
volumeConversionDoubleZeroButton.setFixedSize(90, 90)
volumeConversionDoubleZeroButton.move(120, 780)
volumeConversionDoubleZeroButton.setFont(numberPadFont)
volumeConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def volumeConversionDoubleZero():
    global volumeConversionInput
    volumeConversionInputField.setText(volumeConversionInputField.text() + '00')
    volumeConversionInput += '00'
volumeConversionDoubleZeroButton.clicked.connect(volumeConversionDoubleZero)
# Point [.]
volumeConversionPointButton = QPushButton('.', volumeConversionWidget)
volumeConversionPointButton.setFixedSize(90, 90)
volumeConversionPointButton.move(300, 780)
volumeConversionPointButton.setFont(numberPadFont)
volumeConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def volumeConversionPoint():
    global volumeConversionInput
    if volumeConversionInputField.text():
        volumeConversionInputField.setText(volumeConversionInputField.text() + '.')
        volumeConversionInput += '.'
    else:
        volumeConversionInputField.setText(volumeConversionInputField.text() + '0.')
        volumeConversionInput += '0.'
volumeConversionPointButton.clicked.connect(volumeConversionPoint)
# Deletion
# All Clear
volumeConversionAllClearButton = QPushButton('AC', volumeConversionWidget)
volumeConversionAllClearButton.setFixedSize(90, 90)
volumeConversionAllClearButton.move(390, 510)
volumeConversionAllClearButton.setFont(operatorButtonFont)
volumeConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def volumeConversionAllClear():
    global volumeConversionInput
    volumeConversionInputField.setText('')
    volumeConversionOutputField.setText('')
    volumeConversionInput = ''
volumeConversionAllClearButton.clicked.connect(volumeConversionAllClear)
# Clear [Backspace]
volumeConversionClearButton = QPushButton('C', volumeConversionWidget)
volumeConversionClearButton.setFixedSize(90, 90)
volumeConversionClearButton.move(390, 600)
volumeConversionClearButton.setFont(operatorButtonFont)
volumeConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def volumeConversionClear():
    global volumeConversionInput
    volumeConversionInputFieldText = volumeConversionInputField.text()
    volumeConversionInputFieldText = volumeConversionInputFieldText[:-1]
    volumeConversionInputField.setText(volumeConversionInputFieldText)
    volumeConversionInput = volumeConversionInput[:-1]
volumeConversionClearButton.clicked.connect(volumeConversionClear)
# Result [=]
volumeConversionResultButton = QPushButton('=', volumeConversionWidget)
volumeConversionResultButton.setFixedSize(90, 180)
volumeConversionResultButton.move(390, 690)
volumeConversionResultButton.setFont(resultButtonsFont)
volumeConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def volumeConversionResult():
    global volumeConversionInput
    if volumeConversionInputField.text():
        if volumeConversionInputField.text().endswith('.'):
            volumeConversionInputField.setText(volumeConversionInputField.text().replace('.', ''))
            volumeConversionInput = volumeConversionInput.replace('.', '')
        volumeConversionFrom = volumeConversionFromComboBox.currentIndex()
        volumeConversionTo = volumeConversionToComboBox.currentIndex()
        volumeConversionKey = (volumeConversionFrom, volumeConversionTo)
        volumeConversionFactor = volumeConversionFactors[volumeConversionKey]
        volumeConversionOutput = float(volumeConversionInput) * volumeConversionFactor
        volumeConversionOutputField.setText(str(volumeConversionOutput))
volumeConversionResultButton.clicked.connect(volumeConversionResult)

# Weight Conversion Page
# Weight Conversion Widget
weightConversionWidget = QWidget()
stackedWidget.addWidget(weightConversionWidget)
# Back Button
weightBackButton = QPushButton('←', weightConversionWidget)
weightBackButton.setFixedSize(60, 60)
weightBackButton.move(30, 30)
weightBackButton.setFont(mainLabelFont)
def weightBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
weightBackButton.clicked.connect(weightBack)
# Switch to Calculator Button
weightSwitchToCalculatorButton = QPushButton('⇄', weightConversionWidget)
weightSwitchToCalculatorButton.setFixedSize(60, 60)
weightSwitchToCalculatorButton.move(510, 30)
weightSwitchToCalculatorButton.setFont(mainLabelFont)
def weightSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
weightSwitchToCalculatorButton.clicked.connect(weightSwitchToCalculator)
# Weight Conversion Page Main Label
weightConversionLabel = QLabel('Weight Conversion', weightConversionWidget)
weightConversionLabel.setFixedSize(540, 60)
weightConversionLabel.move(30, 120)
weightConversionLabel.setFont(conversionsLabelFont)
weightConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
weightConversionFromComboBox = QComboBox(weightConversionWidget)
weightConversionFromComboBox.setFixedSize(480, 60)
weightConversionFromComboBox.move(30, 210)
weightConversionFromComboBox.setFont(comboBoxFont)
weightConversionFromComboBox.setStyleSheet('padding-left: 10px')
weightConversionFromComboBox.addItem('Gram (g)')                                                                    # 0
weightConversionFromComboBox.addItem('Kilogram (kg)')                                                               # 1
weightConversionFromComboBox.addItem('Milligram (mg)')                                                              # 2
weightConversionFromComboBox.addItem('Tonne (t)')                                                                   # 3
weightConversionFromComboBox.addItem('Quintal (q)')                                                                 # 4
weightConversionFromComboBox.addItem('Carat (ct)')                                                                  # 5
weightConversionFromComboBox.addItem('Ounce (oz)')                                                                  # 6
weightConversionFromComboBox.addItem('Pound (lb)')                                                                  # 7
weightConversionFromComboBox.addItem('Stone (st)')                                                                  # 8
# Input Field
weightConversionInputField = QLineEdit(weightConversionWidget)
weightConversionInputField.setPlaceholderText('Input')
weightConversionInputField.setFixedSize(480, 60)
weightConversionInputField.move(30, 270)
weightConversionInputField.setFont(inputFieldFont)
weightConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
weightConversionInputField.setReadOnly(True)
# To Combo Box
weightConversionToComboBox = QComboBox(weightConversionWidget)
weightConversionToComboBox.setFixedSize(480, 60)
weightConversionToComboBox.move(30, 360)
weightConversionToComboBox.setFont(comboBoxFont)
weightConversionToComboBox.setStyleSheet('padding-left: 10px')
weightConversionToComboBox.addItem('Gram (g)')                                                                      # 0
weightConversionToComboBox.addItem('Kilogram (kg)')                                                                 # 1
weightConversionToComboBox.addItem('Milligram (mg)')                                                                # 2
weightConversionToComboBox.addItem('Tonne (t)')                                                                     # 3
weightConversionToComboBox.addItem('Quintal (q)')                                                                   # 4
weightConversionToComboBox.addItem('Carat (ct)')                                                                    # 5
weightConversionToComboBox.addItem('Ounce (oz)')                                                                    # 6
weightConversionToComboBox.addItem('Pound (lb)')                                                                    # 7
weightConversionToComboBox.addItem('Stone (st)')                                                                    # 8
# Output Field
weightConversionOutputField = QLineEdit(weightConversionWidget)
weightConversionOutputField.setFixedSize(480, 60)
weightConversionOutputField.move(30, 420)
weightConversionOutputField.setFont(outputFieldFont)
weightConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
weightConversionOutputField.setPlaceholderText('Output')
weightConversionOutputField.setReadOnly(True)
# Paste Output to Input
weightConversionPasteButton = QPushButton('⇅', weightConversionWidget)
weightConversionPasteButton.setFixedSize(60, 270)
weightConversionPasteButton.move(510, 210)
weightConversionPasteButton.setFont(conversionPasteButtonFont)
weightConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def weightConversionPaste():
    global weightConversionInput
    weightConversionFromIndex = weightConversionFromComboBox.currentIndex()
    weightConversionToIndex = weightConversionToComboBox.currentIndex()
    weightConversionFromComboBox.setCurrentIndex(weightConversionToIndex)
    weightConversionToComboBox.setCurrentIndex(weightConversionFromIndex)
    if weightConversionInputField.text():
        if weightConversionInputField.text().endswith('.'):
            weightConversionInputField.setText(weightConversionInputField.text().replace('.', ''))
            weightConversionInput = weightConversionInput.replace('.', '')
        weightConversionFrom = weightConversionFromComboBox.currentIndex()
        weightConversionTo = weightConversionToComboBox.currentIndex()
        weightConversionKey = (weightConversionFrom, weightConversionTo)
        weightConversionFactor = weightConversionFactors[weightConversionKey]
        weightConversionOutput = float(weightConversionInput) * weightConversionFactor
        weightConversionOutputField.setText(str(weightConversionOutput))
weightConversionPasteButton.clicked.connect(weightConversionPaste)
# Number Pad
# Nine [9]
weightConversionNineButton = QPushButton('9', weightConversionWidget)
weightConversionNineButton.setFixedSize(90, 90)
weightConversionNineButton.move(300, 510)
weightConversionNineButton.setFont(numberPadFont)
weightConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionNine():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '9')
    weightConversionInput += '9'
weightConversionNineButton.clicked.connect(weightConversionNine)
# Eight [8]
weightConversionEightButton = QPushButton('8', weightConversionWidget)
weightConversionEightButton.setFixedSize(90, 90)
weightConversionEightButton.move(210, 510)
weightConversionEightButton.setFont(numberPadFont)
weightConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionEight():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '8')
    weightConversionInput += '8'
weightConversionEightButton.clicked.connect(weightConversionEight)
# Seven [7]
weightConversionSevenButton = QPushButton('7', weightConversionWidget)
weightConversionSevenButton.setFixedSize(90, 90)
weightConversionSevenButton.move(120, 510)
weightConversionSevenButton.setFont(numberPadFont)
weightConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionSeven():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '7')
    weightConversionInput += '7'
weightConversionSevenButton.clicked.connect(weightConversionSeven)
# Six [6]
weightConversionSixButton = QPushButton('6', weightConversionWidget)
weightConversionSixButton.setFixedSize(90, 90)
weightConversionSixButton.move(300, 600)
weightConversionSixButton.setFont(numberPadFont)
weightConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionSix():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '6')
    weightConversionInput += '6'
weightConversionSixButton.clicked.connect(weightConversionSix)
# Five [5]
weightConversionFiveButton = QPushButton('5', weightConversionWidget)
weightConversionFiveButton.setFixedSize(90, 90)
weightConversionFiveButton.move(210, 600)
weightConversionFiveButton.setFont(numberPadFont)
weightConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionFive():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '5')
    weightConversionInput += '5'
weightConversionFiveButton.clicked.connect(weightConversionFive)
# Four [4]
weightConversionFourButton = QPushButton('4', weightConversionWidget)
weightConversionFourButton.setFixedSize(90, 90)
weightConversionFourButton.move(120, 600)
weightConversionFourButton.setFont(numberPadFont)
weightConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionFour():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '4')
    weightConversionInput += '4'
weightConversionFourButton.clicked.connect(weightConversionFour)
# Three [3]
weightConversionThreeButton = QPushButton('3', weightConversionWidget)
weightConversionThreeButton.setFixedSize(90, 90)
weightConversionThreeButton.move(300, 690)
weightConversionThreeButton.setFont(numberPadFont)
weightConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionThree():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '3')
    weightConversionInput += '3'
weightConversionThreeButton.clicked.connect(weightConversionThree)
# Two [2]
weightConversionTwoButton = QPushButton('2', weightConversionWidget)
weightConversionTwoButton.setFixedSize(90, 90)
weightConversionTwoButton.move(210, 690)
weightConversionTwoButton.setFont(numberPadFont)
weightConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionTwo():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '2')
    weightConversionInput += '2'
weightConversionTwoButton.clicked.connect(weightConversionTwo)
# One [1]
weightConversionOneButton = QPushButton('1', weightConversionWidget)
weightConversionOneButton.setFixedSize(90, 90)
weightConversionOneButton.move(120, 690)
weightConversionOneButton.setFont(numberPadFont)
weightConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionOne():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '1')
    weightConversionInput += '1'
weightConversionOneButton.clicked.connect(weightConversionOne)
# Zero [0]
weightConversionZeroButton = QPushButton('0', weightConversionWidget)
weightConversionZeroButton.setFixedSize(90, 90)
weightConversionZeroButton.move(210, 780)
weightConversionZeroButton.setFont(numberPadFont)
weightConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionZero():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '0')
    weightConversionInput += '0'
weightConversionZeroButton.clicked.connect(weightConversionZero)
# Double Zero [00]
weightConversionDoubleZeroButton = QPushButton('00', weightConversionWidget)
weightConversionDoubleZeroButton.setFixedSize(90, 90)
weightConversionDoubleZeroButton.move(120, 780)
weightConversionDoubleZeroButton.setFont(numberPadFont)
weightConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def weightConversionDoubleZero():
    global weightConversionInput
    weightConversionInputField.setText(weightConversionInputField.text() + '00')
    weightConversionInput += '00'
weightConversionDoubleZeroButton.clicked.connect(weightConversionDoubleZero)
# Point [.]
weightConversionPointButton = QPushButton('.', weightConversionWidget)
weightConversionPointButton.setFixedSize(90, 90)
weightConversionPointButton.move(300, 780)
weightConversionPointButton.setFont(numberPadFont)
weightConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def weightConversionPoint():
    global weightConversionInput
    if weightConversionInputField.text():
        weightConversionInputField.setText(weightConversionInputField.text() + '.')
        weightConversionInput += '.'
    else:
        weightConversionInputField.setText(weightConversionInputField.text() + '0.')
        weightConversionInput += '0.'
weightConversionPointButton.clicked.connect(weightConversionPoint)
# Deletion
# All Clear
weightConversionAllClearButton = QPushButton('AC', weightConversionWidget)
weightConversionAllClearButton.setFixedSize(90, 90)
weightConversionAllClearButton.move(390, 510)
weightConversionAllClearButton.setFont(operatorButtonFont)
weightConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def weightConversionAllClear():
    global weightConversionInput
    weightConversionInputField.setText('')
    weightConversionOutputField.setText('')
    weightConversionInput = ''
weightConversionAllClearButton.clicked.connect(weightConversionAllClear)
# Clear [Backspace]
weightConversionClearButton = QPushButton('C', weightConversionWidget)
weightConversionClearButton.setFixedSize(90, 90)
weightConversionClearButton.move(390, 600)
weightConversionClearButton.setFont(operatorButtonFont)
weightConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def weightConversionClear():
    global weightConversionInput
    weightConversionInputFieldText = weightConversionInputField.text()
    weightConversionInputFieldText = weightConversionInputFieldText[:-1]
    weightConversionInputField.setText(weightConversionInputFieldText)
    weightConversionInput = weightConversionInput[:-1]
weightConversionClearButton.clicked.connect(weightConversionClear)
# Result [=]
weightConversionResultButton = QPushButton('=', weightConversionWidget)
weightConversionResultButton.setFixedSize(90, 180)
weightConversionResultButton.move(390, 690)
weightConversionResultButton.setFont(resultButtonsFont)
weightConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def weightConversionResult():
    global weightConversionInput
    if weightConversionInputField.text():
        if weightConversionInputField.text().endswith('.'):
            weightConversionInputField.setText(weightConversionInputField.text().replace('.', ''))
            weightConversionInput = weightConversionInput.replace('.', '')
        weightConversionFrom = weightConversionFromComboBox.currentIndex()
        weightConversionTo = weightConversionToComboBox.currentIndex()
        weightConversionKey = (weightConversionFrom, weightConversionTo)
        weightConversionFactor = weightConversionFactors[weightConversionKey]
        weightConversionOutput = float(weightConversionInput) * weightConversionFactor
        weightConversionOutputField.setText(str(weightConversionOutput))
weightConversionResultButton.clicked.connect(weightConversionResult)

# Temperature Conversion Page
# Temperature Conversion Widget
temperatureConversionWidget = QWidget()
stackedWidget.addWidget(temperatureConversionWidget)
# Back Button
temperatureBackButton = QPushButton('←', temperatureConversionWidget)
temperatureBackButton.setFixedSize(60, 60)
temperatureBackButton.move(30, 30)
temperatureBackButton.setFont(mainLabelFont)
def temperatureBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
temperatureBackButton.clicked.connect(temperatureBack)
# Switch to Calculator Button
temperatureSwitchToCalculatorButton = QPushButton('⇄', temperatureConversionWidget)
temperatureSwitchToCalculatorButton.setFixedSize(60, 60)
temperatureSwitchToCalculatorButton.move(510, 30)
temperatureSwitchToCalculatorButton.setFont(mainLabelFont)
def temperatureSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
temperatureSwitchToCalculatorButton.clicked.connect(temperatureSwitchToCalculator)
# Temperature Conversion Page Main Label
temperatureConversionLabel = QLabel('Temperature Conversion', temperatureConversionWidget)
temperatureConversionLabel.setFixedSize(540, 60)
temperatureConversionLabel.move(30, 120)
temperatureConversionLabel.setFont(conversionsLabelFont)
temperatureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
temperatureConversionFromComboBox = QComboBox(temperatureConversionWidget)
temperatureConversionFromComboBox.setFixedSize(480, 60)
temperatureConversionFromComboBox.move(30, 210)
temperatureConversionFromComboBox.setFont(comboBoxFont)
temperatureConversionFromComboBox.setStyleSheet('padding-left: 10px')
temperatureConversionFromComboBox.addItem('Celsius (°C)')                                                           # 0
temperatureConversionFromComboBox.addItem('Fahrenheit (°F)')                                                        # 1
temperatureConversionFromComboBox.addItem('Kelvin (K)')                                                             # 2
temperatureConversionFromComboBox.addItem('Rankine (°Ra)')                                                          # 3
# Input Field
temperatureConversionInputField = QLineEdit(temperatureConversionWidget)
temperatureConversionInputField.setPlaceholderText('Input')
temperatureConversionInputField.setFixedSize(480, 60)
temperatureConversionInputField.move(30, 270)
temperatureConversionInputField.setFont(inputFieldFont)
temperatureConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
temperatureConversionInputField.setReadOnly(True)
# To Combo Box
temperatureConversionToComboBox = QComboBox(temperatureConversionWidget)
temperatureConversionToComboBox.setFixedSize(480, 60)
temperatureConversionToComboBox.move(30, 360)
temperatureConversionToComboBox.setFont(comboBoxFont)
temperatureConversionToComboBox.setStyleSheet('padding-left: 10px')
temperatureConversionToComboBox.addItem('Celsius (°C))')                                                            # 0
temperatureConversionToComboBox.addItem('Fahrenheit (°F)')                                                          # 1
temperatureConversionToComboBox.addItem('Kelvin (K)')                                                               # 2
temperatureConversionToComboBox.addItem('Rankine (°Ra)')                                                            # 3
# Output Field
temperatureConversionOutputField = QLineEdit(temperatureConversionWidget)
temperatureConversionOutputField.setFixedSize(480, 60)
temperatureConversionOutputField.move(30, 420)
temperatureConversionOutputField.setFont(outputFieldFont)
temperatureConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
temperatureConversionOutputField.setPlaceholderText('Output')
temperatureConversionOutputField.setReadOnly(True)
# Paste Output to Input
temperatureConversionPasteButton = QPushButton('⇅', temperatureConversionWidget)
temperatureConversionPasteButton.setFixedSize(60, 270)
temperatureConversionPasteButton.move(510, 210)
temperatureConversionPasteButton.setFont(conversionPasteButtonFont)
temperatureConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def temperatureConversionPaste():
    global temperatureConversionInput
    temperatureConversionFromIndex = temperatureConversionFromComboBox.currentIndex()
    temperatureConversionToIndex = temperatureConversionToComboBox.currentIndex()
    temperatureConversionFromComboBox.setCurrentIndex(temperatureConversionToIndex)
    temperatureConversionToComboBox.setCurrentIndex(temperatureConversionFromIndex)
    if temperatureConversionInputField.text():
        if temperatureConversionInputField.text().endswith('.'):
            temperatureConversionInputField.setText(temperatureConversionInputField.text().replace('.', ''))
            temperatureConversionInput = temperatureConversionInput.replace('.', '')
        if temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = (float(temperatureConversionInput) * 1.8) + 32
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = float(temperatureConversionInput) + 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = (float(temperatureConversionInput) * 1.8) + 491.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = (float(temperatureConversionInput) - 32) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = ((float(temperatureConversionInput) - 32) / 1.8) + 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = float(temperatureConversionInput) + 459.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = float(temperatureConversionInput) - 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = ((float(temperatureConversionInput) - 273.15) * 1.8) + 32
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = float(temperatureConversionInput) * 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = (float(temperatureConversionInput) - 491.67) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = float(temperatureConversionInput) - 459.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = float(temperatureConversionInput) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        else:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
temperatureConversionPasteButton.clicked.connect(temperatureConversionPaste)
# Number Pad
# Nine [9]
temperatureConversionNineButton = QPushButton('9', temperatureConversionWidget)
temperatureConversionNineButton.setFixedSize(90, 90)
temperatureConversionNineButton.move(300, 510)
temperatureConversionNineButton.setFont(numberPadFont)
temperatureConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionNine():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '9')
    temperatureConversionInput += '9'
temperatureConversionNineButton.clicked.connect(temperatureConversionNine)
# Eight [8]
temperatureConversionEightButton = QPushButton('8', temperatureConversionWidget)
temperatureConversionEightButton.setFixedSize(90, 90)
temperatureConversionEightButton.move(210, 510)
temperatureConversionEightButton.setFont(numberPadFont)
temperatureConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionEight():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '8')
    temperatureConversionInput += '8'
temperatureConversionEightButton.clicked.connect(temperatureConversionEight)
# Seven [7]
temperatureConversionSevenButton = QPushButton('7', temperatureConversionWidget)
temperatureConversionSevenButton.setFixedSize(90, 90)
temperatureConversionSevenButton.move(120, 510)
temperatureConversionSevenButton.setFont(numberPadFont)
temperatureConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionSeven():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '7')
    temperatureConversionInput += '7'
temperatureConversionSevenButton.clicked.connect(temperatureConversionSeven)
# Six [6]
temperatureConversionSixButton = QPushButton('6', temperatureConversionWidget)
temperatureConversionSixButton.setFixedSize(90, 90)
temperatureConversionSixButton.move(300, 600)
temperatureConversionSixButton.setFont(numberPadFont)
temperatureConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionSix():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '6')
    temperatureConversionInput += '6'
temperatureConversionSixButton.clicked.connect(temperatureConversionSix)
# Five [5]
temperatureConversionFiveButton = QPushButton('5', temperatureConversionWidget)
temperatureConversionFiveButton.setFixedSize(90, 90)
temperatureConversionFiveButton.move(210, 600)
temperatureConversionFiveButton.setFont(numberPadFont)
temperatureConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionFive():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '5')
    temperatureConversionInput += '5'
temperatureConversionFiveButton.clicked.connect(temperatureConversionFive)
# Four [4]
temperatureConversionFourButton = QPushButton('4', temperatureConversionWidget)
temperatureConversionFourButton.setFixedSize(90, 90)
temperatureConversionFourButton.move(120, 600)
temperatureConversionFourButton.setFont(numberPadFont)
temperatureConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionFour():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '4')
    temperatureConversionInput += '4'
temperatureConversionFourButton.clicked.connect(temperatureConversionFour)
# Three [3]
temperatureConversionThreeButton = QPushButton('3', temperatureConversionWidget)
temperatureConversionThreeButton.setFixedSize(90, 90)
temperatureConversionThreeButton.move(300, 690)
temperatureConversionThreeButton.setFont(numberPadFont)
temperatureConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionThree():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '3')
    temperatureConversionInput += '3'
temperatureConversionThreeButton.clicked.connect(temperatureConversionThree)
# Two [2]
temperatureConversionTwoButton = QPushButton('2', temperatureConversionWidget)
temperatureConversionTwoButton.setFixedSize(90, 90)
temperatureConversionTwoButton.move(210, 690)
temperatureConversionTwoButton.setFont(numberPadFont)
temperatureConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionTwo():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '2')
    temperatureConversionInput += '2'
temperatureConversionTwoButton.clicked.connect(temperatureConversionTwo)
# One [1]
temperatureConversionOneButton = QPushButton('1', temperatureConversionWidget)
temperatureConversionOneButton.setFixedSize(90, 90)
temperatureConversionOneButton.move(120, 690)
temperatureConversionOneButton.setFont(numberPadFont)
temperatureConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionOne():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '1')
    temperatureConversionInput += '1'
temperatureConversionOneButton.clicked.connect(temperatureConversionOne)
# Zero [0]
temperatureConversionZeroButton = QPushButton('0', temperatureConversionWidget)
temperatureConversionZeroButton.setFixedSize(90, 90)
temperatureConversionZeroButton.move(210, 780)
temperatureConversionZeroButton.setFont(numberPadFont)
temperatureConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def temperatureConversionZero():
    global temperatureConversionInput
    temperatureConversionInputField.setText(temperatureConversionInputField.text() + '0')
    temperatureConversionInput += '0'
temperatureConversionZeroButton.clicked.connect(temperatureConversionZero)
# Minus [-]
temperatureConversionMinusButton = QPushButton('-', temperatureConversionWidget)
temperatureConversionMinusButton.setFixedSize(90, 90)
temperatureConversionMinusButton.move(120, 780)
temperatureConversionMinusButton.setFont(operatorButtonFont)
temperatureConversionMinusButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def temperatureConversionMinus():
    global temperatureConversionInput
    if temperatureConversionInputField.text() == '':
        temperatureConversionInputField.setText('-')
        temperatureConversionInput = '-'
temperatureConversionMinusButton.clicked.connect(temperatureConversionMinus)
# Point [.]
temperatureConversionPointButton = QPushButton('.', temperatureConversionWidget)
temperatureConversionPointButton.setFixedSize(90, 90)
temperatureConversionPointButton.move(300, 780)
temperatureConversionPointButton.setFont(numberPadFont)
temperatureConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def temperatureConversionPoint():
    global temperatureConversionInput
    if temperatureConversionInputField.text():
        temperatureConversionInputField.setText(temperatureConversionInputField.text() + '.')
        temperatureConversionInput += '.'
    else:
        temperatureConversionInputField.setText(temperatureConversionInputField.text() + '0.')
        temperatureConversionInput += '0.'
temperatureConversionPointButton.clicked.connect(temperatureConversionPoint)
# Deletion
# All Clear
temperatureConversionAllClearButton = QPushButton('AC', temperatureConversionWidget)
temperatureConversionAllClearButton.setFixedSize(90, 90)
temperatureConversionAllClearButton.move(390, 510)
temperatureConversionAllClearButton.setFont(operatorButtonFont)
temperatureConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def temperatureConversionAllClear():
    global temperatureConversionInput
    temperatureConversionInputField.setText('')
    temperatureConversionOutputField.setText('')
    temperatureConversionInput = ''
temperatureConversionAllClearButton.clicked.connect(temperatureConversionAllClear)
# Clear [Backspace]
temperatureConversionClearButton = QPushButton('C', temperatureConversionWidget)
temperatureConversionClearButton.setFixedSize(90, 90)
temperatureConversionClearButton.move(390, 600)
temperatureConversionClearButton.setFont(operatorButtonFont)
temperatureConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def temperatureConversionClear():
    global temperatureConversionInput
    temperatureConversionInputFieldText = temperatureConversionInputField.text()
    temperatureConversionInputFieldText = temperatureConversionInputFieldText[:-1]
    temperatureConversionInputField.setText(temperatureConversionInputFieldText)
    temperatureConversionInput = temperatureConversionInput[:-1]
temperatureConversionClearButton.clicked.connect(temperatureConversionClear)
# Result [=]
temperatureConversionResultButton = QPushButton('=', temperatureConversionWidget)
temperatureConversionResultButton.setFixedSize(90, 180)
temperatureConversionResultButton.move(390, 690)
temperatureConversionResultButton.setFont(resultButtonsFont)
temperatureConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def temperatureConversionResult():
    global temperatureConversionInput
    if temperatureConversionInputField.text():
        if temperatureConversionInputField.text().endswith('.'):
            temperatureConversionInputField.setText(temperatureConversionInputField.text().replace('.', ''))
            temperatureConversionInput = temperatureConversionInput.replace('.', '')
        if temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = (float(temperatureConversionInput) * 1.8) + 32
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = float(temperatureConversionInput) + 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 0 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = (float(temperatureConversionInput) * 1.8) + 491.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = (float(temperatureConversionInput) - 32) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = ((float(temperatureConversionInput) - 32) / 1.8) + 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 1 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = float(temperatureConversionInput) + 459.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = float(temperatureConversionInput) - 273.15
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = ((float(temperatureConversionInput) - 273.15) * 1.8) + 32
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
        elif temperatureConversionFromComboBox.currentIndex() == 2 and temperatureConversionToComboBox.currentIndex() == 3:
            temperatureConversionOutput = float(temperatureConversionInput) * 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 0:
            temperatureConversionOutput = (float(temperatureConversionInput) - 491.67) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 1:
            temperatureConversionOutput = float(temperatureConversionInput) - 459.67
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        elif temperatureConversionFromComboBox.currentIndex() == 3 and temperatureConversionToComboBox.currentIndex() == 2:
            temperatureConversionOutput = float(temperatureConversionInput) / 1.8
            temperatureConversionOutputField.setText(str(temperatureConversionOutput))
        else:
            temperatureConversionOutput = temperatureConversionInput
            temperatureConversionOutputField.setText(temperatureConversionOutput)
temperatureConversionResultButton.clicked.connect(temperatureConversionResult)

# Speed Conversion Page
# Speed Conversion Widget
speedConversionWidget = QWidget()
stackedWidget.addWidget(speedConversionWidget)
# Back Button
speedBackButton = QPushButton('←', speedConversionWidget)
speedBackButton.setFixedSize(60, 60)
speedBackButton.move(30, 30)
speedBackButton.setFont(mainLabelFont)
def speedBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
speedBackButton.clicked.connect(speedBack)
# Switch to Calculator Button
speedSwitchToCalculatorButton = QPushButton('⇄', speedConversionWidget)
speedSwitchToCalculatorButton.setFixedSize(60, 60)
speedSwitchToCalculatorButton.move(510, 30)
speedSwitchToCalculatorButton.setFont(mainLabelFont)
def speedSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
speedSwitchToCalculatorButton.clicked.connect(speedSwitchToCalculator)
# Speed Conversion Page Main Label
speedConversionLabel = QLabel('Speed Conversion', speedConversionWidget)
speedConversionLabel.setFixedSize(540, 60)
speedConversionLabel.move(30, 120)
speedConversionLabel.setFont(conversionsLabelFont)
speedConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
speedConversionFromComboBox = QComboBox(speedConversionWidget)
speedConversionFromComboBox.setFixedSize(480, 60)
speedConversionFromComboBox.move(30, 210)
speedConversionFromComboBox.setFont(comboBoxFont)
speedConversionFromComboBox.setStyleSheet('padding-left: 10px')
speedConversionFromComboBox.addItem('Metres per second (m/s)')                                                      # 0
speedConversionFromComboBox.addItem('Kilometres per hour (km/h)')                                                   # 1
speedConversionFromComboBox.addItem('Miles per hour (mph)')                                                         # 2
speedConversionFromComboBox.addItem('Mach (Ma)')                                                                    # 3
speedConversionFromComboBox.addItem('Speed of Light (c)')                                                           # 4
# Input Field
speedConversionInputField = QLineEdit(speedConversionWidget)
speedConversionInputField.setPlaceholderText('Input')
speedConversionInputField.setFixedSize(480, 60)
speedConversionInputField.move(30, 270)
speedConversionInputField.setFont(inputFieldFont)
speedConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
speedConversionInputField.setReadOnly(True)
# To Combo Box
speedConversionToComboBox = QComboBox(speedConversionWidget)
speedConversionToComboBox.setFixedSize(480, 60)
speedConversionToComboBox.move(30, 360)
speedConversionToComboBox.setFont(comboBoxFont)
speedConversionToComboBox.setStyleSheet('padding-left: 10px')
speedConversionToComboBox.addItem('Metres per second (m/s)')                                                        # 0
speedConversionToComboBox.addItem('Kilometres per hour (km/h)')                                                     # 1
speedConversionToComboBox.addItem('Miles per hour (mph)')                                                           # 2
speedConversionToComboBox.addItem('Mach (Ma)')                                                                      # 3
speedConversionToComboBox.addItem('Speed of Light (c)')                                                             # 4
# Output Field
speedConversionOutputField = QLineEdit(speedConversionWidget)
speedConversionOutputField.setFixedSize(480, 60)
speedConversionOutputField.move(30, 420)
speedConversionOutputField.setFont(outputFieldFont)
speedConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
speedConversionOutputField.setPlaceholderText('Output')
speedConversionOutputField.setReadOnly(True)
# Paste Output to Input
speedConversionPasteButton = QPushButton('⇅', speedConversionWidget)
speedConversionPasteButton.setFixedSize(60, 270)
speedConversionPasteButton.move(510, 210)
speedConversionPasteButton.setFont(conversionPasteButtonFont)
speedConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def speedConversionPaste():
    global speedConversionInput
    speedConversionFromIndex = speedConversionFromComboBox.currentIndex()
    speedConversionToIndex = speedConversionToComboBox.currentIndex()
    speedConversionFromComboBox.setCurrentIndex(speedConversionToIndex)
    speedConversionToComboBox.setCurrentIndex(speedConversionFromIndex)
    if speedConversionInputField.text():
        if speedConversionInputField.text().endswith('.'):
            speedConversionInputField.setText(speedConversionInputField.text().replace('.', ''))
            speedConversionInput = speedConversionInput.replace('.', '')
        speedConversionFrom = speedConversionFromComboBox.currentIndex()
        speedConversionTo = speedConversionToComboBox.currentIndex()
        speedConversionKey = (speedConversionFrom, speedConversionTo)
        speedConversionFactor = speedConversionFactors[speedConversionKey]
        speedConversionOutput = float(speedConversionInput) * speedConversionFactor
        speedConversionOutputField.setText(str(speedConversionOutput))
speedConversionPasteButton.clicked.connect(speedConversionPaste)
# Number Pad
# Nine [9]
speedConversionNineButton = QPushButton('9', speedConversionWidget)
speedConversionNineButton.setFixedSize(90, 90)
speedConversionNineButton.move(300, 510)
speedConversionNineButton.setFont(numberPadFont)
speedConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionNine():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '9')
    speedConversionInput += '9'
speedConversionNineButton.clicked.connect(speedConversionNine)
# Eight [8]
speedConversionEightButton = QPushButton('8', speedConversionWidget)
speedConversionEightButton.setFixedSize(90, 90)
speedConversionEightButton.move(210, 510)
speedConversionEightButton.setFont(numberPadFont)
speedConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionEight():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '8')
    speedConversionInput += '8'
speedConversionEightButton.clicked.connect(speedConversionEight)
# Seven [7]
speedConversionSevenButton = QPushButton('7', speedConversionWidget)
speedConversionSevenButton.setFixedSize(90, 90)
speedConversionSevenButton.move(120, 510)
speedConversionSevenButton.setFont(numberPadFont)
speedConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionSeven():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '7')
    speedConversionInput += '7'
speedConversionSevenButton.clicked.connect(speedConversionSeven)
# Six [6]
speedConversionSixButton = QPushButton('6', speedConversionWidget)
speedConversionSixButton.setFixedSize(90, 90)
speedConversionSixButton.move(300, 600)
speedConversionSixButton.setFont(numberPadFont)
speedConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionSix():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '6')
    speedConversionInput += '6'
speedConversionSixButton.clicked.connect(speedConversionSix)
# Five [5]
speedConversionFiveButton = QPushButton('5', speedConversionWidget)
speedConversionFiveButton.setFixedSize(90, 90)
speedConversionFiveButton.move(210, 600)
speedConversionFiveButton.setFont(numberPadFont)
speedConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionFive():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '5')
    speedConversionInput += '5'
speedConversionFiveButton.clicked.connect(speedConversionFive)
# Four [4]
speedConversionFourButton = QPushButton('4', speedConversionWidget)
speedConversionFourButton.setFixedSize(90, 90)
speedConversionFourButton.move(120, 600)
speedConversionFourButton.setFont(numberPadFont)
speedConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionFour():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '4')
    speedConversionInput += '4'
speedConversionFourButton.clicked.connect(speedConversionFour)
# Three [3]
speedConversionThreeButton = QPushButton('3', speedConversionWidget)
speedConversionThreeButton.setFixedSize(90, 90)
speedConversionThreeButton.move(300, 690)
speedConversionThreeButton.setFont(numberPadFont)
speedConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionThree():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '3')
    speedConversionInput += '3'
speedConversionThreeButton.clicked.connect(speedConversionThree)
# Two [2]
speedConversionTwoButton = QPushButton('2', speedConversionWidget)
speedConversionTwoButton.setFixedSize(90, 90)
speedConversionTwoButton.move(210, 690)
speedConversionTwoButton.setFont(numberPadFont)
speedConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionTwo():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '2')
    speedConversionInput += '2'
speedConversionTwoButton.clicked.connect(speedConversionTwo)
# One [1]
speedConversionOneButton = QPushButton('1', speedConversionWidget)
speedConversionOneButton.setFixedSize(90, 90)
speedConversionOneButton.move(120, 690)
speedConversionOneButton.setFont(numberPadFont)
speedConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionOne():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '1')
    speedConversionInput += '1'
speedConversionOneButton.clicked.connect(speedConversionOne)
# Zero [0]
speedConversionZeroButton = QPushButton('0', speedConversionWidget)
speedConversionZeroButton.setFixedSize(90, 90)
speedConversionZeroButton.move(210, 780)
speedConversionZeroButton.setFont(numberPadFont)
speedConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionZero():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '0')
    speedConversionInput += '0'
speedConversionZeroButton.clicked.connect(speedConversionZero)
# Double Zero [00]
speedConversionDoubleZeroButton = QPushButton('00', speedConversionWidget)
speedConversionDoubleZeroButton.setFixedSize(90, 90)
speedConversionDoubleZeroButton.move(120, 780)
speedConversionDoubleZeroButton.setFont(numberPadFont)
speedConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def speedConversionDoubleZero():
    global speedConversionInput
    speedConversionInputField.setText(speedConversionInputField.text() + '00')
    speedConversionInput += '00'
speedConversionDoubleZeroButton.clicked.connect(speedConversionDoubleZero)
# Point [.]
speedConversionPointButton = QPushButton('.', speedConversionWidget)
speedConversionPointButton.setFixedSize(90, 90)
speedConversionPointButton.move(300, 780)
speedConversionPointButton.setFont(numberPadFont)
speedConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def speedConversionPoint():
    global speedConversionInput
    if speedConversionInputField.text():
        speedConversionInputField.setText(speedConversionInputField.text() + '.')
        speedConversionInput += '.'
    else:
        speedConversionInputField.setText(speedConversionInputField.text() + '0.')
        speedConversionInput += '0.'
speedConversionPointButton.clicked.connect(speedConversionPoint)
# Deletion
# All Clear
speedConversionAllClearButton = QPushButton('AC', speedConversionWidget)
speedConversionAllClearButton.setFixedSize(90, 90)
speedConversionAllClearButton.move(390, 510)
speedConversionAllClearButton.setFont(operatorButtonFont)
speedConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def speedConversionAllClear():
    global speedConversionInput
    speedConversionInputField.setText('')
    speedConversionOutputField.setText('')
    speedConversionInput = ''
speedConversionAllClearButton.clicked.connect(speedConversionAllClear)
# Clear [Backspace]
speedConversionClearButton = QPushButton('C', speedConversionWidget)
speedConversionClearButton.setFixedSize(90, 90)
speedConversionClearButton.move(390, 600)
speedConversionClearButton.setFont(operatorButtonFont)
speedConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def speedConversionClear():
    global speedConversionInput
    speedConversionInputFieldText = speedConversionInputField.text()
    speedConversionInputFieldText = speedConversionInputFieldText[:-1]
    speedConversionInputField.setText(speedConversionInputFieldText)
    speedConversionInput = speedConversionInput[:-1]
speedConversionClearButton.clicked.connect(speedConversionClear)
# Result [=]
speedConversionResultButton = QPushButton('=', speedConversionWidget)
speedConversionResultButton.setFixedSize(90, 180)
speedConversionResultButton.move(390, 690)
speedConversionResultButton.setFont(resultButtonsFont)
speedConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def speedConversionResult():
    global speedConversionInput
    if speedConversionInputField.text():
        if speedConversionInputField.text().endswith('.'):
            speedConversionInputField.setText(speedConversionInputField.text().replace('.', ''))
            speedConversionInput = speedConversionInput.replace('.', '')
        speedConversionFrom = speedConversionFromComboBox.currentIndex()
        speedConversionTo = speedConversionToComboBox.currentIndex()
        speedConversionKey = (speedConversionFrom, speedConversionTo)
        speedConversionFactor = speedConversionFactors[speedConversionKey]
        speedConversionOutput = float(speedConversionInput) * speedConversionFactor
        speedConversionOutputField.setText(str(speedConversionOutput))
speedConversionResultButton.clicked.connect(speedConversionResult)

# Pressure Conversion Page
# Pressure Conversion Widget
pressureConversionWidget = QWidget()
stackedWidget.addWidget(pressureConversionWidget)
# Back Button
pressureBackButton = QPushButton('←', pressureConversionWidget)
pressureBackButton.setFixedSize(60, 60)
pressureBackButton.move(30, 30)
pressureBackButton.setFont(mainLabelFont)
def pressureBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
pressureBackButton.clicked.connect(pressureBack)
# Switch to Calculator Button
pressureSwitchToCalculatorButton = QPushButton('⇄', pressureConversionWidget)
pressureSwitchToCalculatorButton.setFixedSize(60, 60)
pressureSwitchToCalculatorButton.move(510, 30)
pressureSwitchToCalculatorButton.setFont(mainLabelFont)
def pressureSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
pressureSwitchToCalculatorButton.clicked.connect(pressureSwitchToCalculator)
# Pressure Conversion Page Main Label
pressureConversionLabel = QLabel('Pressure Conversion', pressureConversionWidget)
pressureConversionLabel.setFixedSize(540, 60)
pressureConversionLabel.move(30, 120)
pressureConversionLabel.setFont(conversionsLabelFont)
pressureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
pressureConversionFromComboBox = QComboBox(pressureConversionWidget)
pressureConversionFromComboBox.setFixedSize(480, 60)
pressureConversionFromComboBox.move(30, 210)
pressureConversionFromComboBox.setFont(comboBoxFont)
pressureConversionFromComboBox.setStyleSheet('padding-left: 10px')
pressureConversionFromComboBox.addItem('Atmosphere (atm)')                                                          # 0
pressureConversionFromComboBox.addItem('Bar (Bar)')                                                                 # 1
pressureConversionFromComboBox.addItem('Millibar (mBar)')                                                           # 2
pressureConversionFromComboBox.addItem('Pounds per square inch (psi)')                                              # 3
pressureConversionFromComboBox.addItem('Pascal (Pa) / Newtons per square metre (N/m²)')                             # 4
pressureConversionFromComboBox.addItem('Millimetres of H₂O [Water] (mmH₂O)')                                        # 5
pressureConversionFromComboBox.addItem('Millimetres of Hg [Mercury] (mmHg)')                                        # 6
# Input Field
pressureConversionInputField = QLineEdit(pressureConversionWidget)
pressureConversionInputField.setPlaceholderText('Input')
pressureConversionInputField.setFixedSize(480, 60)
pressureConversionInputField.move(30, 270)
pressureConversionInputField.setFont(inputFieldFont)
pressureConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
pressureConversionInputField.setReadOnly(True)
# To Combo Box
pressureConversionToComboBox = QComboBox(pressureConversionWidget)
pressureConversionToComboBox.setFixedSize(480, 60)
pressureConversionToComboBox.move(30, 360)
pressureConversionToComboBox.setFont(comboBoxFont)
pressureConversionToComboBox.setStyleSheet('padding-left: 10px')
pressureConversionToComboBox.addItem('Atmosphere (atm)')                                                            # 0
pressureConversionToComboBox.addItem('Bar (Bar)')                                                                   # 1
pressureConversionToComboBox.addItem('Millibar (mBar)')                                                             # 2
pressureConversionToComboBox.addItem('Pounds per square inch (psi)')                                                # 3
pressureConversionToComboBox.addItem('Pascal (Pa) / Newtons per square metre (N/m²)')                               # 4
pressureConversionToComboBox.addItem('Millimetres of H₂O [Water] (mmH₂O)')                                          # 5
pressureConversionToComboBox.addItem('Millimetres of Hg [Mercury] (mmHg)')                                          # 6
# Output Field
pressureConversionOutputField = QLineEdit(pressureConversionWidget)
pressureConversionOutputField.setFixedSize(480, 60)
pressureConversionOutputField.move(30, 420)
pressureConversionOutputField.setFont(outputFieldFont)
pressureConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
pressureConversionOutputField.setPlaceholderText('Output')
pressureConversionOutputField.setReadOnly(True)
# Paste Output to Input
pressureConversionPasteButton = QPushButton('⇅', pressureConversionWidget)
pressureConversionPasteButton.setFixedSize(60, 270)
pressureConversionPasteButton.move(510, 210)
pressureConversionPasteButton.setFont(conversionPasteButtonFont)
pressureConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def pressureConversionPaste():
    global pressureConversionInput
    pressureConversionFromIndex = pressureConversionFromComboBox.currentIndex()
    pressureConversionToIndex = pressureConversionToComboBox.currentIndex()
    pressureConversionFromComboBox.setCurrentIndex(pressureConversionToIndex)
    pressureConversionToComboBox.setCurrentIndex(pressureConversionFromIndex)
    if pressureConversionInputField.text():
        if pressureConversionInputField.text().endswith('.'):
            pressureConversionInputField.setText(pressureConversionInputField.text().replace('.', ''))
            pressureConversionInput = pressureConversionInput.replace('.', '')
        pressureConversionFrom = pressureConversionFromComboBox.currentIndex()
        pressureConversionTo = pressureConversionToComboBox.currentIndex()
        pressureConversionKey = (pressureConversionFrom, pressureConversionTo)
        pressureConversionFactor = pressureConversionFactors[pressureConversionKey]
        pressureConversionOutput = float(pressureConversionInput) * pressureConversionFactor
        pressureConversionOutputField.setText(str(pressureConversionOutput))
pressureConversionPasteButton.clicked.connect(pressureConversionPaste)
# Number Pad
# Nine [9]
pressureConversionNineButton = QPushButton('9', pressureConversionWidget)
pressureConversionNineButton.setFixedSize(90, 90)
pressureConversionNineButton.move(300, 510)
pressureConversionNineButton.setFont(numberPadFont)
pressureConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionNine():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '9')
    pressureConversionInput += '9'
pressureConversionNineButton.clicked.connect(pressureConversionNine)
# Eight [8]
pressureConversionEightButton = QPushButton('8', pressureConversionWidget)
pressureConversionEightButton.setFixedSize(90, 90)
pressureConversionEightButton.move(210, 510)
pressureConversionEightButton.setFont(numberPadFont)
pressureConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionEight():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '8')
    pressureConversionInput += '8'
pressureConversionEightButton.clicked.connect(pressureConversionEight)
# Seven [7]
pressureConversionSevenButton = QPushButton('7', pressureConversionWidget)
pressureConversionSevenButton.setFixedSize(90, 90)
pressureConversionSevenButton.move(120, 510)
pressureConversionSevenButton.setFont(numberPadFont)
pressureConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionSeven():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '7')
    pressureConversionInput += '7'
pressureConversionSevenButton.clicked.connect(pressureConversionSeven)
# Six [6]
pressureConversionSixButton = QPushButton('6', pressureConversionWidget)
pressureConversionSixButton.setFixedSize(90, 90)
pressureConversionSixButton.move(300, 600)
pressureConversionSixButton.setFont(numberPadFont)
pressureConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionSix():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '6')
    pressureConversionInput += '6'
pressureConversionSixButton.clicked.connect(pressureConversionSix)
# Five [5]
pressureConversionFiveButton = QPushButton('5', pressureConversionWidget)
pressureConversionFiveButton.setFixedSize(90, 90)
pressureConversionFiveButton.move(210, 600)
pressureConversionFiveButton.setFont(numberPadFont)
pressureConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionFive():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '5')
    pressureConversionInput += '5'
pressureConversionFiveButton.clicked.connect(pressureConversionFive)
# Four [4]
pressureConversionFourButton = QPushButton('4', pressureConversionWidget)
pressureConversionFourButton.setFixedSize(90, 90)
pressureConversionFourButton.move(120, 600)
pressureConversionFourButton.setFont(numberPadFont)
pressureConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionFour():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '4')
    pressureConversionInput += '4'
pressureConversionFourButton.clicked.connect(pressureConversionFour)
# Three [3]
pressureConversionThreeButton = QPushButton('3', pressureConversionWidget)
pressureConversionThreeButton.setFixedSize(90, 90)
pressureConversionThreeButton.move(300, 690)
pressureConversionThreeButton.setFont(numberPadFont)
pressureConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionThree():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '3')
    pressureConversionInput += '3'
pressureConversionThreeButton.clicked.connect(pressureConversionThree)
# Two [2]
pressureConversionTwoButton = QPushButton('2', pressureConversionWidget)
pressureConversionTwoButton.setFixedSize(90, 90)
pressureConversionTwoButton.move(210, 690)
pressureConversionTwoButton.setFont(numberPadFont)
pressureConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionTwo():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '2')
    pressureConversionInput += '2'
pressureConversionTwoButton.clicked.connect(pressureConversionTwo)
# One [1]
pressureConversionOneButton = QPushButton('1', pressureConversionWidget)
pressureConversionOneButton.setFixedSize(90, 90)
pressureConversionOneButton.move(120, 690)
pressureConversionOneButton.setFont(numberPadFont)
pressureConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionOne():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '1')
    pressureConversionInput += '1'
pressureConversionOneButton.clicked.connect(pressureConversionOne)
# Zero [0]
pressureConversionZeroButton = QPushButton('0', pressureConversionWidget)
pressureConversionZeroButton.setFixedSize(90, 90)
pressureConversionZeroButton.move(210, 780)
pressureConversionZeroButton.setFont(numberPadFont)
pressureConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionZero():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '0')
    pressureConversionInput += '0'
pressureConversionZeroButton.clicked.connect(pressureConversionZero)
# Double Zero [00]
pressureConversionDoubleZeroButton = QPushButton('00', pressureConversionWidget)
pressureConversionDoubleZeroButton.setFixedSize(90, 90)
pressureConversionDoubleZeroButton.move(120, 780)
pressureConversionDoubleZeroButton.setFont(numberPadFont)
pressureConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def pressureConversionDoubleZero():
    global pressureConversionInput
    pressureConversionInputField.setText(pressureConversionInputField.text() + '00')
    pressureConversionInput += '00'
pressureConversionDoubleZeroButton.clicked.connect(pressureConversionDoubleZero)
# Point [.]
pressureConversionPointButton = QPushButton('.', pressureConversionWidget)
pressureConversionPointButton.setFixedSize(90, 90)
pressureConversionPointButton.move(300, 780)
pressureConversionPointButton.setFont(numberPadFont)
pressureConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def pressureConversionPoint():
    global pressureConversionInput
    if pressureConversionInputField.text():
        pressureConversionInputField.setText(pressureConversionInputField.text() + '.')
        pressureConversionInput += '.'
    else:
        pressureConversionInputField.setText(pressureConversionInputField.text() + '0.')
        pressureConversionInput += '0.'
pressureConversionPointButton.clicked.connect(pressureConversionPoint)
# Deletion
# All Clear
pressureConversionAllClearButton = QPushButton('AC', pressureConversionWidget)
pressureConversionAllClearButton.setFixedSize(90, 90)
pressureConversionAllClearButton.move(390, 510)
pressureConversionAllClearButton.setFont(operatorButtonFont)
pressureConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def pressureConversionAllClear():
    global pressureConversionInput
    pressureConversionInputField.setText('')
    pressureConversionOutputField.setText('')
    pressureConversionInput = ''
pressureConversionAllClearButton.clicked.connect(pressureConversionAllClear)
# Clear [Backspace]
pressureConversionClearButton = QPushButton('C', pressureConversionWidget)
pressureConversionClearButton.setFixedSize(90, 90)
pressureConversionClearButton.move(390, 600)
pressureConversionClearButton.setFont(operatorButtonFont)
pressureConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def pressureConversionClear():
    global pressureConversionInput
    pressureConversionInputFieldText = pressureConversionInputField.text()
    pressureConversionInputFieldText = pressureConversionInputFieldText[:-1]
    pressureConversionInputField.setText(pressureConversionInputFieldText)
    pressureConversionInput = pressureConversionInput[:-1]
pressureConversionClearButton.clicked.connect(pressureConversionClear)
# Result [=]
pressureConversionResultButton = QPushButton('=', pressureConversionWidget)
pressureConversionResultButton.setFixedSize(90, 180)
pressureConversionResultButton.move(390, 690)
pressureConversionResultButton.setFont(resultButtonsFont)
pressureConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def pressureConversionResult():
    global pressureConversionInput
    if pressureConversionInputField.text():
        if pressureConversionInputField.text().endswith('.'):
            pressureConversionInputField.setText(pressureConversionInputField.text().replace('.', ''))
            pressureConversionInput = pressureConversionInput.replace('.', '')
        pressureConversionFrom = pressureConversionFromComboBox.currentIndex()
        pressureConversionTo = pressureConversionToComboBox.currentIndex()
        pressureConversionKey = (pressureConversionFrom, pressureConversionTo)
        pressureConversionFactor = pressureConversionFactors[pressureConversionKey]
        pressureConversionOutput = float(pressureConversionInput) * pressureConversionFactor
        pressureConversionOutputField.setText(str(pressureConversionOutput))
pressureConversionResultButton.clicked.connect(pressureConversionResult)

# Power Conversion Page
# Power Conversion Widget
powerConversionWidget = QWidget()
stackedWidget.addWidget(powerConversionWidget)
# Back Button
powerBackButton = QPushButton('←', powerConversionWidget)
powerBackButton.setFixedSize(60, 60)
powerBackButton.move(30, 30)
powerBackButton.setFont(mainLabelFont)
def powerBack():
    stackedWidget.setCurrentWidget(conversionsWidget)
powerBackButton.clicked.connect(powerBack)
# Switch to Calculator Button
powerSwitchToCalculatorButton = QPushButton('⇄', powerConversionWidget)
powerSwitchToCalculatorButton.setFixedSize(60, 60)
powerSwitchToCalculatorButton.move(510, 30)
powerSwitchToCalculatorButton.setFont(mainLabelFont)
def powerSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
powerSwitchToCalculatorButton.clicked.connect(powerSwitchToCalculator)
# Power Conversion Page Main Label
powerConversionLabel = QLabel('Power Conversion', powerConversionWidget)
powerConversionLabel.setFixedSize(540, 60)
powerConversionLabel.move(30, 120)
powerConversionLabel.setFont(conversionsLabelFont)
powerConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
powerConversionFromComboBox = QComboBox(powerConversionWidget)
powerConversionFromComboBox.setFixedSize(480, 60)
powerConversionFromComboBox.move(30, 210)
powerConversionFromComboBox.setFont(comboBoxFont)
powerConversionFromComboBox.setStyleSheet('padding-left: 10px')
powerConversionFromComboBox.addItem('Watt (W) | Joules per second (J/s) | Newton-metres per second (N∙m/s)')        # 0
powerConversionFromComboBox.addItem('Foot-pounds per second (ft∙lb/s)')                                             # 1
powerConversionFromComboBox.addItem('Kilocalories per second (kcal/s)')                                             # 2
powerConversionFromComboBox.addItem('Horsepower (HP)')                                                              # 3
# Input Field
powerConversionInputField = QLineEdit(powerConversionWidget)
powerConversionInputField.setPlaceholderText('Input')
powerConversionInputField.setFixedSize(480, 60)
powerConversionInputField.move(30, 270)
powerConversionInputField.setFont(inputFieldFont)
powerConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
powerConversionInputField.setReadOnly(True)
# To Combo Box
powerConversionToComboBox = QComboBox(powerConversionWidget)
powerConversionToComboBox.setFixedSize(480, 60)
powerConversionToComboBox.move(30, 360)
powerConversionToComboBox.setFont(comboBoxFont)
powerConversionToComboBox.setStyleSheet('padding-left: 10px')
powerConversionToComboBox.addItem('Watt (W) | Joules per second (J/s) | Newton-metres per second (N∙m/s)')          # 0
powerConversionToComboBox.addItem('Foot-pounds per second (ft∙lb/s)')                                               # 1
powerConversionToComboBox.addItem('Kilocalories per second (kcal/s)')                                               # 2
powerConversionToComboBox.addItem('Horsepower (HP)')                                                                # 3
# Output Field
powerConversionOutputField = QLineEdit(powerConversionWidget)
powerConversionOutputField.setFixedSize(480, 60)
powerConversionOutputField.move(30, 420)
powerConversionOutputField.setFont(outputFieldFont)
powerConversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
powerConversionOutputField.setPlaceholderText('Output')
powerConversionOutputField.setReadOnly(True)
# Paste Output to Input
powerConversionPasteButton = QPushButton('⇅', powerConversionWidget)
powerConversionPasteButton.setFixedSize(60, 270)
powerConversionPasteButton.move(510, 210)
powerConversionPasteButton.setFont(conversionPasteButtonFont)
powerConversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def powerConversionPaste():
    global powerConversionInput
    powerConversionFromIndex = powerConversionFromComboBox.currentIndex()
    powerConversionToIndex = powerConversionToComboBox.currentIndex()
    powerConversionFromComboBox.setCurrentIndex(powerConversionToIndex)
    powerConversionToComboBox.setCurrentIndex(powerConversionFromIndex)
    if powerConversionInputField.text():
        if powerConversionInputField.text().endswith('.'):
            powerConversionInputField.setText(powerConversionInputField.text().replace('.', ''))
            powerConversionInput = powerConversionInput.replace('.', '')
        powerConversionFrom = powerConversionFromComboBox.currentIndex()
        powerConversionTo = powerConversionToComboBox.currentIndex()
        powerConversionKey = (powerConversionFrom, powerConversionTo)
        powerConversionFactor = powerConversionFactors[powerConversionKey]
        powerConversionOutput = float(powerConversionInput) * powerConversionFactor
        powerConversionOutputField.setText(str(powerConversionOutput))
powerConversionPasteButton.clicked.connect(powerConversionPaste)
# Number Pad
# Nine [9]
powerConversionNineButton = QPushButton('9', powerConversionWidget)
powerConversionNineButton.setFixedSize(90, 90)
powerConversionNineButton.move(300, 510)
powerConversionNineButton.setFont(numberPadFont)
powerConversionNineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionNine():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '9')
    powerConversionInput += '9'
powerConversionNineButton.clicked.connect(powerConversionNine)
# Eight [8]
powerConversionEightButton = QPushButton('8', powerConversionWidget)
powerConversionEightButton.setFixedSize(90, 90)
powerConversionEightButton.move(210, 510)
powerConversionEightButton.setFont(numberPadFont)
powerConversionEightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionEight():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '8')
    powerConversionInput += '8'
powerConversionEightButton.clicked.connect(powerConversionEight)
# Seven [7]
powerConversionSevenButton = QPushButton('7', powerConversionWidget)
powerConversionSevenButton.setFixedSize(90, 90)
powerConversionSevenButton.move(120, 510)
powerConversionSevenButton.setFont(numberPadFont)
powerConversionSevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionSeven():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '7')
    powerConversionInput += '7'
powerConversionSevenButton.clicked.connect(powerConversionSeven)
# Six [6]
powerConversionSixButton = QPushButton('6', powerConversionWidget)
powerConversionSixButton.setFixedSize(90, 90)
powerConversionSixButton.move(300, 600)
powerConversionSixButton.setFont(numberPadFont)
powerConversionSixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionSix():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '6')
    powerConversionInput += '6'
powerConversionSixButton.clicked.connect(powerConversionSix)
# Five [5]
powerConversionFiveButton = QPushButton('5', powerConversionWidget)
powerConversionFiveButton.setFixedSize(90, 90)
powerConversionFiveButton.move(210, 600)
powerConversionFiveButton.setFont(numberPadFont)
powerConversionFiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionFive():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '5')
    powerConversionInput += '5'
powerConversionFiveButton.clicked.connect(powerConversionFive)
# Four [4]
powerConversionFourButton = QPushButton('4', powerConversionWidget)
powerConversionFourButton.setFixedSize(90, 90)
powerConversionFourButton.move(120, 600)
powerConversionFourButton.setFont(numberPadFont)
powerConversionFourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionFour():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '4')
    powerConversionInput += '4'
powerConversionFourButton.clicked.connect(powerConversionFour)
# Three [3]
powerConversionThreeButton = QPushButton('3', powerConversionWidget)
powerConversionThreeButton.setFixedSize(90, 90)
powerConversionThreeButton.move(300, 690)
powerConversionThreeButton.setFont(numberPadFont)
powerConversionThreeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionThree():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '3')
    powerConversionInput += '3'
powerConversionThreeButton.clicked.connect(powerConversionThree)
# Two [2]
powerConversionTwoButton = QPushButton('2', powerConversionWidget)
powerConversionTwoButton.setFixedSize(90, 90)
powerConversionTwoButton.move(210, 690)
powerConversionTwoButton.setFont(numberPadFont)
powerConversionTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionTwo():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '2')
    powerConversionInput += '2'
powerConversionTwoButton.clicked.connect(powerConversionTwo)
# One [1]
powerConversionOneButton = QPushButton('1', powerConversionWidget)
powerConversionOneButton.setFixedSize(90, 90)
powerConversionOneButton.move(120, 690)
powerConversionOneButton.setFont(numberPadFont)
powerConversionOneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionOne():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '1')
    powerConversionInput += '1'
powerConversionOneButton.clicked.connect(powerConversionOne)
# Zero [0]
powerConversionZeroButton = QPushButton('0', powerConversionWidget)
powerConversionZeroButton.setFixedSize(90, 90)
powerConversionZeroButton.move(210, 780)
powerConversionZeroButton.setFont(numberPadFont)
powerConversionZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionZero():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '0')
    powerConversionInput += '0'
powerConversionZeroButton.clicked.connect(powerConversionZero)
# Double Zero [00]
powerConversionDoubleZeroButton = QPushButton('00', powerConversionWidget)
powerConversionDoubleZeroButton.setFixedSize(90, 90)
powerConversionDoubleZeroButton.move(120, 780)
powerConversionDoubleZeroButton.setFont(numberPadFont)
powerConversionDoubleZeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def powerConversionDoubleZero():
    global powerConversionInput
    powerConversionInputField.setText(powerConversionInputField.text() + '00')
    powerConversionInput += '00'
powerConversionDoubleZeroButton.clicked.connect(powerConversionDoubleZero)
# Point [.]
powerConversionPointButton = QPushButton('.', powerConversionWidget)
powerConversionPointButton.setFixedSize(90, 90)
powerConversionPointButton.move(300, 780)
powerConversionPointButton.setFont(numberPadFont)
powerConversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def powerConversionPoint():
    global powerConversionInput
    if powerConversionInputField.text():
        powerConversionInputField.setText(powerConversionInputField.text() + '.')
        powerConversionInput += '.'
    else:
        powerConversionInputField.setText(powerConversionInputField.text() + '0.')
        powerConversionInput += '0.'
powerConversionPointButton.clicked.connect(powerConversionPoint)
# Deletion
# All Clear
powerConversionAllClearButton = QPushButton('AC', powerConversionWidget)
powerConversionAllClearButton.setFixedSize(90, 90)
powerConversionAllClearButton.move(390, 510)
powerConversionAllClearButton.setFont(operatorButtonFont)
powerConversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def powerConversionAllClear():
    global powerConversionInput
    powerConversionInputField.setText('')
    powerConversionOutputField.setText('')
    powerConversionInput = ''
powerConversionAllClearButton.clicked.connect(powerConversionAllClear)
# Clear [Backspace]
powerConversionClearButton = QPushButton('C', powerConversionWidget)
powerConversionClearButton.setFixedSize(90, 90)
powerConversionClearButton.move(390, 600)
powerConversionClearButton.setFont(operatorButtonFont)
powerConversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def powerConversionClear():
    global powerConversionInput
    powerConversionInputFieldText = powerConversionInputField.text()
    powerConversionInputFieldText = powerConversionInputFieldText[:-1]
    powerConversionInputField.setText(powerConversionInputFieldText)
    powerConversionInput = powerConversionInput[:-1]
powerConversionClearButton.clicked.connect(powerConversionClear)
# Result [=]
powerConversionResultButton = QPushButton('=', powerConversionWidget)
powerConversionResultButton.setFixedSize(90, 180)
powerConversionResultButton.move(390, 690)
powerConversionResultButton.setFont(resultButtonsFont)
powerConversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def powerConversionResult():
    global powerConversionInput
    if powerConversionInputField.text():
        if powerConversionInputField.text().endswith('.'):
            powerConversionInputField.setText(powerConversionInputField.text().replace('.', ''))
            powerConversionInput = powerConversionInput.replace('.', '')
        powerConversionFrom = powerConversionFromComboBox.currentIndex()
        powerConversionTo = powerConversionToComboBox.currentIndex()
        powerConversionKey = (powerConversionFrom, powerConversionTo)
        powerConversionFactor = powerConversionFactors[powerConversionKey]
        powerConversionOutput = float(powerConversionInput) * powerConversionFactor
        powerConversionOutputField.setText(str(powerConversionOutput))
powerConversionResultButton.clicked.connect(powerConversionResult)

window.show()
CalcWizard.exec()

# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QDialog
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
# Conversion Essentials
from conversionUnits import currencyUnits, lengthUnits, areaUnits, volumeUnits, weightUnits, temperatureUnits, speedUnits, pressureUnits, powerUnits
from conversionFactors import currencyConversionFactors, lengthConversionFactors, areaConversionFactors, volumeConversionFactors, weightConversionFactors, temperatureConversionFactors, speedConversionFactors, pressureConversionFactors, powerConversionFactors

if getattr(sys, 'frozen', False):
    baseDir = sys._MEIPASS # type: ignore
else:
    baseDir = dirname(abspath(__file__))
iconPath = join(baseDir, 'icon.ico')

API_KEY = environ.get('CW_CURRENCY_API_KEY')

def saveAPI(key):
    global API_KEY
    API_KEY = key
    environ['CW_CURRENCY_API_KEY'] = key
    try:
        from subprocess import run
        run(['setx', 'CW_CURRENCY_API_KEY', key], check = False, capture_output = True)
    except Exception as e:
        errorMessageBox.setIcon(QMessageBox.Icon.Warning)
        errorMessageBox.setWindowTitle('Warning')
        errorMessageBox.setText(f'Could not save API key to system environment: {e}')
        errorMessageBox.exec()

CalcWizard = QApplication([])
# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)
window.setWindowIcon(QIcon(iconPath))

# Pop-ups
# Error Message
errorMessageBox = QMessageBox()
errorMessageBox.setWindowIcon(QIcon(iconPath))
# API Key Dialog Box
class APIKeyDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('API Key Input')
        self.setWindowIcon(QIcon(iconPath))
        self.setFixedSize(400, 150)
        # Label with clickable link
        self.label = QLabel('Enter your API Key (<a href = "https://www.exchangerate-api.com/">ExchangeRate-API</a>)', self)
        self.label.setGeometry(10, 20, 380, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setOpenExternalLinks(True)
        self.label.show()
        # Input Field
        self.apiInput = QLineEdit(self)
        self.apiInput.setGeometry(50, 60, 300, 30)
        self.apiInput.show()
        # OK Button
        self.okButton = QPushButton('OK', self)
        self.okButton.setGeometry(120, 100, 80, 30)
        self.okButton.clicked.connect(self.accept)
        self.okButton.show()
        # Cancel Button
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.setGeometry(210, 100, 80, 30)
        self.cancelButton.clicked.connect(self.reject)
        self.cancelButton.show()

    def getAPIKey(self):
        return self.apiInput.text()

# QStackedWidget Instance
stackedWidget = QStackedWidget(window)
window.setCentralWidget(stackedWidget)

# Calculator Page
calculatorWidget = QWidget()
stackedWidget.addWidget(calculatorWidget)
class calculatorPage:
    def __init__(self):
        self.stackedWidget = stackedWidget
        self.parentWidget = calculatorWidget

        self.calculatorInputValue = ''

        self.widget = QWidget()

        self.createCalculatorPageHeader()
        self.createCalculatorTextFields()
        self.createCalculatorPasteButton()
        self.createCalculatorNumberPad()
        self.createCalculatorOperationButtons()
        self.createCalculatorControlButtons()
        self.createCalculatorModeButton()
        self.createCalculatorBracketButtons()
        self.createCalculatorTrigonometryButtons()
        self.createCalculatorAngleButton()
        self.createCalculatorLogarithmButtons()
        self.createCalculatorExponentButtons()
        self.createCalculatorConstantButtons()
        self.createCalculatorInverseButton()

    def createCalculatorPageHeader(self):
        # Switch to Conversions Button
        self.switchToConversionsButton = QPushButton('⇄', self.parentWidget)
        self.switchToConversionsButton.setGeometry(510, 30, 60, 60)
        self.switchToConversionsButton.setFont(QFont(self.switchToConversionsButton.font().family(), 39, QFont.Weight.Bold))
        self.switchToConversionsButton.clicked.connect(self.switchToConversions)
        # Page Label
        self.calculatorLabel = QLabel('CALCULATOR', self.parentWidget)
        self.calculatorLabel.setGeometry(30, 120, 540, 60)
        self.calculatorLabel.setFont(QFont(self.calculatorLabel.font().family(), 39, QFont.Weight.Bold))
        self.calculatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def createCalculatorTextFields(self):
        # Input Field
        self.calculatorInputField = QLineEdit(self.parentWidget)
        self.calculatorInputField.setPlaceholderText('Input')
        self.calculatorInputField.setGeometry(30, 210, 540, 60)
        self.calculatorInputField.setFont(QFont(self.calculatorInputField.font().family(), 21, QFont.Weight.Bold))
        self.calculatorInputField.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.calculatorInputField.setStyleSheet('border: 2px solid; padding-right: 15px')
        self.calculatorInputField.setReadOnly(True)
        # Output Field
        self.calculatorOutputField = QLineEdit(self.parentWidget)
        self.calculatorOutputField.setGeometry(30, 300, 540, 60)
        self.calculatorOutputField.setFont(QFont(self.calculatorOutputField.font().family(), 21, QFont.Weight.Bold))
        self.calculatorOutputField.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.calculatorOutputField.setStyleSheet('border: 2px solid; padding-right: 15px')
        self.calculatorOutputField.setPlaceholderText('Output')
        self.calculatorOutputField.setReadOnly(True)

    def createCalculatorPasteButton(self):
        self.calculatorPasteButton = QPushButton('↑', self.parentWidget)
        self.calculatorPasteButton.setGeometry(540, 270, 30, 30)
        self.calculatorPasteButton.setFont(QFont(self.calculatorPasteButton.font().family(), 15, QFont.Weight.Bold))
        self.calculatorPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
        self.calculatorPasteButton.clicked.connect(self.calculatorPaste)

    def createCalculatorNumberPad(self):
        # Point [.]
        self.calculatorPointButton = QPushButton('.', self.parentWidget)
        self.calculatorPointButton.setGeometry(300, 840, 90, 90)
        self.calculatorPointButton.setFont(QFont(self.calculatorPointButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
        self.calculatorPointButton.clicked.connect(self.calculatorPoint)
        # Digits
        self.calculatorDigitButtons = {}
        calculatorDigitPositions = {
            '7': (120, 570), '8': (210, 570), '9': (300, 570),
            '4': (120, 660), '5': (210, 660), '6': (300, 660),
            '1': (120, 750), '2': (210, 750), '3': (300, 750),
            '0': (210, 840)
        }
        for calculatorDigit, calculatorDigitPosition in calculatorDigitPositions.items():
            calculatorDigitButton = QPushButton(calculatorDigit, self.parentWidget)
            calculatorDigitButton.setGeometry(*calculatorDigitPosition, 90, 90)
            calculatorDigitButton.setFont(QFont(calculatorDigitButton.font().family(), 27, QFont.Weight.Bold))
            calculatorDigitButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
            calculatorDigitButton.clicked.connect(
                lambda _, calD = calculatorDigit: self.addCalculatorDigit(calD)
            )
            self.calculatorDigitButtons[calculatorDigit] = calculatorDigitButton

    def createCalculatorOperationButtons(self):
        self.calculatorOperationButtons = {}
        calculatorOperationFunctions = {
            '+': '+', '-': '-',
            '×': '*', '÷': '/',
            '%': '/100'
        }
        calculatorOperationPositions = {
            '+': (390, 660), '-': (480, 660),
            '×': (390, 750), '÷': (480, 750),
            '%': (30, 570)
        }

        for calculatorOperation, calculatorOperationPosition in calculatorOperationPositions.items():
            calculatorOperationButton = QPushButton(calculatorOperation, self.parentWidget)
            calculatorOperationButton.setGeometry(*calculatorOperationPosition, 90, 90)
            calculatorOperationButton.setFont(QFont(calculatorOperationButton.font().family(), 33, QFont.Weight.Bold))
            calculatorOperationButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')

            calculatorOperationButton.clicked.connect(
                lambda _, displayOp = calculatorOperation,
                functionOp = calculatorOperationFunctions[calculatorOperation]: self.addCalculatorOperation(displayOp, functionOp)
            )
            self.calculatorOperationButtons[calculatorOperation] = calculatorOperationButton

    def createCalculatorModeButton(self):
        self.calculatorModeButton = QPushButton('∞', self.parentWidget)
        self.calculatorModeButton.setGeometry(30, 390, 90, 90)
        self.calculatorModeButton.setFont(QFont(self.calculatorModeButton.font().family(), 36, QFont.Weight.Bold))
        self.calculatorModeButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 255)')
        self.calculatorModeButton.setCheckable(True)
        self.calculatorModeButton.clicked.connect(self.calculatorMode)

    def createCalculatorBracketButtons(self):
        # Open Bracket [(]
        self.openBracketButton = QPushButton('(', self.parentWidget)
        self.openBracketButton.setGeometry(390, 570, 90, 90)
        self.openBracketButton.setFont(QFont(self.openBracketButton.font().family(), 33, QFont.Weight.Bold))
        self.openBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
        self.openBracketButton.setVisible(False)
        self.openBracketButton.clicked.connect(self.openBracket)
        # Close Bracket [)]
        self.closeBracketButton = QPushButton(')', self.parentWidget)
        self.closeBracketButton.setGeometry(480, 570, 90, 90)
        self.closeBracketButton.setFont(QFont(self.closeBracketButton.font().family(), 33, QFont.Weight.Bold))
        self.closeBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
        self.closeBracketButton.setVisible(False)
        self.closeBracketButton.clicked.connect(self.closeBracket)

    def createCalculatorTrigonometryButtons(self):
        # Sine
        self.calculatorSineButton = QPushButton('sin', self.parentWidget)
        self.calculatorSineButton.setGeometry(120, 390, 90, 90)
        self.calculatorSineButton.setFont(QFont(self.calculatorSineButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorSineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorSineButton.setVisible(False)
        self.calculatorSineButton.clicked.connect(self.calculatorSine)
        # Cosine
        self.calculatorCosineButton = QPushButton('cos', self.parentWidget)
        self.calculatorCosineButton.setGeometry(210, 390, 90, 90)
        self.calculatorCosineButton.setFont(QFont(self.calculatorCosineButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorCosineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorCosineButton.setVisible(False)
        self.calculatorCosineButton.clicked.connect(self.calculatorCosine)
        # Tangent
        self.calculatorTangentButton = QPushButton('tan', self.parentWidget)
        self.calculatorTangentButton.setGeometry(300, 390, 90, 90)
        self.calculatorTangentButton.setFont(QFont(self.calculatorTangentButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorTangentButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorTangentButton.setVisible(False)
        self.calculatorTangentButton.clicked.connect(self.calculatorTangent)
        # Sine Inverse
        self.calculatorSineInverseButton = QPushButton('sin⁻¹', self.parentWidget)
        self.calculatorSineInverseButton.setGeometry(120, 390, 90, 90)
        self.calculatorSineInverseButton.setFont(QFont(self.calculatorSineInverseButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorSineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorSineInverseButton.setVisible(False)
        self.calculatorSineInverseButton.clicked.connect(self.calculatorSineInverse)
        # Cosine Inverse
        self.calculatorCosineInverseButton = QPushButton('cos⁻¹', self.parentWidget)
        self.calculatorCosineInverseButton.setGeometry(210, 390, 90, 90)
        self.calculatorCosineInverseButton.setFont(QFont(self.calculatorCosineInverseButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorCosineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorCosineInverseButton.setVisible(False)
        self.calculatorCosineInverseButton.clicked.connect(self.calculatorCosineInverse)
        # Tangent Inverse
        self.calculatorTangentInverseButton = QPushButton('tan⁻¹', self.parentWidget)
        self.calculatorTangentInverseButton.setGeometry(300, 390, 90, 90)
        self.calculatorTangentInverseButton.setFont(QFont(self.calculatorTangentInverseButton.font().family(), 18, QFont.Weight.Bold))
        self.calculatorTangentInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
        self.calculatorTangentInverseButton.setVisible(False)
        self.calculatorTangentInverseButton.clicked.connect(self.calculatorTangentInverse)

    def createCalculatorAngleButton(self):
        self.calculatorAngleButton = QPushButton('RAD', self.parentWidget)
        self.calculatorAngleButton.setGeometry(390, 390, 180, 90)
        self.calculatorAngleButton.setFont(QFont(self.calculatorAngleButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorAngleButton.setStyleSheet('border: 2px solid; background-color: rgb(200, 180, 160)')
        self.calculatorAngleButton.setVisible(False)
        self.calculatorAngleButton.setCheckable(True)
        self.calculatorAngleButton.clicked.connect(self.calculatorAngle)

    def createCalculatorLogarithmButtons(self):
        # Logarithm
        # Base 10 Log
        self.calculatorBaseTenLogButton = QPushButton('log⏨', self.parentWidget)
        self.calculatorBaseTenLogButton.setGeometry(120, 480, 90, 90)
        self.calculatorBaseTenLogButton.setFont(QFont(self.calculatorBaseTenLogButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorBaseTenLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorBaseTenLogButton.setVisible(False)
        self.calculatorBaseTenLogButton.clicked.connect(self.calculatorBaseTenLog)
        # Base 2 Log
        self.calculatorBaseTwoLogButton = QPushButton('log₂', self.parentWidget)
        self.calculatorBaseTwoLogButton.setGeometry(210, 480, 90, 90)
        self.calculatorBaseTwoLogButton.setFont(QFont(self.calculatorBaseTwoLogButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorBaseTwoLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorBaseTwoLogButton.setVisible(False)
        self.calculatorBaseTwoLogButton.clicked.connect(self.calculatorBaseTwoLog)
        # Natural Log
        self.calculatorNaturalLogButton = QPushButton('ln', self.parentWidget)
        self.calculatorNaturalLogButton.setGeometry(300, 480, 90, 90)
        self.calculatorNaturalLogButton.setFont(QFont(self.calculatorNaturalLogButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorNaturalLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorNaturalLogButton.setVisible(False)
        self.calculatorNaturalLogButton.clicked.connect(self.calculatorNaturalLog)
        # Logarithm Buttons Inverse
        # Exponents of 10
        self.calculatorPowerTenButton = QPushButton('10ˣ', self.parentWidget)
        self.calculatorPowerTenButton.setGeometry(120, 480, 90, 90)
        self.calculatorPowerTenButton.setFont(QFont(self.calculatorPowerTenButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorPowerTenButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorPowerTenButton.setVisible(False)
        self.calculatorPowerTenButton.clicked.connect(self.calculatorPowerTen)
        # Exponent of 2
        self.calculatorPowerTwoButton = QPushButton('2ˣ', self.parentWidget)
        self.calculatorPowerTwoButton.setGeometry(210, 480, 90, 90)
        self.calculatorPowerTwoButton.setFont(QFont(self.calculatorPowerTwoButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorPowerTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorPowerTwoButton.setVisible(False)
        self.calculatorPowerTwoButton.clicked.connect(self.calculatorPowerTwo)
        # Exponents of e
        self.calculatorPowerEulerButton = QPushButton('eˣ', self.parentWidget)
        self.calculatorPowerEulerButton.setGeometry(300, 480, 90, 90)
        self.calculatorPowerEulerButton.setFont(QFont(self.calculatorPowerEulerButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorPowerEulerButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
        self.calculatorPowerEulerButton.setVisible(False)
        self.calculatorPowerEulerButton.clicked.connect(self.calculatorPowerEuler)

    def createCalculatorExponentButtons(self):
        # Square [x²]
        self.calculatorSquareButton = QPushButton('x²', self.parentWidget)
        self.calculatorSquareButton.setGeometry(30, 660, 90, 90)
        self.calculatorSquareButton.setFont(QFont(self.calculatorSquareButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorSquareButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
        self.calculatorSquareButton.setVisible(False)
        self.calculatorSquareButton.clicked.connect(self.calculatorSquare)
        # Exponent
        self.calculatorExponentButton = QPushButton('^', self.parentWidget)
        self.calculatorExponentButton.setGeometry(30, 750, 90, 90)
        self.calculatorExponentButton.setFont(QFont(self.calculatorExponentButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorExponentButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
        self.calculatorExponentButton.setVisible(False)
        self.calculatorExponentButton.clicked.connect(self.calculatorExponent)

    def createCalculatorConstantButtons(self):
        # pi [π]
        self.calculatorPiButton = QPushButton('π', self.parentWidget)
        self.calculatorPiButton.setGeometry(30, 840, 90, 90)
        self.calculatorPiButton.setFont(QFont(self.calculatorPiButton.font().family(), 27, QFont.Weight.Bold, True))
        self.calculatorPiButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
        self.calculatorPiButton.setVisible(False)
        self.calculatorPiButton.clicked.connect(self.calculatorPiCharacter)
        # Euler's Number [e]
        self.calculatorEulerButton = QPushButton('e', self.parentWidget)
        self.calculatorEulerButton.setGeometry(120, 840, 90, 90)
        self.calculatorEulerButton.setFont(QFont(self.calculatorEulerButton.font().family(), 27, QFont.Weight.Bold, True))
        self.calculatorEulerButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
        self.calculatorEulerButton.setVisible(False)
        self.calculatorEulerButton.clicked.connect(self.calculatorEulerNumber)

    def createCalculatorInverseButton(self):
        self.calculatorInverseButton = QPushButton('INV', self.parentWidget)
        self.calculatorInverseButton.setGeometry(30, 480, 90, 90)
        self.calculatorInverseButton.setFont(QFont(self.calculatorInverseButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(128, 128, 128)')
        self.calculatorInverseButton.setVisible(False)
        self.calculatorInverseButton.setCheckable(True)
        self.calculatorInverseButton.clicked.connect(self.calculatorInverse)

    def createCalculatorControlButtons(self):
        # All Clear
        self.calculatorAllClearButton = QPushButton('AC', self.parentWidget)
        self.calculatorAllClearButton.setGeometry(390, 480, 90, 90)
        self.calculatorAllClearButton.setFont(QFont(self.calculatorAllClearButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
        self.calculatorAllClearButton.clicked.connect(self.calculatorAllClear)
        # Clear [Backspace]
        self.calculatorClearButton = QPushButton('C', self.parentWidget)
        self.calculatorClearButton.setGeometry(480, 480, 90, 90)
        self.calculatorClearButton.setFont(QFont(self.calculatorClearButton.font().family(), 27, QFont.Weight.Bold))
        self.calculatorClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
        self.calculatorClearButton.clicked.connect(self.calculatorClear)
        # Result [=]
        self.calculatorResultButton = QPushButton('=', self.parentWidget)
        self.calculatorResultButton.setGeometry(390, 840, 180, 90)
        self.calculatorResultButton.setFont(QFont(self.calculatorResultButton.font().family(), 33, QFont.Weight.Bold))
        self.calculatorResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
        self.calculatorResultButton.clicked.connect(self.calculatorResult)

    def switchToConversions(self):
        self.stackedWidget.setCurrentWidget(conversionsWidget)

    def addCalculatorDigit(self, calculatorDigit):
        self.calculatorInputField.setText(self.calculatorInputField.text() + calculatorDigit)
        self.calculatorInputValue += calculatorDigit

    def calculatorPoint(self):
        if self.calculatorInputField.text():
            self.calculatorInputField.setText(self.calculatorInputField.text() + '.')
            self.calculatorInputValue += '.'
        else:
            self.calculatorInputField.setText(self.calculatorInputField.text() + '0.')
            self.calculatorInputValue += '0.'

    def addCalculatorOperation(self, displayOperation, functionOperation):
        if self.calculatorInputField.text():
            self.calculatorInputField.setText(self.calculatorInputField.text() + displayOperation)
            self.calculatorInputValue += functionOperation

    def openBracket(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + '(')
        self.calculatorInputValue += '('

    def closeBracket(self):
        if self.calculatorInputField.text():
            self.calculatorInputField.setText(self.calculatorInputField.text() + ')')
            if self.calculatorAngleButton.isChecked():
                self.calculatorInputValue += '))'
            else:
                self.calculatorInputValue += ')'

    def calculatorSine(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'sin(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'sin(radians('
        else:
            self.calculatorInputValue += 'sin('

    def calculatorCosine(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'cos(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'cos(radians('
        else:
            self.calculatorInputValue += 'cos('

    def calculatorTangent(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'tan(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'tan(radians('
        else:
            self.calculatorInputValue += 'tan('

    def calculatorSineInverse(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'sin⁻¹(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'asin(radians('
        else:
            self.calculatorInputValue += 'asin('

    def calculatorCosineInverse(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'cos⁻¹(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'acos(radians('
        else:
            self.calculatorInputValue += 'acos('

    def calculatorTangentInverse(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'tan⁻¹(')
        if self.calculatorAngleButton.isChecked():
            self.calculatorInputValue += 'atan(radians('
        else:
            self.calculatorInputValue += 'atan('

    def calculatorAngle(self):
        if self.calculatorAngleButton.isChecked():
            self.calculatorAngleButton.setText('DEG')
        else:
            self.calculatorAngleButton.setText('RAD')

    def calculatorBaseTenLog(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'log⏨(')
        self.calculatorInputValue += 'log10('

    def calculatorBaseTwoLog(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'log₂(')
        self.calculatorInputValue += 'log2('

    def calculatorNaturalLog(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'ln(')
        self.calculatorInputValue += 'log('

    def calculatorPowerTen(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + '10^')
        self.calculatorInputValue += '10**'

    def calculatorPowerTwo(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + '2^')
        self.calculatorInputValue += '2**'

    def calculatorPowerEuler(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'e^')
        self.calculatorInputValue += 'e**'

    def calculatorSquare(self):
        if self.calculatorInputField.text():
            self.calculatorInputField.setText(self.calculatorInputField.text() + '²')
            self.calculatorInputValue += '**(2)'

    def calculatorExponent(self):
        if self.calculatorInputField.text():
            self.calculatorInputField.setText(self.calculatorInputField.text() + '^')
            self.calculatorInputValue += '**'

    def calculatorPiCharacter(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'π')
        self.calculatorInputValue += 'pi'

    def calculatorEulerNumber(self):
        self.calculatorInputField.setText(self.calculatorInputField.text() + 'e')
        self.calculatorInputValue += 'e'

    def calculatorInverse(self):
        if self.calculatorInverseButton.isChecked():
            self.calculatorSineButton.setVisible(False)
            self.calculatorCosineButton.setVisible(False)
            self.calculatorTangentButton.setVisible(False)
            self.calculatorBaseTenLogButton.setVisible(False)
            self.calculatorBaseTwoLogButton.setVisible(False)
            self.calculatorNaturalLogButton.setVisible(False)
            self.calculatorSineInverseButton.setVisible(True)
            self.calculatorCosineInverseButton.setVisible(True)
            self.calculatorTangentInverseButton.setVisible(True)
            self.calculatorPowerTenButton.setVisible(True)
            self.calculatorPowerTwoButton.setVisible(True)
            self.calculatorPowerEulerButton.setVisible(True)
        else:
            self.calculatorSineButton.setVisible(True)
            self.calculatorCosineButton.setVisible(True)
            self.calculatorTangentButton.setVisible(True)
            self.calculatorBaseTenLogButton.setVisible(True)
            self.calculatorBaseTwoLogButton.setVisible(True)
            self.calculatorNaturalLogButton.setVisible(True)
            self.calculatorSineInverseButton.setVisible(False)
            self.calculatorCosineInverseButton.setVisible(False)
            self.calculatorTangentInverseButton.setVisible(False)
            self.calculatorPowerTenButton.setVisible(False)
            self.calculatorPowerTwoButton.setVisible(False)
            self.calculatorPowerEulerButton.setVisible(False)

    def calculatorPaste(self):
        if self.calculatorOutputField.text():
            self.calculatorInputField.setText(self.calculatorOutputField.text())
            self.calculatorInputValue = str(self.calculatorOutputField.text())
            self.calculatorOutputField.setText('')

    def calculatorAllClear(self):
        self.calculatorInputField.setText('')
        self.calculatorOutputField.setText('')
        self.calculatorInputValue = ''

    def calculatorClear(self):
        if self.calculatorInputField.text():
            if self.calculatorInputField.text().endswith('sin('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('sin(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('sin(', '')
            elif self.calculatorInputField.text().endswith('cos('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('cos(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('cos(', '')
            elif self.calculatorInputField.text().endswith('tan('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('tan(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('tan(', '')
            elif self.calculatorInputField.text().endswith('sin⁻¹('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('sin⁻¹(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('atan(', '')
            elif self.calculatorInputField.text().endswith('log⏨('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('log⏨(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('log10(', '')
            elif self.calculatorInputField.text().endswith('log₂('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('log₂(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('log2(', '')
            elif self.calculatorInputField.text().endswith('ln('):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('ln(', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('log(', '')
            elif self.calculatorInputField.text().endswith('10^'):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('10^', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('10**', '')
            elif self.calculatorInputField.text().endswith('2^'):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('2^', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('2**', '')
            elif self.calculatorInputField.text().endswith('e^'):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('e^', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('e**', '')
            elif self.calculatorInputField.text().endswith('²'):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('²', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('**(2)', '')
            elif self.calculatorInputField.text().endswith('^'):
                self.calculatorInputField.setText(self.calculatorInputField.text().replace('^', ''))
                self.calculatorInputValue = self.calculatorInputValue.replace('**', '')
            else:
                self.calculatorInputFieldText = self.calculatorInputField.text()
                self.calculatorInputFieldText = self.calculatorInputFieldText[:-1]
                self.calculatorInputField.setText(self.calculatorInputFieldText)
                self.calculatorInputValue = self.calculatorInputValue[:-1]

    def calculatorMode(self):
        if self.calculatorModeButton.isChecked():                    # Advanced Mode
            self.calculatorModeButton.setText('±')
            self.openBracketButton.setVisible(True)
            self.closeBracketButton.setVisible(True)
            self.calculatorSineButton.setVisible(True)
            self.calculatorCosineButton.setVisible(True)
            self.calculatorTangentButton.setVisible(True)
            self.calculatorAngleButton.setVisible(True)
            self.calculatorBaseTenLogButton.setVisible(True)
            self.calculatorBaseTwoLogButton.setVisible(True)
            self.calculatorNaturalLogButton.setVisible(True)
            self.calculatorInverseButton.setVisible(True)
            self.calculatorSquareButton.setVisible(True)
            self.calculatorExponentButton.setVisible(True)
            self.calculatorPiButton.setVisible(True)
            self.calculatorEulerButton.setVisible(True)
        else:                                                       # Basic Mode
            self.calculatorModeButton.setText('∞')
            self.openBracketButton.setVisible(False)
            self.closeBracketButton.setVisible(False)
            self.calculatorSineButton.setVisible(False)
            self.calculatorCosineButton.setVisible(False)
            self.calculatorTangentButton.setVisible(False)
            self.calculatorSineInverseButton.setVisible(False)
            self.calculatorCosineInverseButton.setVisible(False)
            self.calculatorTangentInverseButton.setVisible(False)
            self.calculatorAngleButton.setVisible(False)
            self.calculatorAngleButton.setChecked(False)
            self.calculatorBaseTenLogButton.setVisible(False)
            self.calculatorBaseTwoLogButton.setVisible(False)
            self.calculatorNaturalLogButton.setVisible(False)
            self.calculatorPowerTenButton.setVisible(False)
            self.calculatorPowerTwoButton.setVisible(False)
            self.calculatorPowerEulerButton.setVisible(False)
            self.calculatorInverseButton.setVisible(False)
            self.calculatorInverseButton.setChecked(False)
            self.calculatorSquareButton.setVisible(False)
            self.calculatorExponentButton.setVisible(False)
            self.calculatorPiButton.setVisible(False)
            self.calculatorEulerButton.setVisible(False)

    def calculatorResult(self):
        try:
            if self.calculatorInputField.text():
                if self.calculatorInputField.text().endswith('.'):
                    self.calculatorInputField.setText(self.calculatorInputField.text().replace('.', ''))
                    self.calculatorInputValue = self.calculatorInputValue.replace('.', '')
                self.calculatorOutputField.setText(str(eval(self.calculatorInputValue)))
        except Exception as err:
            errorMessage = str(err)
            errorMessage = errorMessage.replace('(<string>, line 1)', '')
            errorMessageBox.critical(self.widget, 'Error', f'An error occurred: {errorMessage}\nScript: {self.calculatorInputValue}')
calculator = calculatorPage()

# Note Label
def createNoteLabel(parent):
    noteLabel = QLabel('<b>⚠️ NOTE:</b> Currency Conversion requires Internet Connection', parent)
    noteLabel.setGeometry(30, 900, 540, 30)
    noteLabel.setFont(QFont(noteLabel.font().family(), 15))
    noteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Conversions Page
conversionsWidget = QWidget()
stackedWidget.addWidget(conversionsWidget)
# Switch to Calculator Button
conversionsSwitchToCalculatorButton = QPushButton('⇄', conversionsWidget)
conversionsSwitchToCalculatorButton.setGeometry(510, 30, 60, 60)
conversionsSwitchToCalculatorButton.setFont(QFont(conversionsSwitchToCalculatorButton.font().family(), 39, QFont.Weight.Bold))
def conversionsSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
conversionsSwitchToCalculatorButton.clicked.connect(conversionsSwitchToCalculator)
# Conversions Page Main Label
conversionsLabel = QLabel('CONVERSIONS', conversionsWidget)
conversionsLabel.setGeometry(30, 120, 540, 60)
conversionsLabel.setFont(QFont(conversionsLabel.font().family(), 39, QFont.Weight.Bold))
conversionsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# Conversion Page Buttons
def createGoToConversionCombos(goToConversionsParent):
    goToConversionButtons = {}
    goToConversionDestinations = {
        '💲': 'currencyConversion', '📏': 'lengthConversion', '🏁': 'areaConversion',
        '🧊': 'volumeConversion', '⚖️': 'weightConversion', '🌡️': 'temperatureConversion',
        '🏎️': 'speedConversion', '⏱️': 'pressureConversion', '💪': 'powerConversion'
    }
    goToConversionButtonPositions = {
        '💲': (60, 240), '📏': (240, 240), '🏁': (420, 240),
        '🧊': (60, 450), '⚖️': (240, 450), '🌡️': (420, 450),
        '🏎️': (60, 660), '⏱️': (240, 660), '💪': (420, 660)
    }

    for goToConversionB, goToConversionButtonPosition in goToConversionButtonPositions.items():
        goToConversionButton = QPushButton(goToConversionB, goToConversionsParent)
        goToConversionButton.setGeometry(*goToConversionButtonPosition, 120, 120)
        goToConversionButton.setFont(QFont(goToConversionButton.font().family(), 60, QFont.Weight.Bold))
        goToConversionButton.setStyleSheet('border: 2px solid; background-color: rgb(217, 190, 240)')

        conversionDestination = goToConversionDestinations[goToConversionB]
        goToConversionButton.clicked.connect(createButtonClickHandler(conversionDestination))
        goToConversionButtons[goToConversionB] = goToConversionButton

    goToConversionLabels = {}
    goToConversionLabelPositions = {
        'Currency': (60, 360), 'Length': (240, 360), 'Area': (420, 360),
        'Volume': (60, 570), 'Weight': (240, 570), 'Temperature': (420, 570),
        'Speed': (60, 780), 'Pressure': (240, 780), 'Power': (420, 780)
    }

    for goToConversionL, goToConversionLabelPosition in goToConversionLabelPositions.items():
        goToConversionLabel = QLabel(goToConversionL, goToConversionsParent)
        goToConversionLabel.setGeometry(*goToConversionLabelPosition, 120, 30)
        goToConversionLabel.setFont(QFont(goToConversionLabel.font().family(), 15, QFont.Weight.Bold))
        goToConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        goToConversionLabels[goToConversionL] = goToConversionLabel
    return goToConversionButtons, goToConversionLabels
def createButtonClickHandler(destination):
    return lambda: addGoToConversion(destination)
def addGoToConversion(goToConversionDestination):
    conversionObject = globals()[goToConversionDestination]
    stackedWidget.setCurrentWidget(conversionObject.widget)
goToConversionCombos = createGoToConversionCombos(conversionsWidget)
# Note for Currency Conversion
conversionsPageNoteLabel = createNoteLabel(conversionsWidget)

# Conversion Page
class conversionPage:
    def __init__(self, name, units, conversionFactors):
        self.label = name
        self.unitOptions = units
        self.conversion = conversionFactors
        self.stackedWidget = stackedWidget
        self.parentWidget = conversionsWidget
        self.calculatorWidget = calculatorWidget

        self.conversionInputValue = ''

        self.widget = QWidget()
        self.stackedWidget.addWidget(self.widget)

        self.createConversionPageHeader()
        self.createComboBoxes()
        self.createConversionTextFields()
        self.createConversionPasteButton()
        self.createConversionNumberPad()
        self.createConversionControlButtons()

    def createConversionPageHeader(self):
        # Back Button
        self.backButton = QPushButton('←', self.widget)
        self.backButton.setGeometry(30, 30, 60, 60)
        self.backButton.setFont(QFont(self.backButton.font().family(), 39, QFont.Weight.Bold))
        self.backButton.clicked.connect(self.back)
        # Switch to Calculator Button
        self.switchToCalculatorButton = QPushButton('⇄', self.widget)
        self.switchToCalculatorButton.setGeometry(510, 30, 60, 60)
        self.switchToCalculatorButton.setFont(QFont(self.switchToCalculatorButton.font().family(), 39, QFont.Weight.Bold))
        self.switchToCalculatorButton.clicked.connect(self.switchToCalculator)
        # Page Label
        self.pageLabel = QLabel(f'{self.label} Conversion', self.widget)
        self.pageLabel.setGeometry(30, 120, 540, 60)
        self.pageLabel.setFont(QFont(self.pageLabel.font().family(), 30, QFont.Weight.Bold))
        self.pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def createComboBoxes(self):
        # From ComboBox
        self.fromComboBox = QComboBox(self.widget)
        self.fromComboBox.setGeometry(30, 210, 480, 60)
        self.fromComboBox.setFont(QFont(self.fromComboBox.font().family(), 10, QFont.Weight.Bold, True))
        self.fromComboBox.setStyleSheet('padding-left: 10px')
        for option in self.unitOptions:
            self.fromComboBox.addItem(option)
        # To ComboBox
        self.toComboBox = QComboBox(self.widget)
        self.toComboBox.setGeometry(30, 360, 480, 60)
        self.toComboBox.setFont(QFont(self.toComboBox.font().family(), 10, QFont.Weight.Bold, True))
        self.toComboBox.setStyleSheet('padding-left: 10px')
        for option in self.unitOptions:
            self.toComboBox.addItem(option)

    def createConversionTextFields(self):
        # Input Field
        self.conversionInputField = QLineEdit(self.widget)
        self.conversionInputField.setPlaceholderText('Input')
        self.conversionInputField.setGeometry(30, 270, 480, 60)
        self.conversionInputField.setFont(QFont(self.conversionInputField.font().family(), 21))
        self.conversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
        self.conversionInputField.setReadOnly(True)
        # Output Field
        self.conversionOutputField = QLineEdit(self.widget)
        self.conversionOutputField.setGeometry(30, 420, 480, 60)
        self.conversionOutputField.setFont(QFont(self.conversionOutputField.font().family(), 21))
        self.conversionOutputField.setStyleSheet('border: 2px solid; padding-left: 15px')
        self.conversionOutputField.setPlaceholderText('Output')
        self.conversionOutputField.setReadOnly(True)

    def createConversionPasteButton(self):
        self.conversionPasteButton = QPushButton('⇅', self.widget)
        self.conversionPasteButton.setGeometry(510, 210, 60, 270)
        self.conversionPasteButton.setFont(QFont(self.conversionPasteButton.font().family(), 33, QFont.Weight.Bold))
        self.conversionPasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
        self.conversionPasteButton.clicked.connect(self.conversionPaste)

    def createConversionNumberPad(self):
        # Point [.]
        self.conversionPointButton = QPushButton('.', self.widget)
        self.conversionPointButton.setGeometry(300, 780, 90, 90)
        self.conversionPointButton.setFont(QFont(self.conversionPointButton.font().family(), 27, QFont.Weight.Bold))
        self.conversionPointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
        self.conversionPointButton.clicked.connect(self.addConversionPoint)
        # Digits
        self.conversionDigitButtons = {}
        conversionDigitPositions = {
            '7': (120, 510), '8': (210, 510), '9': (300, 510),
            '4': (120, 600), '5': (210, 600), '6': (300, 600),
            '1': (120, 690), '2': (210, 690), '3': (300, 690),
            '00': (120, 780), '0': (210, 780)
        }
        for conversionDigit, conversionDigitPosition in conversionDigitPositions.items():
            conversionDigitButton = QPushButton(conversionDigit, self.widget)
            conversionDigitButton.setGeometry(*conversionDigitPosition, 90, 90)
            conversionDigitButton.setFont(QFont(conversionDigitButton.font().family(), 27, QFont.Weight.Bold))
            conversionDigitButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
            conversionDigitButton.clicked.connect(
                lambda _, conD = conversionDigit: self.addConversionDigit(conD)
            )
            self.conversionDigitButtons[conversionDigit] = conversionDigitButton

    def createConversionControlButtons(self):
        # All Clear
        self.conversionAllClearButton = QPushButton('AC', self.widget)
        self.conversionAllClearButton.setGeometry(390, 510, 90, 90)
        self.conversionAllClearButton.setFont(QFont(self.conversionAllClearButton.font().family(), 27, QFont.Weight.Bold))
        self.conversionAllClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
        self.conversionAllClearButton.clicked.connect(self.conversionAllClear)
        # Clear [Backspace]
        self.conversionClearButton = QPushButton('C', self.widget)
        self.conversionClearButton.setGeometry(390, 600, 90, 90)
        self.conversionClearButton.setFont(QFont(self.conversionClearButton.font().family(), 27, QFont.Weight.Bold))
        self.conversionClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
        self.conversionClearButton.clicked.connect(self.conversionClear)
        # Result [=]
        self.conversionResultButton = QPushButton('=', self.widget)
        self.conversionResultButton.setGeometry(390, 690, 90, 180)
        self.conversionResultButton.setFont(QFont(self.conversionResultButton.font().family(), 33, QFont.Weight.Bold))
        self.conversionResultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
        self.conversionResultButton.clicked.connect(self.conversionResult)

    def back(self):
        self.stackedWidget.setCurrentWidget(self.parentWidget)

    def switchToCalculator(self):
        self.stackedWidget.setCurrentWidget(self.calculatorWidget)

    def addConversionDigit(self, conversionDigit):
        self.conversionInputField.setText(self.conversionInputField.text() + conversionDigit)
        self.conversionInputValue += conversionDigit

    def addConversionPoint(self):
        if self.conversionInputField.text():
            self.conversionInputField.setText(self.conversionInputField.text() + '.')
            self.conversionInputValue += '.'
        else:
            self.conversionInputField.setText(self.conversionInputField.text() + '0.')
            self.conversionInputValue += '0.'

    def conversionPaste(self):
        fromIndex = self.fromComboBox.currentIndex()
        toIndex = self.toComboBox.currentIndex()
        self.fromComboBox.setCurrentIndex(toIndex)
        self.toComboBox.setCurrentIndex(fromIndex)
        if self.conversionInputField.text():
            self.conversionInputField.setText(self.conversionOutputField.text())
            self.conversionInputValue = str(self.conversionOutputField.text())
            self.conversionResult()

    def conversionAllClear(self):
        self.conversionInputField.setText('')
        self.conversionOutputField.setText('')
        self.conversionInputValue = ''

    def conversionClear(self):
        conversionInputFieldText = self.conversionInputField.text()
        conversionInputFieldText = conversionInputFieldText[:-1]
        self.conversionInputField.setText(conversionInputFieldText)
        self.conversionInputValue = self.conversionInputValue[:-1]

    def conversionResult(self):
        if self.conversionInputField.text():
            if self.conversionInputField.text().endswith('.'):
                self.conversionInputField.setText(self.conversionInputField.text().replace('.', ''))
                self.conversionInputValue = self.conversionInputValue.replace('.', '')
            value = float(self.conversionInputValue)
            if self.label == 'Currency':
                fromText = self.fromComboBox.currentText()[:3]
                toText = self.toComboBox.currentText()[:3]
                result = self.convertCurrency(value, fromText, toText)
            elif self.label == 'Temperature':
                fromIndex = self.fromComboBox.currentIndex()
                toIndex = self.toComboBox.currentIndex()
                result = self.convertTemperature(value, fromIndex, toIndex)
            else:
                fromIndex = self.fromComboBox.currentIndex()
                toIndex = self.toComboBox.currentIndex()
                conversionKey = (fromIndex, toIndex)
                factor = self.conversion[conversionKey]
                result = value * factor
            self.conversionOutputField.setText(str(result))

    def convertCurrency(self, value, fromText, toText):
        global API_KEY
        if API_KEY == None:
            apiDialog = APIKeyDialog(self.widget)
            result = apiDialog.exec()
            if result == QDialog.DialogCode.Accepted:
                url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{fromText}/{toText}/{value}'
                try:
                    response = get(url)
                    data = response.json()
                    if "result" in data and data["result"] != "error":
                        saveAPI(API_KEY)
                        return data["conversion_result"]
                    else:
                        error_message = data.get("error-type", "Unknown error")
                        API_KEY = ''
                        errorMessageBox.critical(self.widget, 'Error', f'An error occurred: {error_message}')
                except Exception as e:
                    errorMessageBox.critical(self.widget, 'Error', f'Connection error: {str(e)}')
        else:
            url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{fromText}/{toText}/{value}'
            response = get(url)
            data = response.json()
            return data["conversion_result"]

    def convertTemperature(self, value, fromIndex, toIndex):
        if fromIndex == 0 and toIndex == 0:
            result = value
            return result
        elif fromIndex == 0 and toIndex == 1:
            result = (float(value) * 1.8) + 32
            return result
        elif fromIndex == 0 and toIndex == 2:
            result = float(value) + 273.15
            return result
        elif fromIndex == 0 and toIndex == 3:
            result = (float(value) * 1.8) + 491.67
            return result
        elif fromIndex == 1 and toIndex == 0:
            result = (float(value) - 32) / 1.8
            return result
        elif fromIndex == 1 and toIndex == 1:
            result = value
            return result
        elif fromIndex == 1 and toIndex == 2:
            result = ((float(value) - 32) / 1.8) + 273.15
            return result
        elif fromIndex == 1 and toIndex == 3:
            result = float(value) + 459.67
            return result
        elif fromIndex == 2 and toIndex == 0:
            result = float(value) - 273.15
            return result
        elif fromIndex == 2 and toIndex == 1:
            result = ((float(value) - 273.15) * 1.8) + 32
            return result
        elif fromIndex == 2 and toIndex == 2:
            result = value
            return result
        elif fromIndex == 2 and toIndex == 3:
            result = float(value) * 1.8
            return result
        elif fromIndex == 3 and toIndex == 0:
            result = (float(value) - 491.67) / 1.8
            return result
        elif fromIndex == 3 and toIndex == 1:
            result = float(value) - 459.67
            return result
        elif fromIndex == 3 and toIndex == 2:
            result = float(value) / 1.8
            return result
        else:
            result = value
            return result

# Individual Conversion Pages
currencyConversion = conversionPage('Currency', currencyUnits, currencyConversionFactors)
currencyConversionNoteLabel = createNoteLabel(currencyConversion.widget)

lengthConversion = conversionPage('Length', lengthUnits, lengthConversionFactors)

areaConversion = conversionPage('Area', areaUnits, areaConversionFactors)

volumeConversion = conversionPage('Volume', volumeUnits, volumeConversionFactors)

weightConversion = conversionPage('Weight', weightUnits, weightConversionFactors)

temperatureConversion = conversionPage('Temperature', temperatureUnits, temperatureConversionFactors)

speedConversion = conversionPage('Speed', speedUnits, speedConversionFactors)

pressureConversion = conversionPage('Pressure', pressureUnits, pressureConversionFactors)

powerConversion = conversionPage('Power', powerUnits, powerConversionFactors)

window.show()
CalcWizard.exec()

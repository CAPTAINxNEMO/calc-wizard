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

if getattr(sys, 'frozen', False):
    baseDir = sys._MEIPASS # type: ignore
else:
    baseDir = dirname(abspath(__file__))
iconPath = join(baseDir, 'CalcWizardIcon.ico')

calculatorInput = ''

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

# Font Attributes
# Main Label Font
mainLabelFont = QFont()
mainLabelFont.setPixelSize(52)  # 39
mainLabelFont.setBold(True)
# Conversion Pages Label Font
conversionsLabelFont = QFont()
conversionsLabelFont.setPixelSize(40)
conversionsLabelFont.setBold(True)
# Input Field Font
inputFieldFont = QFont()
inputFieldFont.setPixelSize(28)     # 21
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
numberPadFont.setPixelSize(36)  # 27
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
comboBoxFont.setPixelSize(13)      # 10
comboBoxFont.setBold(True)
comboBoxFont.setItalic(True)

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
# Calculator Widget
calculatorWidget = QWidget()
stackedWidget.addWidget(calculatorWidget)
# Switch to Conversions Button
switchToConversionsButton = QPushButton('⇄', calculatorWidget)
switchToConversionsButton.setFixedSize(60, 60)
switchToConversionsButton.move(510, 30)
switchToConversionsButton.setFont(QFont(switchToConversionsButton.font().family(), 39, QFont.Weight.Bold))
def switchToConversions():
    stackedWidget.setCurrentWidget(conversionsWidget)
switchToConversionsButton.clicked.connect(switchToConversions)
# Calculator Page Main Label
calculatorLabel = QLabel('CALCULATOR', calculatorWidget)
calculatorLabel.setFixedSize(540, 60)
calculatorLabel.move(30, 120)
calculatorLabel.setFont(QFont(calculatorLabel.font().family(), 39, QFont.Weight.Bold))
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
def createCalculatorDigitButtons(calculatorDigitsParent):
    calculatorDigitButtons = {}
    calculatorDigitPositions = {
        '7': (120, 480), '8': (210, 480), '9': (300, 480),
        '4': (120, 570), '5': (210, 570), '6': (300, 570),
        '1': (120, 660), '2': (210, 660), '3': (300, 660),
        '0': (210, 750)
    }

    for calculatorDigit, calculatorDigitPosition in calculatorDigitPositions.items():
        calculatorDigitButton = QPushButton(calculatorDigit, calculatorDigitsParent)
        calculatorDigitButton.setFixedSize(90, 90)
        calculatorDigitButton.move(*calculatorDigitPosition)
        calculatorDigitButton.setFont(QFont(calculatorDigitButton.font().family(), 27, QFont.Weight.Bold))
        calculatorDigitButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
        calculatorDigitButton.clicked.connect(
            lambda calD = calculatorDigit: addCalculatorDigit(calD)
        )
        calculatorDigitButtons[calculatorDigit] = calculatorDigitButton
    return calculatorDigitButtons
def addCalculatorDigit(calculatorDigit):
    global calculatorInput
    calculatorInputField.setText(calculatorInputField.text() + calculatorDigit)
    calculatorInput += calculatorDigit
calculatorDigits = createCalculatorDigitButtons(calculatorWidget)
# Point [.]
calculatorPointButton = QPushButton('.', calculatorWidget)
calculatorPointButton.setFixedSize(90, 90)
calculatorPointButton.move(300, 840)
calculatorPointButton.setFont(QFont(calculatorPointButton.font().family(), 27, QFont.Weight.Bold))
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
# Operators [+ | - | × | ÷ | %]
def createCalculatorOperationButtons(calculatorOperationsParent):
    calculatorOperationButtons = {}
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
        calculatorOperationButton = QPushButton(calculatorOperation, calculatorOperationsParent)
        calculatorOperationButton.setFixedSize(90, 90)
        calculatorOperationButton.move(*calculatorOperationPosition)
        calculatorOperationButton.setFont(QFont(calculatorOperationButton.font().family(), 33, QFont.Weight.Bold))
        calculatorOperationButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')

        calculatorOperationButton.clicked.connect(
            lambda displayOp = calculatorOperation,
            functionOp = calculatorOperationFunctions[calculatorOperation]: addCalculatorOperation(displayOp, functionOp)
        )
        calculatorOperationButtons[calculatorOperation] = calculatorOperationButton
    return calculatorOperationButtons
def addCalculatorOperation(displayOperation, functionOperation):
    global calculatorInput
    if calculatorInputField.text():
        calculatorInputField.setText(calculatorInputField.text() + displayOperation)
        calculatorInput += functionOperation
calculatorOperations = createCalculatorOperationButtons(calculatorWidget)

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
conversionsSwitchToCalculatorButton.setFont(QFont(conversionsSwitchToCalculatorButton.font().family(), 39, QFont.Weight.Bold))
def conversionsSwitchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
conversionsSwitchToCalculatorButton.clicked.connect(conversionsSwitchToCalculator)
# Conversions Page Main Label
conversionsLabel = QLabel('CONVERSIONS', conversionsWidget)
conversionsLabel.setFixedSize(540, 60)
conversionsLabel.move(30, 120)
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
        goToConversionButton.setFixedSize(120, 120)
        goToConversionButton.move(*goToConversionButtonPosition)
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
        goToConversionLabel.setFixedSize(120, 30)
        goToConversionLabel.move(*goToConversionLabelPosition)
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
noteLabel = QLabel('<b>⚠️ NOTE:</b> Currency Conversion requires Internet Connection', conversionsWidget)
noteLabel.setFixedSize(540, 30)
noteLabel.move(30, 900)
noteLabel.setFont(QFont(noteLabel.font().family(), 15))
noteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# # Note for Currency Conversion
# noteLabel = QLabel('<b>⚠️ NOTE:</b> Currency Conversion requires Internet Connection', currencyConversionWidget)
# noteLabel.setFixedSize(540, 30)
# noteLabel.move(30, 900)
# noteLabel.setFont(QFont(noteLabel.font().family(), 15))
# noteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Conversion Pages
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

        self.createHeader()
        self.createComboBoxes()
        self.createConversionTextFields()
        self.createConversionPasteButton()
        self.createConversionNumberPad()
        self.createConversionControlButtons()

    def createHeader(self):
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
        self.pageLabel.setFont(QFont(self.pageLabel.font().family(), 39, QFont.Weight.Bold))
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
            conversionDigitButton.setFixedSize(90, 90)
            conversionDigitButton.move(*conversionDigitPosition)
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
            self.conversionOutputField.setText(result)
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
            self.conversionOutputField.setText(result)
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

# Currency Conversion
currencyUnits = [
    'AED - UAE Dirham (United Arab Emirates)',
    'AFN - Afghan Afghani (Afghanistan)',
    'ALL - Albanian Lek (Albania)',
    'AMD - Armenian Dram (Armenia)',
    'ANG - Netherlands Antillian Guilder (Netherlands Antilles)',
    'AOA - Angolan Kwanza (Angola)',
    'ARS - Argentine Peso (Argentina)',
    'AUD - Australian Dollar (Australia)',
    'AWG - Aruban Florin (Aruba)',
    'AZN - Azerbaijani Manat (Azerbaijan)',
    'BAM - Bosnia and Herzegovina Mark (Bosnia and Herzegovina)',
    'BBD - Barbados Dollar (Barbados)',
    'BDT - Bangladeshi Taka (Bangladesh)',
    'BGN - Bulgarian Lev (Bulgaria)',
    'BHD - Bahraini Dinar (Bahrain)',
    'BIF - Burundian Franc (Burundi)',
    'BMD - Bermudian Dollar (Bermuda)',
    'BND - Brunei Dollar (Brunei)',
    'BOB - Bolivian Boliviano (Bolivia)',
    'BRL - Brazilian Real (Brazil)',
    'BSD - Bahamian Dollar (Bahamas)',
    'BTN - Bhutanese Ngultrum (Bhutan)',
    'BWP - Botswana Pula (Botswana)',
    'BYN - Belarusian Ruble (Belarus)',
    'BZD - Belize Dollar (Belize)',
    'CAD - Canadian Dollar (Canada)',
    'CDF - Congolese Franc (Democratic Republic of the Congo)',
    'CHF - Swiss Franc (Switzerland)',
    'CLP - Chilean Peso (Chile)',
    'CNY - Chinese Renminbi (China)',
    'COP - Colombian Peso (Colombia)',
    'CRC - Costa Rican Colon (Costa Rica)',
    'CUP - Cuban Peso (Cuba)',
    'CVE - Cape Verdean Escudo (Cape Verde)',
    'CZK - Czech Koruna (Czech Republic)',
    'DJF - Djiboutian Franc (Djibouti)',
    'DKK - Danish Krone (Denmark)',
    'DOP - Dominican Peso (Dominican Republic)',
    'DZD - Algerian Dinar (Algeria)',
    'EGP - Egyptian Pound (Egypt)',
    'ERN - Eritrean Nakfa (Eritrea)',
    'ETB - Ethiopian Birr (Ethiopia)',
    'EUR - Euro (European Union)',
    'FJD - Fiji Dollar (Fiji)',
    'FKP - Falkland Islands Pound (Falkland Islands)',
    'FOK - Faroese Króna (Faroe Islands)',
    'GBP - Pound Sterling (United Kingdom)',
    'GEL - Georgian Lari (Georgia)',
    'GGP - Guernsey Pound (Guernsey)',
    'GHS - Ghanaian Cedi (Ghana)',
    'GIP - Gibraltar Pound (Gibraltar)',
    'GMD - Gambian Dalasi The (Gambia)',
    'GNF - Guinean Franc (Guinea)',
    'GTQ - Guatemalan Quetzal (Guatemala)',
    'GYD - Guyanese Dollar (Guyana)',
    'HKD - Hong Kong Dollar (Hong Kong)',
    'HNL - Honduran Lempira (Honduras)',
    'HRK - Croatian Kuna (Croatia)',
    'HTG - Haitian Gourde (Haiti)',
    'HUF - Hungarian Forint (Hungary)',
    'IDR - Indonesian Rupiah (Indonesia)',
    'ILS - Israeli New Shekel (Israel)',
    'IMP - Manx Pound (Isle of Man)',
    'INR - Indian Rupee (India)',
    'IQD - Iraqi Dinar (Iraq)',
    'IRR - Iranian Rial (Iran)',
    'ISK - Icelandic Króna (Iceland)',
    'JEP - Jersey Pound (Jersey)',
    'JMD - Jamaican Dollar (Jamaica)',
    'JOD - Jordanian Dinar (Jordan)',
    'JPY - Japanese Yen (Japan)',
    'KES - Kenyan Shilling (Kenya)',
    'KGS - Kyrgyzstani Som (Kyrgyzstan)',
    'KHR - Cambodian Riel (Cambodia)',
    'KID - Kiribati Dollar (Kiribati)',
    'KMF - Comorian Franc (Comoros)',
    'KRW - South Korean Won (South Korea)',
    'KWD - Kuwaiti Dinar (Kuwait)',
    'KYD - Cayman Islands Dollar (Cayman Islands)',
    'KZT - Kazakhstani Tenge (Kazakhstan)',
    'LAK - Lao Kip (Laos)',
    'LBP - Lebanese Pound (Lebanon)',
    'LKR - Sri Lanka Rupee (Sri Lanka)',
    'LRD - Liberian Dollar (Liberia)',
    'LSL - Lesotho Loti (Lesotho)',
    'LYD - Libyan Dinar (Libya)',
    'MAD - Moroccan Dirham (Morocco)',
    'MDL - Moldovan Leu (Moldova)',
    'MGA - Malagasy Ariary (Madagascar)',
    'MKD - Macedonian Denar (North Macedonia)',
    'MMK - Burmese Kyat (Myanmar)',
    'MNT - Mongolian Tögrög (Mongolia)',
    'MOP - Macanese Pataca (Macau)',
    'MRU - Mauritanian Ouguiya (Mauritania)',
    'MUR - Mauritian Rupee (Mauritius)',
    'MVR - Maldivian Rufiyaa (Maldives)',
    'MWK - Malawian Kwacha (Malawi)',
    'MXN - Mexican Peso (Mexico)',
    'MYR - Malaysian Ringgit (Malaysia)',
    'MZN - Mozambican Metical (Mozambique)',
    'NAD - Namibian Dollar (Namibia)',
    'NGN - Nigerian Naira (Nigeria)',
    'NIO - Nicaraguan Córdoba (Nicaragua)',
    'NOK - Norwegian Krone (Norway)',
    'NPR - Nepalese Rupee (Nepal)',
    'NZD - New Zealand Dollar (New Zealand)',
    'OMR - Omani Rial (Oman)',
    'PAB - Panamanian Balboa (Panama)',
    'PEN - Peruvian Sol (Peru)',
    'PGK - Papua New Guinean Kina (Papua New Guinea)',
    'PHP - Philippine Peso (Philippines)',
    'PKR - Pakistani Rupee (Pakistan)',
    'PLN - Polish Złoty (Poland)',
    'PYG - Paraguayan Guaraní (Paraguay)',
    'QAR - Qatari Riyal (Qatar)',
    'RON - Romanian Leu (Romania)',
    'RSD - Serbian Dinar (Serbia)',
    'RUB - Russian Ruble (Russia)',
    'RWF - Rwandan Franc (Rwanda)',
    'SAR - Saudi Riyal (Saudi Arabia)',
    'SBD - Solomon Islands Dollar (Solomon Islands)',
    'SCR - Seychellois Rupee (Seychelles)',
    'SDG - Sudanese Pound (Sudan)',
    'SEK - Swedish Krona (Sweden)',
    'SGD - Singapore Dollar (Singapore)',
    'SHP - Saint Helena Pound (Saint Helena)',
    'SLE - Sierra Leonean Leone (Sierra Leone)',
    'SOS - Somali Shilling (Somalia)',
    'SRD - Surinamese Dollar (Suriname)',
    'SSP - South Sudanese Pound (South Sudan)',
    'STN - São Tomé and Príncipe Dobra (São Tomé and Príncipe)',
    'SYP - Syrian Pound (Syria)',
    'SZL - Eswatini Lilangeni (Eswatini)',
    'THB - Thai Baht (Thailand)',
    'TJS - Tajikistani Somoni (Tajikistan)',
    'TMT - Turkmenistan Manat (Turkmenistan)',
    'TND - Tunisian Dinar (Tunisia)',
    'TOP - Tongan Paʻanga (Tonga)',
    'TRY - Turkish Lira (Turkey)',
    'TTD - Trinidad and Tobago Dollar (Trinidad and Tobago)',
    'TVD - Tuvaluan Dollar (Tuvalu)',
    'TWD - New Taiwan Dollar (Taiwan)',
    'TZS - Tanzanian Shilling (Tanzania)',
    'UAH - Ukrainian Hryvnia (Ukraine)',
    'UGX - Ugandan Shilling (Uganda)',
    'USD - United States Dollar (United States)',
    'UYU - Uruguayan Peso (Uruguay)',
    'UZS - Uzbekistani So\'m (Uzbekistan)',
    'VES - Venezuelan Bolívar Soberano (Venezuela)',
    'VND - Vietnamese Đồng (Vietnam)',
    'VUV - Vanuatu Vatu (Vanuatu)',
    'WST - Samoan Tālā (Samoa)',
    'XAF - Central African CFA Franc (CEMAC)',
    'XCD - East Caribbean Dollar (Organisation of Eastern Caribbean States)',
    'XDR - Special Drawing Rights (International Monetary Fund)',
    'XOF - West African CFA franc (CFA)',
    'XPF - CFP Franc (Collectivités d\'Outre-Mer)',
    'YER - Yemeni Rial (Yemen)',
    'ZAR - South African Rand (South Africa)',
    'ZMW - Zambian Kwacha (Zambia)',
    'ZWL - Zimbabwean Dollar (Zimbabwe)'
]
currencyConversionFactors = {}
currencyConversion = conversionPage('Currency', currencyUnits, currencyConversionFactors)
# Length Conversion
lengthUnits = [
    'Metre (m)',
    'Millimetre (mm)',
    'Centimetre (cm)',
    'Decimetre (dm)',
    'Kilometre (km)',
    'Micrometre (μm)',
    'Nanometre (nm)',
    'Picometre (pm)',
    'Inch (in)',
    'Foot (ft)',
    'Yard (yd)',
    'Mile (mi)',
    'Nautical Mile (nmi)'
]
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
lengthConversion = conversionPage('Length', lengthUnits, lengthConversionFactors)
# Area Conversion
areaUnits = [
    'Square Metre (m²)',
    'Square Millimetre (mm²)',
    'Square Centimetre (cm²)',
    'Square Decimetre (dm²)',
    'Square Kilometre (km²)',
    'Hectare (ha)',
    'Acre (ac)',
    'Square Micrometre (μm²)',
    'Square Nanometre (nm²)',
    'Square Picometre (pm²)',
    'Are (a)'
]
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
areaConversion = conversionPage('Area', areaUnits, areaConversionFactors)
# Volume Conversion
volumeUnits = [
    'Cubic Metre (m³)',
    'Cubic Centimetre (cm³)',
    'Millilitre (mL)',
    'Litre (L)',
    'Cubic Inch (in³)',
    'Cubic Foot (ft³)',
    'Cubic Yard (yd³)',
    'Gallon (US) (gal)',
    'Gallon (UK) (gal)'
]
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
volumeConversion = conversionPage('Volume', volumeUnits, volumeConversionFactors)
# Weight Conversion
weightUnits = [
    'Gram (g)',
    'Kilogram (kg)',
    'Milligram (mg)',
    'Tonne (t)',
    'Quintal (q)',
    'Carat (ct)',
    'Ounce (oz)',
    'Pound (lb)',
    'Stone (st)'
]
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
weightConversion = conversionPage('Weight', weightUnits, weightConversionFactors)
# Temperature Conversion
temperatureUnits = [
    'Celsius (°C)',
    'Fahrenheit (°F)',
    'Kelvin (K)',
    'Rankine (°Ra)'
]
temperatureConversionFactors = {}
temperatureConversion = conversionPage('Temperature', temperatureUnits, temperatureConversionFactors)
# Speed Conversion
speedUnits = [
    'Metres per second (m/s)',
    'Kilometres per hour (km/h)',
    'Miles per hour (mph)',
    'Mach (Ma)',
    'Speed of Light (c)'
]
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
speedConversion = conversionPage('Speed', speedUnits, speedConversionFactors)
# Pressure Conversion
pressureUnits = [
    'Atmosphere (atm)',
    'Bar (Bar)',
    'Millibar (mBar)',
    'Pounds per square inch (psi)',
    'Pascal (Pa) | Newtons per square metre (N/m²)',
    'Millimetres of H₂O [Water] (mmH₂O)',
    'Millimetres of Hg [Mercury] (mmHg)'
]
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
pressureConversion = conversionPage('Pressure', pressureUnits, pressureConversionFactors)
# Power Conversion
powerUnits = [
    'Watt (W) | Joules per second (J/s) | Newton-metres per second (N∙m/s)',
    'Foot-pounds per second (ft∙lb/s)',
    'Kilocalories per second (kcal/s)',
    'Horsepower (HP)'
]
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
powerConversion = conversionPage('Power', powerUnits, powerConversionFactors)

window.show()
CalcWizard.exec()

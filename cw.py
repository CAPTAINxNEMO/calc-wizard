# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QInputDialog
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
# Icon Check
import sys
from os.path import dirname, abspath, join

if getattr(sys, 'frozen', False):
    baseDir = sys._MEIPASS # type: ignore
else:
    baseDir = dirname(abspath(__file__))
iconPath = join(baseDir, 'CalcWizardIcon.ico')

calculatorInput = ''

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
        calculatorDigitButton.setFont(numberPadFont)
        calculatorDigitButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')

        calculatorDigitButton.clicked.connect(
            lambda checked = False,
            calD = calculatorDigit: addCalculatorDigit(calD)
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
        calculatorOperationButton.setFont(numberPadFont)
        calculatorOperationButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')

        calculatorOperationButton.clicked.connect(
            lambda checked = False, displayOp = calculatorOperation,
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

window.show()
CalcWizard.exec()

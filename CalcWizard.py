# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
# Mathematical Functions
from math import sin, cos, tan, asin, acos, atan, radians, pi, e, log, log2, log10

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

CalcWizard = QApplication([])
# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)

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
comboBoxFont.setItalic(True)

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
            calculatorInput = calculatorInput.replace('asin(', '')
        elif calculatorInputField.text().endswith('cos⁻¹('):
            calculatorInputField.setText(calculatorInputField.text().replace('cos⁻¹(', ''))
            calculatorInput = calculatorInput.replace('acos(', '')
        elif calculatorInputField.text().endswith('tan⁻¹('):
            calculatorInputField.setText(calculatorInputField.text().replace('tan⁻¹(', ''))
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
            calculatorOutputField.setText(str(eval(calculatorInput)))
    except Exception as err:
        errorMessage = str(err)
        errorMessage = errorMessage.replace('(<string>, line 1)', '')
        QMessageBox.critical(calculatorWidget, 'Error', f'An error occurred: {errorMessage}\nScript: {calculatorInput}')
calculatorResultButton.clicked.connect(calculatorResult)

# Conversions Page
# Conversions Widget
conversionsWidget = QWidget()
stackedWidget.addWidget(conversionsWidget)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', conversionsWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
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
backButton = QPushButton('←', currencyConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', currencyConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Currency Conversion Page Main Label
currencyConversionLabel = QLabel('Currency Conversion', currencyConversionWidget)
currencyConversionLabel.setFixedSize(540, 60)
currencyConversionLabel.move(30, 120)
currencyConversionLabel.setFont(conversionsLabelFont)
currencyConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# From Combo Box
currencyConversionFrom = QComboBox(currencyConversionWidget)
currencyConversionFrom.setFixedSize(480, 60)
currencyConversionFrom.move(30, 210)
currencyConversionFrom.setFont(comboBoxFont)
currencyConversionFrom.setStyleSheet('padding-left: 10px')
currencyConversionFrom.addItem('AED - UAE Dirham (United Arab Emirates)')
currencyConversionFrom.addItem('AFN - Afghan Afghani (Afghanistan)')
currencyConversionFrom.addItem('ALL - Albanian Lek (Albania)')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
currencyConversionFrom.addItem('')
# Input Field
currencyConversionInputField = QLineEdit(currencyConversionWidget)
currencyConversionInputField.setPlaceholderText('Input')
currencyConversionInputField.setFixedSize(480, 60)
currencyConversionInputField.move(30, 270)
currencyConversionInputField.setFont(inputFieldFont)
currencyConversionInputField.setStyleSheet('border: 2px solid; padding-left: 15px')
currencyConversionInputField.setReadOnly(True)
# To Combo Box
currencyConversionTo = QComboBox(currencyConversionWidget)
currencyConversionTo.setFixedSize(480, 60)
currencyConversionTo.move(30, 360)
currencyConversionTo.setFont(comboBoxFont)
currencyConversionTo.setStyleSheet('padding-left: 10px')
currencyConversionTo.addItem('AED - UAE Dirham (United Arab Emirates)')
currencyConversionTo.addItem('AFN - Afghan Afghani (Afghanistan)')
currencyConversionTo.addItem('ALL - Albanian Lek (Albania)')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
currencyConversionTo.addItem('')
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
    global currencyConversionInput
    print('Placeholder')
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
    print('Placeholder')
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
backButton = QPushButton('←', lengthConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', lengthConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Length Conversion Page Main Label
lengthConversionLabel = QLabel('Length Conversion', lengthConversionWidget)
lengthConversionLabel.setFixedSize(540, 60)
lengthConversionLabel.move(30, 120)
lengthConversionLabel.setFont(conversionsLabelFont)
lengthConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Area Conversion Page
# Area Conversion Widget
areaConversionWidget = QWidget()
stackedWidget.addWidget(areaConversionWidget)
# Back Button
backButton = QPushButton('←', areaConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', areaConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Area Conversion Page Main Label
areaConversionLabel = QLabel('Area Conversion', areaConversionWidget)
areaConversionLabel.setFixedSize(540, 60)
areaConversionLabel.move(30, 120)
areaConversionLabel.setFont(conversionsLabelFont)
areaConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Volume Conversion Page
# Volume Conversion Widget
volumeConversionWidget = QWidget()
stackedWidget.addWidget(volumeConversionWidget)
# Back Button
backButton = QPushButton('←', volumeConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', volumeConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Volume Conversion Page Main Label
volumeConversionLabel = QLabel('Volume Conversion', volumeConversionWidget)
volumeConversionLabel.setFixedSize(540, 60)
volumeConversionLabel.move(30, 120)
volumeConversionLabel.setFont(conversionsLabelFont)
volumeConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Weight Conversion Page
# Weight Conversion Widget
weightConversionWidget = QWidget()
stackedWidget.addWidget(weightConversionWidget)
# Back Button
backButton = QPushButton('←', weightConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', weightConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Weight Conversion Page Main Label
weightConversionLabel = QLabel('Weight Conversion', weightConversionWidget)
weightConversionLabel.setFixedSize(540, 60)
weightConversionLabel.move(30, 120)
weightConversionLabel.setFont(conversionsLabelFont)
weightConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Temperature Conversion Page
# Temperature Conversion Widget
temperatureConversionWidget = QWidget()
stackedWidget.addWidget(temperatureConversionWidget)
# Back Button
backButton = QPushButton('←', temperatureConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', temperatureConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Temperature Conversion Page Main Label
temperatureConversionLabel = QLabel('Temperature Conversion', temperatureConversionWidget)
temperatureConversionLabel.setFixedSize(540, 60)
temperatureConversionLabel.move(30, 120)
temperatureConversionLabel.setFont(conversionsLabelFont)
temperatureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Speed Conversion Page
# Speed Conversion Widget
speedConversionWidget = QWidget()
stackedWidget.addWidget(speedConversionWidget)
# Back Button
backButton = QPushButton('←', speedConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', speedConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Speed Conversion Page Main Label
speedConversionLabel = QLabel('Speed Conversion', speedConversionWidget)
speedConversionLabel.setFixedSize(540, 60)
speedConversionLabel.move(30, 120)
speedConversionLabel.setFont(conversionsLabelFont)
speedConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Pressure Conversion Page
# Pressure Conversion Widget
pressureConversionWidget = QWidget()
stackedWidget.addWidget(pressureConversionWidget)
# Back Button
backButton = QPushButton('←', pressureConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', pressureConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Pressure Conversion Page Main Label
pressureConversionLabel = QLabel('Pressure Conversion', pressureConversionWidget)
pressureConversionLabel.setFixedSize(540, 60)
pressureConversionLabel.move(30, 120)
pressureConversionLabel.setFont(conversionsLabelFont)
pressureConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Power Conversion Page
# Power Conversion Widget
powerConversionWidget = QWidget()
stackedWidget.addWidget(powerConversionWidget)
# Back Button
backButton = QPushButton('←', powerConversionWidget)
backButton.setFixedSize(60, 60)
backButton.move(30, 30)
backButton.setFont(mainLabelFont)
def back():
    stackedWidget.setCurrentWidget(conversionsWidget)
backButton.clicked.connect(back)
# Switch to Calculator Button
switchToCalculatorButton = QPushButton('⇄', powerConversionWidget)
switchToCalculatorButton.setFixedSize(60, 60)
switchToCalculatorButton.move(510, 30)
switchToCalculatorButton.setFont(mainLabelFont)
def switchToCalculator():
    stackedWidget.setCurrentWidget(calculatorWidget)
switchToCalculatorButton.clicked.connect(switchToCalculator)
# Power Conversion Page Main Label
powerConversionLabel = QLabel('Power Conversion', powerConversionWidget)
powerConversionLabel.setFixedSize(540, 60)
powerConversionLabel.move(30, 120)
powerConversionLabel.setFont(conversionsLabelFont)
powerConversionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

window.show()
CalcWizard.exec()

# https://www.exchangerate-api.com/docs/python-currency-api
'''
AMD - Armenian Dram	Armenia
ANG - Netherlands Antillian Guilder	Netherlands Antilles
AOA - Angolan Kwanza	Angola
ARS - Argentine Peso	Argentina
AUD - Australian Dollar	Australia
AWG - Aruban Florin	Aruba
AZN - Azerbaijani Manat	Azerbaijan
BAM - Bosnia and Herzegovina Mark	Bosnia and Herzegovina
BBD - Barbados Dollar	Barbados
BDT - Bangladeshi Taka	Bangladesh
BGN - Bulgarian Lev	Bulgaria
BHD - Bahraini Dinar	Bahrain
BIF - Burundian Franc	Burundi
BMD - Bermudian Dollar	Bermuda
BND - Brunei Dollar	Brunei
BOB - Bolivian Boliviano	Bolivia
BRL - Brazilian Real	Brazil
BSD - Bahamian Dollar	Bahamas
BTN - Bhutanese Ngultrum	Bhutan
BWP - Botswana Pula	Botswana
BYN - Belarusian Ruble	Belarus
BZD - Belize Dollar	Belize
CAD - Canadian Dollar	Canada
CDF - Congolese Franc	Democratic Republic of the Congo
CHF - Swiss Franc	Switzerland
CLP - Chilean Peso	Chile
CNY - Chinese Renminbi	China
COP - Colombian Peso	Colombia
CRC - Costa Rican Colon	Costa Rica
CUP - Cuban Peso	Cuba
CVE - Cape Verdean Escudo	Cape Verde
CZK - Czech Koruna	Czech Republic
DJF - Djiboutian Franc	Djibouti
DKK - Danish Krone	Denmark
DOP - Dominican Peso	Dominican Republic
DZD - Algerian Dinar	Algeria
EGP - Egyptian Pound	Egypt
ERN - Eritrean Nakfa	Eritrea
ETB - Ethiopian Birr	Ethiopia
EUR - Euro	European Union
FJD - Fiji Dollar	Fiji
FKP - Falkland Islands Pound	Falkland Islands
FOK - Faroese Króna	Faroe Islands
GBP - Pound Sterling	United Kingdom
GEL - Georgian Lari	Georgia
GGP - Guernsey Pound	Guernsey
GHS - Ghanaian Cedi	Ghana
GIP - Gibraltar Pound	Gibraltar
GMD - Gambian Dalasi	The Gambia
GNF - Guinean Franc	Guinea
GTQ - Guatemalan Quetzal	Guatemala
GYD - Guyanese Dollar	Guyana
HKD - Hong Kong Dollar	Hong Kong
HNL - Honduran Lempira	Honduras
HRK - Croatian Kuna	Croatia
HTG - Haitian Gourde	Haiti
HUF - Hungarian Forint	Hungary
IDR - Indonesian Rupiah	Indonesia
ILS - Israeli New Shekel	Israel
IMP - Manx Pound	Isle of Man
INR - Indian Rupee	India
IQD - Iraqi Dinar	Iraq
IRR - Iranian Rial	Iran
ISK - Icelandic Króna	Iceland
JEP - Jersey Pound	Jersey
JMD - Jamaican Dollar	Jamaica
JOD - Jordanian Dinar	Jordan
JPY - Japanese Yen	Japan
KES - Kenyan Shilling	Kenya
KGS - Kyrgyzstani Som	Kyrgyzstan
KHR - Cambodian Riel	Cambodia
KID - Kiribati Dollar	Kiribati
KMF - Comorian Franc	Comoros
KRW - South Korean Won	South Korea
KWD - Kuwaiti Dinar	Kuwait
KYD - Cayman Islands Dollar	Cayman Islands
KZT - Kazakhstani Tenge	Kazakhstan
LAK - Lao Kip	Laos
LBP - Lebanese Pound	Lebanon
LKR - Sri Lanka Rupee	Sri Lanka
LRD - Liberian Dollar	Liberia
LSL - Lesotho Loti	Lesotho
LYD - Libyan Dinar	Libya
MAD - Moroccan Dirham	Morocco
MDL - Moldovan Leu	Moldova
MGA - Malagasy Ariary	Madagascar
MKD - Macedonian Denar	North Macedonia
MMK - Burmese Kyat	Myanmar
MNT - Mongolian Tögrög	Mongolia
MOP - Macanese Pataca	Macau
MRU - Mauritanian Ouguiya	Mauritania
MUR - Mauritian Rupee	Mauritius
MVR - Maldivian Rufiyaa	Maldives
MWK - Malawian Kwacha	Malawi
MXN - Mexican Peso	Mexico
MYR - Malaysian Ringgit	Malaysia
MZN - Mozambican Metical	Mozambique
NAD - Namibian Dollar	Namibia
NGN - Nigerian Naira	Nigeria
NIO - Nicaraguan Córdoba	Nicaragua
NOK - Norwegian Krone	Norway
NPR - Nepalese Rupee	Nepal
NZD - New Zealand Dollar	New Zealand
OMR - Omani Rial	Oman
PAB - Panamanian Balboa	Panama
PEN - Peruvian Sol	Peru
PGK - Papua New Guinean Kina	Papua New Guinea
PHP - Philippine Peso	Philippines
PKR - Pakistani Rupee	Pakistan
PLN - Polish Złoty	Poland
PYG - Paraguayan Guaraní	Paraguay
QAR - Qatari Riyal	Qatar
RON - Romanian Leu	Romania
RSD - Serbian Dinar	Serbia
RUB - Russian Ruble	Russia
RWF - Rwandan Franc	Rwanda
SAR - Saudi Riyal	Saudi Arabia
SBD - Solomon Islands Dollar	Solomon Islands
SCR - Seychellois Rupee	Seychelles
SDG - Sudanese Pound	Sudan
SEK - Swedish Krona	Sweden
SGD - Singapore Dollar	Singapore
SHP - Saint Helena Pound	Saint Helena
SLE - Sierra Leonean Leone	Sierra Leone
SOS - Somali Shilling	Somalia
SRD - Surinamese Dollar	Suriname
SSP - South Sudanese Pound	South Sudan
STN - São Tomé and Príncipe Dobra	São Tomé and Príncipe
SYP - Syrian Pound	Syria
SZL - Eswatini Lilangeni	Eswatini
THB - Thai Baht	Thailand
TJS - Tajikistani Somoni	Tajikistan
TMT - Turkmenistan Manat	Turkmenistan
TND - Tunisian Dinar	Tunisia
TOP - Tongan Paʻanga	Tonga
TRY - Turkish Lira	Turkey
TTD - Trinidad and Tobago Dollar	Trinidad and Tobago
TVD - Tuvaluan Dollar	Tuvalu
TWD - New Taiwan Dollar	Taiwan
TZS - Tanzanian Shilling	Tanzania
UAH - Ukrainian Hryvnia	Ukraine
UGX - Ugandan Shilling	Uganda
USD - United States Dollar	United States
UYU - Uruguayan Peso	Uruguay
UZS - Uzbekistani So\'m	Uzbekistan
VES - Venezuelan Bolívar Soberano	Venezuela
VND - Vietnamese Đồng	Vietnam
VUV - Vanuatu Vatu	Vanuatu
WST - Samoan Tālā	Samoa
XAF - Central African CFA Franc	CEMAC
XCD - East Caribbean Dollar	(Organisation of Eastern Caribbean States)
XDR - Special Drawing Rights	International Monetary Fund
XOF - West African CFA franc	CFA
XPF - CFP Franc	Collectivités d'Outre-Mer
YER - Yemeni Rial	Yemen
ZAR - South African Rand	South Africa
ZMW - Zambian Kwacha	Zambia
ZWL - Zimbabwean Dollar	Zimbabwe
'''
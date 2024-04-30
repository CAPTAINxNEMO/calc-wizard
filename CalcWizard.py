# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from math import sin, cos, tan, asin, acos, atan, radians, pi, e, log, log2, log10

input = ''

CalcWizard = QApplication([])

# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)

# Font Attributes
# Main Label & Switch Button Font
mainLabel_switchButtonFont = QFont()
mainLabel_switchButtonFont.setPixelSize(52)
mainLabel_switchButtonFont.setBold(True)
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

# Switch between Modes Button
switchButton = QPushButton('⇄', window)
switchButton.setFixedSize(60, 60)
switchButton.move(510, 30)
switchButton.setFont(mainLabel_switchButtonFont)
def switchMode():
    print('Placeholder')
switchButton.clicked.connect(switchMode)

# Calculator Page Main Label
calculatorLabel = QLabel('CALCULATOR', window)
calculatorLabel.setFixedSize(540, 60)
calculatorLabel.move(30, 120)
calculatorLabel.setFont(mainLabel_switchButtonFont)
calculatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Input Field
inputField = QLineEdit(window)
inputField.setPlaceholderText('Input')
inputField.setFixedSize(540, 60)
inputField.move(30, 210)
inputField.setFont(inputFieldFont)
inputField.setAlignment(Qt.AlignmentFlag.AlignRight)
inputField.setStyleSheet('border: 2px solid; padding-right: 15px')
inputField.setReadOnly(True)

# Paste Output to Input
pasteButton = QPushButton('↑', window)
pasteButton.setFixedSize(30, 30)
pasteButton.move(540, 270)
pasteButton.setFont(pasteButtonFont)
pasteButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 0)')
def paste():
    if outputField.text():
        global input
        inputField.setText(outputField.text())
        input = str(outputField.text())
        outputField.setText('')
pasteButton.clicked.connect(paste)

# Output Field
outputField = QLineEdit(window)
outputField.setFixedSize(540, 60)
outputField.move(30, 300)
outputField.setFont(outputFieldFont)
outputField.setAlignment(Qt.AlignmentFlag.AlignRight)
outputField.setStyleSheet('border: 2px solid; padding-right: 15px')
outputField.setPlaceholderText('Output')
outputField.setReadOnly(True)

# Calculator Mode Button
calculatorModeButton = QPushButton('∞', window)
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
nineButton = QPushButton('9', window)
nineButton.setFixedSize(90, 90)
nineButton.move(300, 570)
nineButton.setFont(numberPadFont)
nineButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def nine():
    global input
    inputField.setText(inputField.text() + '9')
    input += '9'
nineButton.clicked.connect(nine)
# Eight [8]
eightButton = QPushButton('8', window)
eightButton.setFixedSize(90, 90)
eightButton.move(210, 570)
eightButton.setFont(numberPadFont)
eightButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def eight():
    global input
    inputField.setText(inputField.text() + '8')
    input += '8'
eightButton.clicked.connect(eight)
# Seven [7]
sevenButton = QPushButton('7', window)
sevenButton.setFixedSize(90, 90)
sevenButton.move(120, 570)
sevenButton.setFont(numberPadFont)
sevenButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def seven():
    global input
    inputField.setText(inputField.text() + '7')
    input += '7'
sevenButton.clicked.connect(seven)
# Six [6]
sixButton = QPushButton('6', window)
sixButton.setFixedSize(90, 90)
sixButton.move(300, 660)
sixButton.setFont(numberPadFont)
sixButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def six():
    global input
    inputField.setText(inputField.text() + '6')
    input += '6'
sixButton.clicked.connect(six)
# Five [5]
fiveButton = QPushButton('5', window)
fiveButton.setFixedSize(90, 90)
fiveButton.move(210, 660)
fiveButton.setFont(numberPadFont)
fiveButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def five():
    global input
    inputField.setText(inputField.text() + '5')
    input += '5'
fiveButton.clicked.connect(five)
# Four [4]
fourButton = QPushButton('4', window)
fourButton.setFixedSize(90, 90)
fourButton.move(120, 660)
fourButton.setFont(numberPadFont)
fourButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def four():
    global input
    inputField.setText(inputField.text() + '4')
    input += '4'
fourButton.clicked.connect(four)
# Three [3]
threeButton = QPushButton('3', window)
threeButton.setFixedSize(90, 90)
threeButton.move(300, 750)
threeButton.setFont(numberPadFont)
threeButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def three():
    global input
    inputField.setText(inputField.text() + '3')
    input += '3'
threeButton.clicked.connect(three)
# Two [2]
twoButton = QPushButton('2', window)
twoButton.setFixedSize(90, 90)
twoButton.move(210, 750)
twoButton.setFont(numberPadFont)
twoButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def two():
    global input
    inputField.setText(inputField.text() + '2')
    input += '2'
twoButton.clicked.connect(two)
# One [1]
oneButton = QPushButton('1', window)
oneButton.setFixedSize(90, 90)
oneButton.move(120, 750)
oneButton.setFont(numberPadFont)
oneButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def one():
    global input
    inputField.setText(inputField.text() + '1')
    input += '1'
oneButton.clicked.connect(one)
# Zero [0]
zeroButton = QPushButton('0', window)
zeroButton.setFixedSize(90, 90)
zeroButton.move(210, 840)
zeroButton.setFont(numberPadFont)
zeroButton.setStyleSheet('border: 2px solid; background-color: rgb(185, 195, 205)')
def zero():
    global input
    inputField.setText(inputField.text() + '0')
    input += '0'
zeroButton.clicked.connect(zero)

# Point [.]
pointButton = QPushButton('.', window)
pointButton.setFixedSize(90, 90)
pointButton.move(300, 840)
pointButton.setFont(numberPadFont)
pointButton.setStyleSheet('border: 2px solid; background-color: rgb(177, 156, 217)')
def point():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '.')
        input += '.'
    else:
        inputField.setText(inputField.text() + '0.')
        input += '0.'
pointButton.clicked.connect(point)

# Deletion
# All Clear
allClearButton = QPushButton('AC', window)
allClearButton.setFixedSize(90, 90)
allClearButton.move(390, 480)
allClearButton.setFont(operatorButtonFont)
allClearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def allClear():
    global input
    inputField.setText('')
    outputField.setText('')
    input = ''
allClearButton.clicked.connect(allClear)
# Clear [Backspace]
clearButton = QPushButton('C', window)
clearButton.setFixedSize(90, 90)
clearButton.move(480, 480)
clearButton.setFont(operatorButtonFont)
clearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def clear():
    global input
    if inputField.text():
        if inputField.text().endswith('sin('):
            inputField.setText(inputField.text().replace('sin(', ''))
            input = input.replace('sin(', '')
        elif inputField.text().endswith('cos('):
            inputField.setText(inputField.text().replace('cos(', ''))
            input = input.replace('cos(', '')
        elif inputField.text().endswith('tan('):
            inputField.setText(inputField.text().replace('tan(', ''))
            input = input.replace('tan(', '')
        elif inputField.text().endswith('sin⁻¹('):
            inputField.setText(inputField.text().replace('sin⁻¹(', ''))
            input = input.replace('asin(', '')
        elif inputField.text().endswith('cos⁻¹('):
            inputField.setText(inputField.text().replace('cos⁻¹(', ''))
            input = input.replace('acos(', '')
        elif inputField.text().endswith('tan⁻¹('):
            inputField.setText(inputField.text().replace('tan⁻¹(', ''))
            input = input.replace('atan(', '')
        elif inputField.text().endswith('log⏨('):
            inputField.setText(inputField.text().replace('log⏨(', ''))
            input = input.replace('log10(', '')
        elif inputField.text().endswith('log₂('):
            inputField.setText(inputField.text().replace('log₂(', ''))
            input = input.replace('log2(', '')
        elif inputField.text().endswith('ln('):
            inputField.setText(inputField.text().replace('ln(', ''))
            input = input.replace('log(', '')
        elif inputField.text().endswith('10^'):
            inputField.setText(inputField.text().replace('10^', ''))
            input = input.replace('10**', '')
        elif inputField.text().endswith('2^'):
            inputField.setText(inputField.text().replace('2^', ''))
            input = input.replace('2**', '')
        elif inputField.text().endswith('e^'):
            inputField.setText(inputField.text().replace('e^', ''))
            input = input.replace('e**', '')
        elif inputField.text().endswith('²'):
            inputField.setText(inputField.text().replace('²', ''))
            input = input.replace('**(2)', '')
        elif inputField.text().endswith('^'):
            inputField.setText(inputField.text().replace('^', ''))
            input = input.replace('**', '')
        else:
            inputFieldText = inputField.text()
            inputFieldText = inputFieldText[:-1]
            inputField.setText(inputFieldText)
            input = input[:-1]
clearButton.clicked.connect(clear)

# Operators [+ | - | × | ÷]
# Plus [+]
plusButton = QPushButton('+', window)
plusButton.setFixedSize(90, 90)
plusButton.move(390, 660)
plusButton.setFont(operatorButtonFont)
plusButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def plus():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '+')
        input += '+'
plusButton.clicked.connect(plus)
# Minus [-]
minusButton = QPushButton('-', window)
minusButton.setFixedSize(90, 90)
minusButton.move(480, 660)
minusButton.setFont(operatorButtonFont)
minusButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def minus():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '-')
        input += '-'
minusButton.clicked.connect(minus)
# Multiply [×]
multiplyButton = QPushButton('×', window)
multiplyButton.setFixedSize(90, 90)
multiplyButton.move(390, 750)
multiplyButton.setFont(operatorButtonFont)
multiplyButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def multiply():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '×')
        input += '*'
multiplyButton.clicked.connect(multiply)
# Divide [÷]
divideButton = QPushButton('÷', window)
divideButton.setFixedSize(90, 90)
divideButton.move(480, 750)
divideButton.setFont(operatorButtonFont)
divideButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def divide():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '÷')
        input += '/'
divideButton.clicked.connect(divide)

# Percent [%]
percentButton = QPushButton('%', window)
percentButton.setFixedSize(90, 90)
percentButton.move(30, 570)
percentButton.setFont(operatorButtonFont)
percentButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 255, 0)')
def percent():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '%')
        input += '/100'
percentButton.clicked.connect(percent)

# Brackets
# Open Bracket [(]
openBracketButton = QPushButton('(', window)
openBracketButton.setFixedSize(90, 90)
openBracketButton.move(390, 570)
openBracketButton.setFont(operatorButtonFont)
openBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
openBracketButton.setVisible(False)
def openBracket():
    global input
    inputField.setText(inputField.text() + '(')
    input += '('
openBracketButton.clicked.connect(openBracket)
# Close Bracket [)]
closeBracketButton = QPushButton(')', window)
closeBracketButton.setFixedSize(90, 90)
closeBracketButton.move(480, 570)
closeBracketButton.setFont(operatorButtonFont)
closeBracketButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 255, 191)')
closeBracketButton.setVisible(False)
def closeBracket():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + ')')
        if angleButton.isChecked():
            input += '))'
        else:
            input += ')'
closeBracketButton.clicked.connect(closeBracket)

# Trigonometry
# Sine
sineButton = QPushButton('sin', window)
sineButton.setFixedSize(90, 90)
sineButton.move(120, 390)
sineButton.setFont(trigonometryButtonFont)
sineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
sineButton.setVisible(False)
def sine():
    global input
    inputField.setText(inputField.text() + 'sin(')
    if angleButton.isChecked():
        input += 'sin(radians('
    else:
        input += 'sin('
sineButton.clicked.connect(sine)
# Cosine
cosineButton = QPushButton('cos', window)
cosineButton.setFixedSize(90, 90)
cosineButton.move(210, 390)
cosineButton.setFont(trigonometryButtonFont)
cosineButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
cosineButton.setVisible(False)
def cosine():
    global input
    inputField.setText(inputField.text() + 'cos(')
    if angleButton.isChecked():
        input += 'cos(radians('
    else:
        input += 'cos('
cosineButton.clicked.connect(cosine)
# Tangent
tangentButton = QPushButton('tan', window)
tangentButton.setFixedSize(90, 90)
tangentButton.move(300, 390)
tangentButton.setFont(trigonometryButtonFont)
tangentButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
tangentButton.setVisible(False)
def tangent():
    global input
    inputField.setText(inputField.text() + 'tan(')
    if angleButton.isChecked():
        input += 'tan(radians('
    else:
        input += 'tan('
tangentButton.clicked.connect(tangent)
# Sine Inverse
sineInverseButton = QPushButton('sin⁻¹', window)
sineInverseButton.setFixedSize(90, 90)
sineInverseButton.move(120, 390)
sineInverseButton.setFont(trigonometryButtonFont)
sineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
sineInverseButton.setVisible(False)
def sineInverse():
    global input
    inputField.setText(inputField.text() + 'sin⁻¹(')
    if angleButton.isChecked():
        input += 'asin(radians('
    else:
        input += 'asin('
sineInverseButton.clicked.connect(sineInverse)
# Cosine Inverse
cosineInverseButton = QPushButton('cos⁻¹', window)
cosineInverseButton.setFixedSize(90, 90)
cosineInverseButton.move(210, 390)
cosineInverseButton.setFont(trigonometryButtonFont)
cosineInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
cosineInverseButton.setVisible(False)
def cosineInverse():
    global input
    inputField.setText(inputField.text() + 'cos⁻¹(')
    if angleButton.isChecked():
        input += 'acos(radians('
    else:
        input += 'acos('
cosineInverseButton.clicked.connect(cosineInverse)
# Tangent Inverse
tangentInverseButton = QPushButton('tan⁻¹', window)
tangentInverseButton.setFixedSize(90, 90)
tangentInverseButton.move(300, 390)
tangentInverseButton.setFont(trigonometryButtonFont)
tangentInverseButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 165, 0)')
tangentInverseButton.setVisible(False)
def tangentInverse():
    global input
    inputField.setText(inputField.text() + 'tan⁻¹(')
    if angleButton.isChecked():
        input += 'atan(radians('
    else:
        input += 'atan('
tangentInverseButton.clicked.connect(tangentInverse)
# Angle Button
angleButton = QPushButton('RAD', window)
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
baseTenLogButton = QPushButton('log⏨', window)
baseTenLogButton.setFixedSize(90, 90)
baseTenLogButton.move(120, 480)
baseTenLogButton.setFont(numberPadFont)
baseTenLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
baseTenLogButton.setVisible(False)
def baseTenLog():
    global input
    inputField.setText(inputField.text() + 'log⏨(')
    input += 'log10('
baseTenLogButton.clicked.connect(baseTenLog)
# Base 2 Log
baseTwoLogButton = QPushButton('log₂', window)
baseTwoLogButton.setFixedSize(90, 90)
baseTwoLogButton.move(210, 480)
baseTwoLogButton.setFont(numberPadFont)
baseTwoLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
baseTwoLogButton.setVisible(False)
def baseTwoLog():
    global input
    inputField.setText(inputField.text() + 'log₂(')
    input += 'log2('
baseTwoLogButton.clicked.connect(baseTwoLog)
# Natural Log
naturalLogButton = QPushButton('ln', window)
naturalLogButton.setFixedSize(90, 90)
naturalLogButton.move(300, 480)
naturalLogButton.setFont(numberPadFont)
naturalLogButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
naturalLogButton.setVisible(False)
def naturalLog():
    global input
    inputField.setText(inputField.text() + 'ln(')
    input += 'log('
naturalLogButton.clicked.connect(naturalLog)

# Logarithm Buttons Inverse
# Exponents of 10
powerTenButton = QPushButton('10ˣ', window)
powerTenButton.setFixedSize(90, 90)
powerTenButton.move(120, 480)
powerTenButton.setFont(numberPadFont)
powerTenButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerTenButton.setVisible(False)
def powerTen():
    global input
    inputField.setText(inputField.text() + '10^')
    input += '10**'
powerTenButton.clicked.connect(powerTen)
# Exponent of 2
powerTwoButton = QPushButton('2ˣ', window)
powerTwoButton.setFixedSize(90, 90)
powerTwoButton.move(210, 480)
powerTwoButton.setFont(numberPadFont)
powerTwoButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerTwoButton.setVisible(False)
def powerTwo():
    global input
    inputField.setText(inputField.text() + '2^')
    input += '2**'
powerTwoButton.clicked.connect(powerTwo)
# Exponents of e
powerEulerButton = QPushButton('eˣ', window)
powerEulerButton.setFixedSize(90, 90)
powerEulerButton.move(300, 480)
powerEulerButton.setFont(numberPadFont)
powerEulerButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 192, 203)')
powerEulerButton.setVisible(False)
def powerEuler():
    global input
    inputField.setText(inputField.text() + 'e^')
    input += 'e**'
powerEulerButton.clicked.connect(powerEuler)

# Inverse Button
inverseButton = QPushButton('INV', window)
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
squareButton = QPushButton('x²', window)
squareButton.setFixedSize(90, 90)
squareButton.move(30, 660)
squareButton.setFont(numberPadFont)
squareButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
squareButton.setVisible(False)
def square():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '²')
        input += '**(2)'
squareButton.clicked.connect(square)

# Exponent
exponentButton = QPushButton('^', window)
exponentButton.setFixedSize(90, 90)
exponentButton.move(30, 750)
exponentButton.setFont(numberPadFont)
exponentButton.setStyleSheet('border: 2px solid; background-color: rgb(191, 255, 0)')
exponentButton.setVisible(False)
def exponent():
    global input
    if inputField.text():
        inputField.setText(inputField.text() + '^')
        input += '**'
exponentButton.clicked.connect(exponent)

# Constants [π | e]
# pi [π]
piButton = QPushButton('π', window)
piButton.setFixedSize(90, 90)
piButton.move(30, 840)
piButton.setFont(constantButtonFont)
piButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
piButton.setVisible(False)
def piCharacter():
    global input
    inputField.setText(inputField.text() + 'π')
    input += 'pi'
piButton.clicked.connect(piCharacter)
# Euler's Number [e]
eulerButton = QPushButton('e', window)
eulerButton.setFixedSize(90, 90)
eulerButton.move(120, 840)
eulerButton.setFont(constantButtonFont)
eulerButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 180)')
eulerButton.setVisible(False)
def eulerNumber():
    global input
    inputField.setText(inputField.text() + 'e')
    input += 'e'
eulerButton.clicked.connect(eulerNumber)

# Result [=]
resultButton = QPushButton('=', window)
resultButton.setFixedSize(180, 90)
resultButton.move(390, 840)
resultButton.setFont(resultButtonsFont)
resultButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 0)')
def result():
    global input
    try:
        if inputField.text():
            outputField.setText(str(eval(input)))
    except Exception as err:
        errorMessage = str(err)
        errorMessage = errorMessage.replace('(<string>, line 1)', '')
        QMessageBox.critical(window, 'Error', f'An error occurred: {errorMessage}\nScript: {input}')
    print(input)
resultButton.clicked.connect(result)

window.show()

CalcWizard.exec()
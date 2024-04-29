# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

input = ''

CalcWizard = QApplication([])

# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)

# Font Attributes
# Main Label & Switch Button Font
mainLabel_switchButtonFont = QFont('Aptos')
mainLabel_switchButtonFont.setPixelSize(52)
mainLabel_switchButtonFont.setBold(True)
# Input Field Font
inputFieldFont = QFont('Aptos')
inputFieldFont.setPixelSize(28)
inputFieldFont.setBold(False)
# Output Field Font
outputFieldFont = QFont('Aptos')
outputFieldFont.setPixelSize(28)
outputFieldFont.setBold(True)
# Paste Button Font
pasteButtonFont = QFont('Aptos')
pasteButtonFont.setPixelSize(20)
pasteButtonFont.setBold(True)
# Advanced & Basic Buttons Font
advanced_basicButtonFont = QFont('Aptos')
advanced_basicButtonFont.setPixelSize(48)
advanced_basicButtonFont.setBold(True)
# Number Pad Font
numberPadFont = QFont('Aptos')
numberPadFont.setPixelSize(36)
numberPadFont.setBold(True)
# Result Buttons Font
resultButtonsFont = QFont('Aptos')
resultButtonsFont.setPixelSize(60)
resultButtonsFont.setBold(True)
# Operator Buttons Font
operatorButtonFont = QFont('Aptos')
operatorButtonFont.setPixelSize(44)
operatorButtonFont.setBold(True)

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

# Advanced Mode Button
advancedButton = QPushButton('∞', window)
advancedButton.setFixedSize(90, 90)
advancedButton.move(30, 390)
advancedButton.setFont(advanced_basicButtonFont)
advancedButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 255)')
advancedButton.setVisible(True)
def advancedMode():
    advancedButton.setVisible(False)
    basicButton.setVisible(True)
advancedButton.clicked.connect(advancedMode)

# Basic Mode Button
basicButton = QPushButton('±', window)
basicButton.setFixedSize(90, 90)
basicButton.move(30, 390)
basicButton.setFont(advanced_basicButtonFont)
basicButton.setStyleSheet('border: 2px solid; background-color: rgb(0, 0, 255)')
basicButton.setVisible(False)
def basicMode():
    advancedButton.setVisible(True)
    basicButton.setVisible(False)
basicButton.clicked.connect(basicMode)

# Number Pad
# Nine (9)
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
# Eight (8)
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
# Seven (7)
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
# Six (6)
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
# Five (5)
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
# Four (4)
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
# Three (3)
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
# Two (2)
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
# One (1)
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
# Zero (0)
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

# Point (.)
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
# Clear (Backspace)
clearButton = QPushButton('C', window)
clearButton.setFixedSize(90, 90)
clearButton.move(480, 480)
clearButton.setFont(operatorButtonFont)
clearButton.setStyleSheet('border: 2px solid; background-color: rgb(255, 0, 255)')
def clear():
    global input
    if inputField.text():
        inputFieldText = inputField.text()
        inputFieldText = inputFieldText[:-1]
        inputField.setText(inputFieldText)
        input = input[:-1]
clearButton.clicked.connect(clear)

# Operators (+ | - | × | ÷)
# Plus (+)
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
# Minus (-)
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
# Multiply (×)
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
# Divide (÷)
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

# Percent (%)
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

# Result (=)
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
        QMessageBox.critical(window, 'Error', f'An error occurred: {str(err)}')
resultButton.clicked.connect(result)

window.show()

CalcWizard.exec()
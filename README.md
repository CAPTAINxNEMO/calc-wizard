# ![CalcWizard (Icon)-2](https://github.com/user-attachments/assets/78b0159e-2f0e-47c9-8630-ed299d66be9c) CalcWizard

**CalcWizard** is a powerful, all-in-one calculator and unit conversion tool built using **PyQt6**. It supports:

- Scientific and basic arithmetic calculations
- Conversions for currency, length, area, volume, weight, temperature, speed, pressure, and power
- Clean and user-friendly interface
- API support for real-time currency conversion

---

## 🚀 Features

- Scientific calculator with trigonometric, logarithmic, and exponential functions
- Multiple unit conversion modules with accurate conversion factors
- Dual mode (Basic / Advanced) interface
- Support for radians and degrees in trigonometric operations
- Custom icon and persistent API key storage

---

## 🛠️ Installation

### Requirements

- Python 3.10+
- Packages:

  ```
  pip install PyQt6 qtpy requests
  ```

---

## 🔧 Building Executable

- Run PyInstaller with the following command:

  ```
  pyinstaller --onefile --windowed --icon="CalcWizard (Icon).ico" --add-data="CalcWizard (Icon).ico;." CalcWizard.py
  ```

- Explanation of flags:
  - `onefile`: Bundle everything into a single executable.
  - `windowed`: Build the app without opening a terminal/console window.
  - `icon`: Embed the custom application icon.
  - `add-data`: Includes the icon file in the build and places it in the current directory (.) inside the executable.

- The executable will be found in the `dist/` folder:

  ```
  dist/CalcWizard.exe
  ```

---

## 🌐 Currency API Key Setup
CalcWizard uses ExchangeRate-API for live currency conversion. To use this feature:

1. Get your free API key from [here](https://www.exchangerate-api.com).
2. On first run, enter your key when prompted.
3. The app attempts to save the key to your system environment for future use.
If saving fails, the key must be entered each time.

NOTE: You can set the environment variable manually by creating the variable `CW_CURRENCY_API_KEY` and assigning your API Key as the value. This value can later be edited.

---

## 📄 License
MIT License – feel free to use and modify as needed.

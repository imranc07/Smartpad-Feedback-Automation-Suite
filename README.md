
# 🌟 Smartpad Feedback Automation Suite

Welcome to the **Smartpad Feedback Automation** project!  
This framework is designed to **automate feedback submission testing** for various product types using **Selenium WebDriver**, **PyTest**, and **Excel-based data-driven testing**.

---

## 🚀 Key Highlights

✅ Automates end-to-end feedback flow for Gin and Wine products  
✅ Reads test data dynamically from Excel (`testdata.xlsx`)  
✅ Generates detailed test results using PyTest  
✅ Uses a modular, maintainable folder structure  
✅ Ideal for QA teams validating web-based feedback portals

---

## 🗂️ Folder Structure Overview

```
SMARTPAD FEEDBACK/
│
├── TestData/                 
│   ├── data.py               # Excel data reading logic
│   └── testdata.xlsx         # Actual test data
│
├── TestLocators/
│   └── locators.py           # Central repository of all UI element locators
│
├── TestScripts/
│   ├── GinPotionFeedback.py      # Test script for Gin products
│   └── test_WinePotionFeedback.py# Test script for Wine products
│
├── Utilities/
│   ├── BrowserManager.py     # Manages browser setup and teardown
│   └── excel_functions.py    # Excel read/write utility functions
│
└── README.md                 # Project documentation
```

---

## 🔧 How It Works

🔹 **Note:** This framework currently focuses on **positive feedback testing only**. Negative test scenarios are not included.

1. **Excel-driven Testing**: Test data is loaded from `testdata.xlsx`.
2. **Web Automation**: Selenium drives browser actions based on that data.
3. **Assertions & Logging**: Test validations are written with PyTest and custom logging.
4. **Maintainability**: All locators, data, and helpers are modularized for easy reuse and updates.

---

## 🧪 Run the Tests

Run all tests from the root directory using:

```bash
pytest TestScripts/
```

> 💡 Tip: Use `-v` for verbose output and `--html=report.html` if you have `pytest-html` installed.

---

## 📌 Requirements

- Python 3.8+
- Selenium
- PyTest
- openpyxl
- webdriver-manager

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🙌 Contributing

Found a bug or have an enhancement in mind? Feel free to open an issue or submit a pull request. Let’s improve together!

---

## 📃 License

This project is open for educational and evaluation purposes. Commercial usage must be discussed with the author.

---

Crafted with 💻 and 🧪 for robust web testing!

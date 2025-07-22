"""
This Python class is used to store constant data values required for testing the OrangeHRM webpage.

The class `OrangeHRMData` acts as a central repository for storing:
- URLs used in the tests (e.g., login page, dashboard).
- File path of the Excel file that contains test data for data-driven testing.
- The sheet name or index of the Excel sheet containing the relevant test data.
"""

class SmartpadFeedbackData:

    # URL for the Smartpad Feedback Home Page
    url = "https://smartpad-customer-feedback.vercel.app/"
    
    # Path to the Excel file containing the test data
    excel_file = "D:\\P-S\\Python-Selenium\\VScode\\Interview_task\\Kristalball\\Smartpad Feedback Application DDT\\TestData\\testdata.xlsx"

    # Name or index of the sheet within the Excel file containing test data
    sheet_number_1 = "GinTestLog"
    sheet_number_2 = "WineTestLog"

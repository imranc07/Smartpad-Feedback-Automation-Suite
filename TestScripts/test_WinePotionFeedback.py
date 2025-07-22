# """
# Smartpad Feedback Application DDT
# This script performs data-driven testing for the Smartpad Feedback Application login functionality.
# """

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Importing exception handling classes
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

# Importing WebDriver wait utilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importing locators, test data, and utility functions
# Assuming these are correctly defined in your project
from TestLocators.locators import SmartpadFeedbackLocators
from TestData.data import SmartpadFeedbackData
from Utilities.excel_functions import ExcelFunctions
from Utilities.BrowserManager import BrowserManager

import time


class TestGinPotionFeedback:
    """
    Test class for Smartpad Feedback Application data-driven testing.
    """

    def start(self):
        """Setup WebDriver and WebDriverWait."""
        self.driver = BrowserManager.get_driver(browser="chrome", headless=False)
        self.wait = WebDriverWait(self.driver, 40)

    def _is_element_present(self, xpath):
        """
        Checks whether an element is present on the page.
        """
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def _scroll_until_visible(self, product_xpath):
        """
        Scrolls down step-by-step until the given product_xpath element is visible or page end is reached.
        """
        scroll_attempts = 0
        max_scroll_attempts = 10000  # Limit scroll attempts to prevent infinite loops

        while not self._is_element_present(product_xpath) and scroll_attempts < max_scroll_attempts:
            current_height = self.driver.execute_script("return window.scrollY + window.innerHeight")
            page_height = self.driver.execute_script("return document.body.scrollHeight")

            if current_height >= page_height:
                break  # Reached the end, product not found
            self.driver.execute_script("window.scrollBy(0, 400)")  # Scroll down a bit
            # Add a small explicit wait after scrolling to allow DOM to update
            time.sleep(0.8)
            scroll_attempts += 1


    def _navigate_to_feedback_form(self):
        """
        Helper method to navigate to the feedback form by clicking common initial buttons.
        """
        self.driver.get(SmartpadFeedbackData.url)
        self.driver.maximize_window()

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.get_started_button_locator))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.wine_locator))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.without_login_button_locator))).click()

            # Click age declaration if present
            if self._is_element_present(SmartpadFeedbackLocators.age_declaration_locator):
                self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.age_declaration_locator))).click()

        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            print(f"[ERROR] Navigation to feedback form failed: {e}")
            raise

    def test_submit_feedback(self):
        """
        Executes data-driven feedback submission using Excel data.
        """
        self.start()  # Initialize WebDriver and wait

        try:
            # Load Excel file and initialize utility
            self.excel = ExcelFunctions(SmartpadFeedbackData.excel_file, SmartpadFeedbackData.sheet_number_2)
            total_rows = self.excel.row_count()

            # Iterate through Excel rows
            for row in range(2, total_rows + 1):  # Start from row 2 as row 1 is header
                try:
                    # Navigate to the feedback form for each iteration
                    # This ensures a clean state for each test case
                    self._navigate_to_feedback_form()

                    # Read test data from Excel
                    # Handle both types of apostrophes and strip whitespace
                    potion_name_raw = self.excel.read_data(row, 7)
                    if potion_name_raw:
                        potion_name = potion_name_raw.replace("’", "'").strip()
                    else:
                        potion_name = "" # Handle case where potion_name might be empty

                    name = self.excel.read_data(row, 3)
                    email = self.excel.read_data(row, 4)
                    comment = self.excel.read_data(row, 8)

                    if not potion_name:
                        print(f"Row {row}: Potion name is empty, skipping this row.")
                        self.excel.write_data(row, 9, datetime.today().strftime("%d-%m-%Y"))
                        self.excel.write_data(row, 10, datetime.now().time())
                        self.excel.write_data(row, 11, "Skipped: Empty Potion Name")
                        continue

                    product_xpath = SmartpadFeedbackLocators.potion_locator.format(potion_name)

                    # Scroll until the product is visible
                    self._scroll_until_visible(product_xpath)

                    # Then try to click the product
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, product_xpath))).click()

                    self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.share_feedback_button_locator))).click()
                    self.wait.until(EC.presence_of_element_located((By.XPATH, SmartpadFeedbackLocators.name_locator))).send_keys(name)
                    self.wait.until(EC.presence_of_element_located((By.XPATH, SmartpadFeedbackLocators.email_locator))).send_keys(email)
                    self.driver.find_element(By.XPATH, SmartpadFeedbackLocators.rating_locator).click()
                    self.wait.until(EC.presence_of_element_located((By.XPATH, SmartpadFeedbackLocators.comment_locator))).send_keys(comment)
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, SmartpadFeedbackLocators.submit_button_locator))).click()

                    try:
                        # Success case
                        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, SmartpadFeedbackLocators.success_message), "Thankyou!"))
                        self.excel.write_data(row, 9, datetime.today().strftime("%d-%m-%Y"))
                        self.excel.write_data(row, 10, datetime.now().time().strftime("%H:%M:%S"))
                        self.excel.write_data(row, 11, "Test Pass")

                    except TimeoutException:
                        try:
                            # Failure case (like validation error)
                            self.wait.until(EC.presence_of_element_located((By.XPATH, SmartpadFeedbackLocators.feedback_error)))

                            error_msg = self.driver.find_element(By.XPATH, SmartpadFeedbackLocators.feedback_error).text
                            print(f"Row {row}: Feedback error for '{potion_name}' - {error_msg}")
                            self.excel.write_data(row, 9, datetime.today().strftime("%d-%m-%Y"))
                            self.excel.write_data(row, 10, datetime.now().time().strftime("%H:%M:%S"))
                            self.excel.write_data(row, 11, f"Test Fail: {error_msg}")

                        except TimeoutException:
                            # If neither message is found
                            print(f"Row {row}: No clear result after submission for '{potion_name}'.")
                            self.excel.write_data(row, 9, datetime.today().strftime("%d-%m-%Y"))
                            self.excel.write_data(row, 10, datetime.now().time().strftime("%H:%M:%S"))
                            self.excel.write_data(row, 11, "Unknown Result")

                except (NoSuchElementException, ElementNotVisibleException, TimeoutException, ElementClickInterceptedException) as error:
                    # Handling exceptions during the test case execution for a row
                    print(f"Row {row}: ERROR submitting feedback for '{potion_name}'. Error: {error}")
                    # Log error details in the Excel sheet
                    self.excel.write_data(row, 9, datetime.today().strftime("%d-%m-%Y"))
                    self.excel.write_data(row, 10, datetime.now().time().strftime("%H:%M:%S"))
                    self.excel.write_data(row, 11, f"Error: {type(error).__name__} - {error}")
                    # Optionally, take a screenshot here for better debugging
                    # self.driver.save_screenshot(f"screenshot_row_{row}.png")

        finally:
            # Close the WebDriver
            self.driver.quit()
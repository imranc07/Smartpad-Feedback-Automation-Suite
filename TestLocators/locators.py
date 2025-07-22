"""
This file contains all the locators used for interacting with elements on the Smartpad Feedback Application webpage.
"""

class SmartpadFeedbackLocators:

    # Locators for the Feedback form fields
    get_started_button_locator = "/html/body/div/div[1]/div/div[2]/div[3]/div"
    gin_locator = "//div[contains(text(), 'Gin')]"
    wine_locator = "//div[contains(text(), 'Wine')]"
    without_login_button_locator = '//div[contains(text(),"Continue without an account")]'
    age_declaration_locator = "//button[contains(text(), 'Yes')]"
    # affigem_locator = "//h2[contains(text(), 'Affigem')]"
    share_feedback_button_locator = '//p[contains(text(),"Share Feedback")]'
    name_locator = "//input[@placeholder='Type your name here...']"
    email_locator = "//input[@placeholder='Type your email here...']"
    rating_locator = "/html/body/div/div[2]/div/div[3]/div/div[5]/p"
    comment_locator = "//textarea[@placeholder='Type your comments here...']"
    # potion_locator = "//h2[contains(text(), '{}')]"
    # potion_locator = "//h2[contains(@class,'text-lg font-bold') and contains(text(), '{}')]"

    potion_locator = '//h2[contains(@class,"text-lg font-bold") and text()="{}"]'


    # Locators for the buttons
    submit_button_locator = '//div[@role="button"]'

    # Locators for error messages
    feedback_error = "//div[@role='status']" # Please give a rating, Please enter your name, Please enter your email
    success_message = "//div[text()='Thankyou!']" # Success message after valid submission

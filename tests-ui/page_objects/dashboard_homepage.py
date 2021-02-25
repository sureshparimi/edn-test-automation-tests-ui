from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.locators import Locators

class DashboardHomePage:
    # WELCOME_BACK_TEXT_ON_FRONT_PAGE = (By.XPATH,"//h4[contains(text(),'Welcome back')]")
    # full_name_on_dashboard = (By.XPATH, "//h1[contains(text(),'Suresh Parimi')]") 

    def __init__(self,selenium,locators):
        self.selenium = selenium
        self.locators = locators


    def title(self):
        return self.selenium.title



    # def welcome_back_text_on_dashboard(self):
    #     welcome_back_on_dashboard = self.selenium.find_element(*self.WELCOME_BACK_TEXT_ON_FRONT_PAGE)
    #     return welcome_back_on_dashboard.text   # .get_attribute('value]

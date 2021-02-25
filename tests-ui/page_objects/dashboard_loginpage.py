from assertpy import assert_that
import os
import pytest
from collections import defaultdict
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from page_objects.locators import DashboardHomePageLocators
from page_objects.locators import DashboardLoginPageLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait


class DashboardLoginPage(BasePage):
    def __pfizer_NT_ID(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.Pfizer_NT_ID_INPUT)
    
    def __pfizer_NT_password(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.Password_INPUT)

    def __submit_button(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.SUBMIT_BUTTON)

    def __go_to_homepage(self):
        self._selenium.get(DashboardHomePageLocators.URL)
        self._selenium.maximize_window()
        
    def __load_dashboard_url(self):
        self.__go_to_homepage()
        # self.selenium.implicitly_wait(20)
        self._selenium.get(os.getenv("SSO_URL"))
        # self.selenium.implicitly_wait(20)
        
    def __login_to_dashboard(self):
        self.__load_dashboard_url()
        pfizerID = self.__pfizer_NT_ID()
        pfizerID.send_keys(os.getenv("Pfizer_NT_ID"))
        password = self.__pfizer_NT_password()
        password.send_keys(os.getenv("pfizer_NT_Password"))
        submit = self.__submit_button()
        submit.click()

    def login_to_dashboard(self):
        self.__login_to_dashboard()

    def __go_to_smartsite_integration_ODE(self):
            self._selenium.get(os.getenv("smartsite_integration_ODE"))
            self._selenium.maximize_window()
    
    def go_to_smartsite_integration_ODE(self):
        self.__go_to_smartsite_integration_ODE()
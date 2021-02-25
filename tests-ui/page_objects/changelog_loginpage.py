from assertpy import assert_that
import os
import pytest
from collections import defaultdict
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from page_objects.locators import changelogLocators
from page_objects.base_page import BasePage
from page_objects.locators import DashboardLoginPageLocators
from selenium.webdriver.support.wait import WebDriverWait

    
class ChangeLogLoginPage(BasePage):
    
    def __pfizer_NT_ID(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.Pfizer_NT_ID_INPUT)
    
    def __login_with_credentials_link(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.login_with_credentials_link)
    
    def __pfizer_NT_password(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.Password_INPUT)

    def __submit_button(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.SUBMIT_BUTTON)


    def login_to_changelogs(self,changelog_site):
        self._selenium.get(changelog_site)
        self._selenium.maximize_window()
        login_with_credentials_link = self.__login_with_credentials_link()
        login_with_credentials_link.click()
        self._wait.static_wait(5)
        self._selenium.get(os.getenv("SSO_URL"))
        pfizerID = self.__pfizer_NT_ID()
        pfizerID.send_keys(os.getenv("Pfizer_NT_ID"))
        password = self.__pfizer_NT_password()
        password.send_keys(os.getenv("pfizer_NT_Password"))
        submit = self.__submit_button()
        submit.click()
        # self._selenium.get(changelog_site)

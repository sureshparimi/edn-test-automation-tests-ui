from assertpy import assert_that
import os
import pytest
from collections import defaultdict
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from page_objects.locators import DashBoardWebsitesPageLocators
from page_objects.locators import DashboardHomePageLocators
from page_objects.locators import DashboardLoginPageLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait

class DashboardWebsitePage(BasePage):

    def fullname_on_dashboard(self):
        fullname = self._selenium.find_element(by=By.XPATH, value=DashboardLoginPageLocators.full_name_on_dashboard)
        return fullname.text
    
    def __websites_menu_on_dashboard(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.websites_menu_on_dashboard)
    
    def __offering_type_on_websites_menu(self,offering_type):
        xparth_string_part1 = str("//a[contains(text(),")
        xparth_string_part2 = str(")]")
        complete_xpath = xparth_string_part1 + '"' + offering_type + '"'+ xparth_string_part2
        return self._selenium.find_element(by=By.XPATH, value=complete_xpath)
    
    def __websites_text_on_websites_page(self):
        websites_page_title = self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.websites_text)
        print("This is websites_text value,from pagepbject",websites_page_title.text)
        return websites_page_title

        
    def click_websites_menu_dropdown(self):
        self._wait.static_wait(5)
        self.__websites_menu_on_dashboard().click()


    def get_text_on_websites_page(self):
        websites_header = self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.websites_text)
        return websites_header.text
    
    def __go_to_dashboad_home_page(self):
        return self._selenium.find_element(by=By.XPATH, value="//a[contains(text(),'DASHBOARD')]")
    
    def navigate_to_dashboard(self):
        dashboard_menu = self.__go_to_dashboad_home_page()
        dashboard_menu.click()

    def go_to_website_from_dashboard(self,sitename):
        search_websites_input_field = self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.search_websites_input_field)
        search_websites_input_field.send_keys(sitename)
        self._wait.static_wait(3)
        auto_complete_field_url = self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.auto_complete_field_url_in_search_websites)
        auto_complete_field_name= self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.auto_complete_field_name_in_search_websites)
        if auto_complete_field_name:
            auto_complete_field_name.click()
        else:
            auto_complete_field_url.click()
        self._wait.static_wait(5)
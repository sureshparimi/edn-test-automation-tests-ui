from assertpy import assert_that
import os
import pytest
from collections import defaultdict
import os
import datetime
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from page_objects.locators import changelogLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait

class CreateChangeLogPage(BasePage):
    def __content_in_tool_bar(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.content_in_tool_bar)

    def __add_content_button(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.add_content_button)
        
    def __input_title(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.title_input_field)
        
    def __input_summary(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.summary_input_box)
        
    def __input_body(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.body_section_in_body)
        
    def __input_revision_log_message(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.revision_log_message_input_box)
    
    def __changerecod_link_in_add_content_page(self):
        return self._selenium.find_element(by=By.XPATH, value=changelogLocators.changerecod_link_in_add_content_page)
    
    def __change_record_types_options_in_dropdown(self):
        options_available = Select(self._selenium.find_element(by=By.XPATH, value=changelogLocators.all_options_in_chagerecord_type_dropdown))
        return options_available
    
    def set_event_date(self,event_date):
        self._selenium.send_keys(Keys.TAB)
        date = datetime.datetime.strptime(event_date, "%d %b %Y  %H:%M:%S.%f")
        input_date = date.day
        input_month = date.month
        input_year = date.year
        event_date = self._selenium.find_element(by=By.XPATH, value=changelogLocators.event_date)
        event_date.send_keys(input_date)
        self._selenium.send_keys(Keys.TAB)
        event_date.send_keys(input_month)
        self._selenium.send_keys(Keys.TAB)
        event_date.send_keys(input_year)
        

    def go_to_create_change_record(self):
        self._wait.static_wait(3)
        content_link_in_tool_bar = self.__content_in_tool_bar()
        content_link_in_tool_bar.click()
        self._wait.static_wait(3)
        add_content_button = self.__add_content_button()
        add_content_button.click()
        self._wait.static_wait(3)
        changerecord_link = self.__changerecod_link_in_add_content_page()
        changerecord_link.click()
        self._wait.static_wait(3)
        
    def create_change_record(self,title,change_record_Type,event_date,affects,summary,body,notifications,contacts,save_as,revision_log_message):
        self._wait.static_wait(5)
        title_input_box = self.__input_title()
        summary_input_box =  self.__input_summary()
        # body_input_box =  self.__input_body()
        revision_log_input_box =  self.__input_revision_log_message()
        title_input_box.send_keys(title)
        summary_input_box.send_keys(summary)
        self._selenium.send_keys(Keys.TAB)
        self._selenium.send_keys(body)
        revision_log_input_box.send_keys(revision_log_message)
        options = self.__change_record_types_options_in_dropdown()
        options.select_by_value(change_record_Type)
        self.set_event_date(event_date)
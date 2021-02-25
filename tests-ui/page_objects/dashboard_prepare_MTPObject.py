from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from page_objects.locators import DashBoardWebsitesPageLocators
from page_objects.locators import DashboardHomePageLocators
from page_objects.locators import HamburgerMenuLinksLocators
from page_objects.locators import PrepareMTPpageLocators
from page_objects.locators import MTPDetailsLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait

class DashboardPrepareMTPPage(BasePage):
    def __mtp_options_in_dropdown(self):
        options_available = Select(self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.all_options_in_mtp_type_dropdown))
        return options_available
    
    def __is_error_message_displayed_on_submitting_prepare_mtp_form(self):
        error_message = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.error_message_on_prepare_mtp_form)
        return error_message
    
    def set_mtp_date_in_prepare_mtp_form(self,mtp_date):
        mtp_date_input = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_date_widget)
        mtp_date_input.send_keys(mtp_date)
        
    def set_mtp_date_time_zone(self,mtp_date_time_zone):
        mtp_date_time_zone_dropdown = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_date_time_zone)
        mtp_date_time_zone_dropdown.click()
        mtp_date_time_zone_chosen_search_box = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_date_time_zone_chosen_search_input)
        mtp_date_time_zone_chosen_search_box.send_keys(mtp_date_time_zone)
        mtp_date_time_zone_chosen_result = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_date_time_zone_chosen_result)
        mtp_date_time_zone_chosen_result.click()
    
    def set_service_request(self,service_request):
        mtp_service_reqeust = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_service_reqeust)
        mtp_service_reqeust.send_keys(service_request)
        
    def set_SCO(self,SCO):
        mtp_SCO = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_solution_center_owner)
        mtp_SCO.send_keys(SCO)
    
    def set_vendor_assignee(self,vendor_assignee):
        mtp_vendor_assignee = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_vendor_assignee_field)
        mtp_vendor_assignee.send_keys(vendor_assignee)
    
    def set_manual_verification_text(self,manual_verification_text):
        mtp_manual_verification_field = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_manual_verification_input_field)
        mtp_manual_verification_field.send_keys(manual_verification_text)
    
    def click_submit_button(self):
        submit_button = self._selenium.find_element(by=By.XPATH, value=PrepareMTPpageLocators.mtp_submit_button)
        submit_button.click()

    def fill_mtp_form(self,mtp_type,mtp_date,mtp_date_time_zone,service_request,SCO,vendor_assignee,manual_verification_text):
            options = self.__mtp_options_in_dropdown()
            options.select_by_value(mtp_type)
            self.set_mtp_date_in_prepare_mtp_form(mtp_date)
            self.set_mtp_date_time_zone(mtp_date_time_zone)
            self.set_service_request(service_request)
            self.set_SCO(SCO)
            self.set_vendor_assignee(vendor_assignee)
            self.set_manual_verification_text(manual_verification_text)
            self.click_submit_button()
            self._wait.static_wait(5)
            
            

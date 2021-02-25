##############################################
# Page reference in Application: https://smartsite-integration.pfizersite.io/mtps 
##############################################

from assertpy import assert_that
import pandas as pd
import requests
import json
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from page_objects.locators import DashBoardWebsitesPageLocators
from page_objects.locators import DashboardHomePageLocators
from page_objects.locators import HamburgerMenuLinksLocators
from page_objects.locators import PrepareMTPpageLocators
from page_objects.locators import MTPDetailsLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait

class DashboardMTPsPage(BasePage):
    
    # list_of_mtps_created_with_preparation_status = []
    mtps_dictionary = dict()
    def __click_on_tools_menu(self):
        tools_menu_on_dashboard =self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.Tools_menu_on_dashboard)
        return tools_menu_on_dashboard
    
    def __mtps_in_tools_menu(self):
        mtps_link_in_tools_menu =self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.mtp_link_in_the_tools_menu)
        return mtps_link_in_tools_menu

    def __sitename_in_mtps_page(self):
         return self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.sitename_in_mtp_page)

    def __filter_button_in_mtps_page(self):
        return self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.filter_button_in_mtp_page)

    def __hamburger_menu_in_mtps_page(self):
        hamburger_menu  = self._selenium.find_element(by=By.XPATH, value=HamburgerMenuLinksLocators.hamburger_icon)
        return hamburger_menu

    def __cancel_mtp_link_in_hamburger_menu(self):
        cancel_mtp_link = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.cancel_mtp_link_hamburger_menu)
        return  cancel_mtp_link
    
    def __delete_mtp_link_in_hamburger_menu(self):
        delete_mtp_link = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.delete_mtp_link_hamburger_menu)
        return  delete_mtp_link

    def __confirm_cancel_mtp_button(self):
        confirm_cancel_button = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.confirm_cancel_button)
        return confirm_cancel_button

    def __confirm_delet_mtp_button(self):
        confirm_delete_button = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.confirm_cancel_button)
        return confirm_delete_button

    def __jira_username(self):
        jira_user_name = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.jira_user_name)
        return jira_user_name
    
    def reload_page(self):
        self._selenium.refresh()
        self._wait.static_wait(3)

    def __jira_password(self):
        return self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.jira_password)
    
    def __jira_login_submit_button(self):
        return  self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.jira_login_submit_button)

    def get_element_by_locator(self,locator):
        return self._selenium.find_element(by=By.XPATH, value=locator)

    def verify_dns_cutover_checkbox(self):
        return self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.verify_dns_request_cutover_checkbox_unchecked)

    def go_to_mtps_page(self):
        self._wait.static_wait(5)
        tools_menu = self.__click_on_tools_menu()
        tools_menu.click()
        self._wait.static_wait(5)
        MTPs_link_in_tools_menu = self.__mtps_in_tools_menu()
        MTPs_link_in_tools_menu.click()

    def filter_mtps_by_sitename(self,sitename):
        sitename_input_field  = self.__sitename_in_mtps_page()
        sitename_input_field.send_keys(sitename)
        filter_button = self.__filter_button_in_mtps_page()
        filter_button.click()

    def perform_mtp_button_ready_for_deployment_state(self): 
        perform_MTP_button = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.perform_MTP_button_in_ready_for_deployment_state)
        return perform_MTP_button
    
    def trigger_build_button_in_ready_for_deployment_state(self): 
        trigger_build_button = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.trigger_build_button_on_popup)
        return trigger_build_button
    
    def fetch_all_existing_mtps_of_a_site(self,base_url):
        mtp_links = []
        page = self._selenium.page_source
        soup = BeautifulSoup(page, 'html.parser')
        rows = soup.select('table > tbody > tr')
        # table_headers = soup.select('table > thead > tr > th')
        for row in rows[0:]:  # omit header row
            cols = row.find_all('td')
            fields = [td.text.strip() for td in cols if td.text.strip()]
            # print(fields)
            if fields:  # if the row is not empty
                link = row.find('a')['href']
                mtp_links.append(base_url+link)
        return mtp_links

    def cancel_all_mtps(self,all_mtps):
        for each_mtp in all_mtps:
            # print(all_mtps)
            self._selenium.get(each_mtp)
            self._wait.static_wait(5)
            hamburger_menu = self.__hamburger_menu_in_mtps_page()
            hamburger_menu.click()
            self._wait.static_wait(2)
            try:
                cancel_mtp_link = self.__cancel_mtp_link_in_hamburger_menu()
                if cancel_mtp_link.is_displayed() and cancel_mtp_link.is_enabled():
                    cancel_mtp_link.click()
                    self._wait.static_wait(5)
                    confirm_cancel_button = self.__confirm_cancel_mtp_button()
                    confirm_cancel_button.click()
                    self._wait.static_wait(5)
            except:
                print("No cancel MTP link present for mtp",each_mtp)
    
    def delete_mtps(self,all_mtps):
        for each_mtp in all_mtps:
            # print(all_mtps)
            self._selenium.get(each_mtp)
            self._wait.static_wait(5)
            hamburger_menu = self.__hamburger_menu_in_mtps_page()
            hamburger_menu.click()
            self._wait.static_wait(2)
            try:
                delete_mtp_link = self.__delete_mtp_link_in_hamburger_menu()
                if delete_mtp_link.is_displayed() and delete_mtp_link.is_enabled():
                    delete_mtp_link.click()
                    self._wait.static_wait(5)
                    confirm_delete_button = self.__confirm_delet_mtp_button()
                    confirm_delete_button.click()
                    self._wait.static_wait(5)
            except:
                print("No Delete link present for mtp",each_mtp)
    
    def get_current_active_MTP_state(self):
        current_active_mtp_state = self._selenium.find_element(by=By.XPATH, value=MTPDetailsLocators.current_active_mtp_state)
        return current_active_mtp_state
    
    def login_to_jira(self):
        # self._selenium.delete_all_cookies()
        # self._selenium.get('https://aed-dev.atlassian.net/')
        pfizerID = self.__jira_username()
        submit = self.__jira_login_submit_button()
        password = self.__jira_password()
        pfizerID.send_keys(os.getenv("pfizer_email_address"))
        submit.click()
        self._wait.static_wait(5)
        password.send_keys(os.getenv("jira_passowrd"))
        submit.click()
        self._wait.static_wait(5)


    def get_sdlc_ticket_link(self):
        sdlc_ticket_link = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.mtp_sdlc_ticket_link)
        return sdlc_ticket_link
    # .get_attribute("href")
    
    def sdlc_jira_ticket_status(self,locatorvalue):
        current_sdlc_ticket_status = self._selenium.find_element(by=By.XPATH,value=locatorvalue)
        return current_sdlc_ticket_status
    
    def sdlc_jira_draft_status(self):
        sdlc_draft_status = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICKET_INITIAL_STATUS)
        return sdlc_draft_status
    
    def sdlc_jira_submit_Delverables_status(self):
        sdlc_jira_submit_Delverables_status = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICEKT_Submit_delivarables_Current_Status)
        return sdlc_jira_submit_Delverables_status
    
    def sdlc_jira_prelimenary_check_passed_status(self):
        sdlc_jira_prelimenary_check_passed_status = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICKET_select_Prelimanary_check_Passed_status)
        return sdlc_jira_prelimenary_check_passed_status
    
    
    def JIRA_SDLC_TICKET_select_SCO_APPROVED_status(self):
        JIRA_SDLC_TICKET_select_SCO_APPROVED_status = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICKET_select_SCO_APPROVED_status)
        return JIRA_SDLC_TICKET_select_SCO_APPROVED_status
    
    def JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status(self):
        JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status)
        return JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status
    
    def support_check_passed_in_popup(self):
        support_check_passed_in_popup = self._selenium.find_element(by=By.XPATH,value=MTPDetailsLocators.JIRA_SDLC_TICKET_POP_UP_SUPPORT_CHECK_PASSED_BUTTON)
        return support_check_passed_in_popup
        
    def write_mtps_to_dashboard_mtp_test_dataJson(self,sitename):
        filename = "/Users/sparimi/Desktop/edison_test_automation_suite/tests-ui/test_data/dashboard_mtp_test_data.json"
        current_mtp_url = self._selenium.current_url
        # DashboardMTPsPage.list_of_mtps_created_with_preparation_status.append(current_mtp_url)
        # print("This is the current URL of the mtp",DashboardMTPsPage.list_of_mtps_created_with_preparation_status)
        if sitename in DashboardMTPsPage.mtps_dictionary:
            DashboardMTPsPage.mtps_dictionary[sitename].append(current_mtp_url)
        else:
            DashboardMTPsPage.mtps_dictionary[sitename] = [current_mtp_url]
        with open(filename,'r') as jsonfile:
            existing_data = json.load(jsonfile)
            existing_data['MTPs_in_preparation_state'].update(DashboardMTPsPage.mtps_dictionary)
            jsonfile.close()
        with open(filename,'w') as jsonfile:
            json.dump(existing_data,jsonfile,indent=4)
            jsonfile.close()
    
    def action_steps_on_SDLC_JIRA_ticket(self,selenium,base_url):
        MTPPage = DashboardMTPsPage(selenium, base_url)
        self._wait.static_wait(5)
        sdlc_jira_ticket_current_status = MTPPage.sdlc_jira_ticket_status(MTPDetailsLocators.JIRA_SDLC_TICKET_INITIAL_STATUS)
        if "In Draft" == sdlc_jira_ticket_current_status.text:
            draft_status = MTPPage.sdlc_jira_draft_status()
            draft_status.click()
            self._wait.static_wait(3)
            select_submit_delivarables_status = MTPPage.sdlc_jira_submit_Delverables_status()
            select_submit_delivarables_status.click()
            self._wait.static_wait(3)
            sdlc_jira_ticket_current_status = MTPPage.sdlc_jira_ticket_status(MTPDetailsLocators.JIRA_SDLC_TICEKT_Submit_delivarables_Current_Status)
            sdlc_jira_ticket_current_status.click()
            self._wait.static_wait(3)
            select_prelimenary_check_passed_status = MTPPage.sdlc_jira_prelimenary_check_passed_status()
            select_prelimenary_check_passed_status.click()
            self._wait.static_wait(3)
            sdlc_jira_ticket_current_status = MTPPage.sdlc_jira_ticket_status(MTPDetailsLocators.JIRA_SDLC_TICKET_select_Prelimanary_check_Passed_status)
            sdlc_jira_ticket_current_status.click()
            JIRA_SDLC_TICKET_select_SCO_APPROVED_status = MTPPage.JIRA_SDLC_TICKET_select_SCO_APPROVED_status()
            JIRA_SDLC_TICKET_select_SCO_APPROVED_status.click()
            self._wait.static_wait(3)
            sdlc_jira_ticket_current_status = MTPPage.sdlc_jira_ticket_status(MTPDetailsLocators.JIRA_SDLC_TICEKT_SCO_APPROVED_Current_Status)
            sdlc_jira_ticket_current_status.click()
            JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status = MTPPage.JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status()
            JIRA_SDLC_TICKET_select_READY_FOR_DEPLOYMENT_status.click()
            self._wait.static_wait(5)
            # ready for deployment status popup box
            support_check_button_popup = MTPPage.support_check_passed_in_popup()
            support_check_button_popup.click()
            self._wait.static_wait(3)
        else:
            print("The JIRA ticket's initial state is not Draft")
    
    def act_on_SDLC_ticket_in_mtp(self,selenium,base_url,site):
        MTPPage = DashboardMTPsPage(selenium, base_url)
        # Get the available MTPs by site from dashboard_mtp_test_data.json
        filename = "../tests-ui/test_data/dashboard_mtp_test_data.json"
        with open(filename,'r') as jsonfile:
                existing_data = json.load(jsonfile)
                MTPs_available_by_site = existing_data['MTPs_in_preparation_state'][site]
                jsonfile.close()
                print("These are the MTPs available from test data file",MTPs_available_by_site)
                for each_mtp in MTPs_available_by_site:
                    selenium.get(each_mtp)
                    current_active_state = MTPPage.get_current_active_MTP_state().text
                    StringList = current_active_state.split('\n')
                    if StringList[1] == "PREPARATION":
                        erify_dns_cutover_checkbox = MTPPage.verify_dns_cutover_checkbox()
                        sdlc_ticket_link = MTPPage.get_sdlc_ticket_link()
                        sdlc_ticket_link.click()
                        selenium.switch_to.window(selenium.window_handles[-1])
                        self._wait.static_wait(5)
                        try:
                            login_submit_button = self.__jira_login_submit_button()
                            # if login_submit_button:
                            MTPPage.login_to_jira()
                            self._wait.static_wait(5)
                            MTPPage.action_steps_on_SDLC_JIRA_ticket(selenium,base_url)
                            selenium.switch_to.window(selenium.window_handles[0])

                        except:
                                MTPPage.action_steps_on_SDLC_JIRA_ticket(selenium,base_url)
                                selenium.switch_to.window(selenium.window_handles[0])
                    else:
                        print("MTP is not in preparation status")

    def act_on_verify_DNS_and_request_cutover_section(self,selenium,base_url,site):
        MTPPage = DashboardMTPsPage(selenium, base_url)
        filename = "../tests-ui/test_data/dashboard_mtp_test_data.json"
        with open(filename,'r') as jsonfile:
                existing_data = json.load(jsonfile)
                MTPs_available_by_site = existing_data['MTPs_in_preparation_state'][site]
                jsonfile.close()
                for each_mtp in MTPs_available_by_site:
                    selenium.get(each_mtp)
                    self._wait.static_wait(5)
                    current_active_state = MTPPage.get_current_active_MTP_state().text
                    StringList = current_active_state.split('\n')
                    if StringList[1] == "PREPARATION":
                        verify_dns_cutover_checkbox = MTPPage.verify_dns_cutover_checkbox()
                        if verify_dns_cutover_checkbox.get_attribute('checked') :
                            print(f'"DNS check box is already checked for the mtp: {each_mtp}"')
                            self._wait.static_wait(5)
                            
                        else:
                            self._wait.static_wait(5)
                            verify_dns_cutover_checkbox.click()
                    else:
                        print(f'"the mtp:{each_mtp} is not in preparation state"')
    
    def perform_mtp_actions_in_ready_for_deployment_state(self,selenium,base_url,site):
        MTPPage = DashboardMTPsPage(selenium, base_url)
        filename = "../tests-ui/test_data/dashboard_mtp_test_data.json"
        with open(filename,'r') as jsonfile:
                existing_data = json.load(jsonfile)
                MTPs_available_by_site = existing_data['MTPs_in_preparation_state'][site]
                jsonfile.close()
                for each_mtp in MTPs_available_by_site:
                    selenium.get(each_mtp)
                    self._wait.static_wait(5)
                    current_active_state = MTPPage.get_current_active_MTP_state().text
                    StringList = current_active_state.split('\n')
                    if StringList[1] == "READY FOR DEPLOYMENT":
                        perform_MTP_button = MTPPage.perform_mtp_button_ready_for_deployment_state()
                        if perform_MTP_button.is_displayed():
                            print("The mtp is in Ready for deployment state")
                            perform_MTP_button.click()
                            self._wait.static_wait(3)
                            trigger_build_button = MTPPage.trigger_build_button_in_ready_for_deployment_state()
                            trigger_build_button.click()
                            self._wait.static_wait(3)
                            MTPPage.reload_page()
                        else:
                            print("The PERFORM MTP button is not available, can not advance mtp to Deployment in progress state")
# Standard library imports
import os
import json
import re
# Third party imports
import pandas as pd
from datetime import datetime, date
from datetime import timedelta
import requests
import pytest
from bs4 import BeautifulSoup
from pytest_bdd import scenarios, given, when, parsers
from pytest_selenium_enhancer import CustomWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


# Application imports
from utils.locators import Locators
from page_objects.dashboard_loginpage import DashboardLoginPage
from page_objects.dashboard_homepage import DashboardHomePage
from page_objects.dashboard_homeObject import DashboardWebsitePage
from page_objects.dashboard_websitepageObject import DashboardWebsitesPage
from page_objects.dashboard_prepare_MTPObject import DashboardPrepareMTPPage
from page_objects.dashboard_mtps_pageObject import DashboardMTPsPage
from page_objects.create_changelogpage import CreateChangeLogPage


@when(parsers.re("I set the locale for locators to '(?P<locale>.*)'"))
@when(parsers.re("I set the language for locators to '(?P<locale>.*)'"))

def set_locale(locators: Locators, locale):
    locators.set_locale(locale)


@when(parsers.re("I click on '(?P<locator_path>.*)'"))
def click_element(selenium, locators: Locators, locator_path):
    selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)).click()


@when(parsers.re("I double click on '(?P<locator_path>.*)'"))
@when(parsers.re("I doubleclick on '(?P<locator_path>.*)'"))
def dbl_click_element(selenium, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    ActionChains(selenium).double_click(element).perform()


@when(parsers.re("I programmatic click on '(?P<locator_path>.*)'"))
def js_click_element(selenium, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    selenium.execute_script('arguments[0].click();', element)


@when(parsers.re("I add text '(?P<text>.*)' to field '(?P<locator_path>.*)'"))
def add_element_value(selenium, text, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    actual_text = element.get_attribute('value')
    element.send_keys(actual_text + text)


@when(parsers.re("I set text '(?P<text>.*)' to field '(?P<locator_path>.*)'"))
def set_element_value(selenium, text, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    element.send_keys(text)


@when(parsers.re("I clear text from field '(?P<locator_path>.*)'"))
def set_add_element_value(selenium, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    element.clear()


@when(parsers.re("I drag and drop element '(?P<source>.*)' to element '(?P<target>.*)'"))
def drag_and_drop_element(selenium, locators: Locators, source, target):
    source_elem = selenium.find_element(By.XPATH, locators.parse_and_get(source))
    target_elem = selenium.find_element(By.XPATH, locators.parse_and_get(target))

    action = ActionChains(selenium)
    action.drag_and_drop(source_elem, target_elem).perform()


@when(parsers.re("I pause for '(?P<time>.*)' s"))
def pause_execution(selenium, time):
    CustomWait(selenium).static_wait(int(time))


@when(parsers.re("I set the cookie '(?P<name>.*)' with value '(?P<value>.*)' for path (?P<path>.*)"))
def check_cookie_content(selenium, name, value, path='/'):
    selenium.add_cookie({"name": name, "value": value, "path": path})


@when(parsers.re("I delete the cookie '(?P<name>.*)'"))
def check_cookie_content(selenium, name):
    selenium.delete_cookie(name)


@when(parsers.re("I press '(?P<key>.*)'"))
def press_button(selenium, key):
    ActionChains(selenium).send_keys(key).perform()


@when(parsers.re("I accept popup prompt"))
@when(parsers.re("I accept popup alertbox"))
@when(parsers.re("I accept popup confirmbox"))
def accept_modal(selenium):
    selenium.switch_to().alert().accept()


@when(parsers.re("I dismiss popup prompt"))
@when(parsers.re("I dismiss popup alertbox"))
@when(parsers.re("I dismiss popup confirmbox"))
def dismiss_modal(selenium):
    selenium.switch_to().alert().dismiss()


@when(parsers.re("I enter (?P<text>.*) into popup alertbox"))
@when(parsers.re("I enter (?P<text>.*) into popup confirmbox"))
@when(parsers.re("I enter (?P<text>.*) into popup prompt"))
def check_modal(selenium, text):
    selenium.switch_to().alert().send_keys(text)


@when(parsers.re("I scroll to element '(?P<locator_path>.*)'"))
def scroll_to_element(selenium, locators: Locators, locator_path):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    script = 'arguments[0].scrollIntoView({block: "center", inline: "center"})'
    selenium.execute_script(script, element)


@when(parsers.re("I close the last opened window"))
@when(parsers.re("I close the last opened tab"))
def close_last_opened_window(selenium):
    windows = selenium.window_handles
    selenium.switch_to_window(windows[-1])
    selenium.close()


@when(parsers.re("I focus the last opened window"))
@when(parsers.re("I focus the last opened tab"))
def switch_to_last(selenium):
    windows = selenium.window_handles
    selenium.switch_to_window(windows[-1])


@when(parsers.re("I select the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
      converters=dict(index=int))
def select_option_by_index(selenium, index: int, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.select_by_index(index)


@when(parsers.re("I select the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"))
def select_option_by_value(selenium, option, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.select_by_value(option)


@when(parsers.re("I select the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"))
def select_option_by_visible_text(selenium, option, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.select_by_visible_text(option)


@when(parsers.re("I deselect the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
      converters=dict(index=int))
def deselect_option_index(selenium, index: int, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.deselect_by_index(index)


@when(parsers.re("I deselect the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"))
def deselect_option_by_value(selenium, option, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.deselect_by_value(option)


@when(parsers.re("I deselect the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"))
def deselect_option_by_visible_text(selenium, option, locators: Locators, locator_path):
    select = Select(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)))
    select.deselect_by_visible_text(option)


@when(parsers.re("I move to element '(?P<locator_path>.*)' with offset '(?P<x>.*)' '(?P<y>.*)'"))
def move_to_element_by_offset(selenium, locators: Locators, locator_path, x, y):
    element = selenium.find_element(By.XPATH, locators.parse_and_get(locator_path))
    ActionChains(selenium).move_to_element_with_offset(element, int(x), int(y))

@when("the user submits valid <username> and <password>")
# @when(parsers.re("the user submits valid '(?P<username>.*)' and '(?P<password>.*)'"))
def dashboard_login(selenium,username,password):
    login_page = DashboardLoginPage()
    login_page.login_to_dashboard(username,password)

@when("the user clicks on websites menu")
def click_websites_menu(selenium,base_url):
    homepage = DashboardWebsitePage(selenium,base_url)
    homepage.click_websites_menu_dropdown()
    

@when('the user clicks on <offering_type>')
def go_to_websites_page(selenium,base_url,offering_type):
    homepage = DashboardWebsitesPage(selenium,base_url)
    if offering_type in ["Edison Custom","Edison Lite","Edison Legacy"]:
        homepage.click_offering_type_in_websites_menu(offering_type)
    else:
        print("Offering type entered is not valid")
        
@when('the user enters <sitename_value> into sitename field')
def filter_websites(selenium,base_url,sitename_value):
    set_filter_options = DashboardWebsitesPage(selenium,base_url)
    set_filter_options.input_sitename_search_filters(sitename_value)
    
@when('the user clicks the Filter button')
def click_filter_button_on_websites_page(selenium,base_url):
    fliter_button = DashboardWebsitesPage(selenium,base_url)
    fliter_button.click_filter_button_on_websites_page()

@when('the user set filter options')
def set_filter_options_in_website_search(selenium,base_url):
    fliter_button = DashboardWebsitesPage(selenium,base_url)
    fliter_button.click_filter_button_on_websites_page()

def set_MTP_Date(mtp_date):
    date_time_obj = datetime.strptime(mtp_date, '%d/%m/%Y')
    if date_time_obj.isoweekday() == 6:
        date_time_obj += timedelta(days=2)
    elif date_time_obj.isoweekday() == 7:
        date_time_obj += timedelta(days=1)
    else:
        date_time_obj += timedelta(days=0)
    return datetime.strftime(date_time_obj, '%d/%m/%Y')


@when("the user fills the MTP form with <mtp_type>,<mtp_date>,<mtp_date_time_zone>,<service_request>,<SCO>,<vendor_assignee>,<manual_verification_text>")
def fill_mtp_form(selenium,base_url,mtp_type,mtp_date,mtp_date_time_zone,service_request,SCO,vendor_assignee,manual_verification_text):
    prepare_mtp_form = DashboardPrepareMTPPage(selenium,base_url)
    mtp_date = set_MTP_Date(mtp_date)
    prepare_mtp_form.fill_mtp_form(mtp_type,mtp_date,mtp_date_time_zone,service_request,SCO,vendor_assignee,manual_verification_text)


@when("the user clicks on MTPs in Tools menu")
def navigate_to_mtps_page(selenium,base_url):
    mtps_page = DashboardMTPsPage(selenium,base_url)
    mtps_page.go_to_mtps_page()
    
@when("the user deletes the MTP")
def deletes_existing_mtps_available_for_sitename(selenium,base_url):
    # Get All mtps by site name
    mtpsPage = DashboardMTPsPage(selenium,base_url)
    all_mtps = mtpsPage.fetch_all_existing_mtps_of_a_site(base_url)
    mtpsPage.delete_mtps(all_mtps)

# @when("the the user logs in to JIRA")
# def login_to_jira(selenium,base_url):
#     mtpsPage = DashboardMTPsPage(selenium,base_url)
#     mtpsPage.login_to_jira()

@when("the user advances MTP of the <site> into Ready for deployment state")
def advance_the_mtp_from_preparation_to_Ready_for_deployment(selenium,base_url,site):
    mtpsPage = DashboardMTPsPage(selenium,base_url)
    mtpsPage.act_on_verify_DNS_and_request_cutover_section(selenium,base_url,site)
    mtpsPage.act_on_SDLC_ticket_in_mtp(selenium,base_url,site)
    
    # mtpsPage.act_on_SDLC_ticket_in_mtp(selenium,base_url)
    # mtpsPage.act_on_verify_DNS_and_request_cutover()

@when("the user advances MTP of the <site> into Deployment progress state")
def advance_the_mtp_from_Ready_for_deployment_to_deployment_in_progress(selenium,base_url,site):
    mtpsPage = DashboardMTPsPage(selenium,base_url)
    mtpsPage.perform_mtp_actions_in_ready_for_deployment_state(selenium,base_url,site)
    
@when("the user publishes a changelog with <title><change_record_Type><event_date><affects><summary><body><notifications><contacts><save_as><revision_log_message>")
def create_a_changelog(selenium,base_url,title,change_record_Type,event_date,affects,summary,body,notifications,contacts,save_as,revision_log_message):
   create_changelog_record = CreateChangeLogPage(selenium,base_url)
   create_changelog_record.create_change_record(title,change_record_Type,event_date,affects,summary,body,notifications,contacts,save_as,revision_log_message)
   
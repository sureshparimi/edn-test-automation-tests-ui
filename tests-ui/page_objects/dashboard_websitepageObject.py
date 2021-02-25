from assertpy import assert_that
from selenium.webdriver.common.by import By
from page_objects.locators import DashBoardWebsitesPageLocators
from page_objects.locators import DashboardHomePageLocators
from page_objects.locators import HamburgerMenuLinksLocators
from page_objects.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait

class DashboardWebsitesPage(BasePage):
  
    
    def input_sitename_search_filters(self,sitename_value):
        sitename = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.sitename)
        sitename.send_keys(sitename_value)
        
    def set_offering_type_search_filters(self,sitename_value):
        sitename = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.offering)
        sitename.send_keys(sitename_value)
        
    def __fliter_button_on_website_page(self):
        filter_button = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.filter_button)
        return filter_button
    
    
    def click_filter_button_on_websites_page(self):
        self.__fliter_button_on_website_page().click()
        self._wait.static_wait(10)
        
        # audience = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.audience)
        # offering = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.offering)
        # usermanagement = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.usermanagement)
        # testsite = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.testsite)
        # autologouttime = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.autologouttime)
        # live = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.live)
        # internaldns = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.internaldns)
        # framework = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.framework)
        # tags = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.tags)
        # microservices = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.microservices)
        # filter_button = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.filter_button)
        # search_results_table_header_count = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.search_results_table_header_count)
        # number_of_websites_displayed_in_search_results = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.number_of_websites_displayed_in_search_results)
        # No_sites_available = self._selenium.find_element(by=By.XPATH, value=DashBoardWebsitesPageLocators.No_sites_available)

    def __edison_custom_offering_type(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.offering_type)


    def click_edison_custom_in_websites_menu(self):
        self._wait.static_wait(10)
        self.__edison_custom_offering_type().click()
        self._wait.static_wait(5)
        
    def get_selected_offering_from_filters(self):
        selected_offering = self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.selected_offering_type_in_fliters)
        return selected_offering.text

    def __edison_custom_offering_type(self):
        return self._selenium.find_element(by=By.XPATH, value=DashboardHomePageLocators.offering_type)

    def click_offering_type_in_websites_menu(self,offering_type):
        self.__offering_type_on_websites_menu(offering_type).click()

    def __offering_type_on_websites_menu(self,offering_type):
        xparth_string_part1 = str("//a[contains(text(),")
        xparth_string_part2 = str(")]")
        complete_xpath = xparth_string_part1 + '"' + offering_type + '"'+ xparth_string_part2
        return self._selenium.find_element(by=By.XPATH, value=complete_xpath)

    def __get_all_site_links_from_search_results(self):
        return  self._selenium.find_elements(by=By.XPATH, value=DashBoardWebsitesPageLocators.all_websites_displayed_in_search_results)

    def __get_all_sites_from_search_results(self):
        sites = self._selenium.find_elements_by_xpath('//tbody/tr//td[1]//*[@href]')
        sites_urls = {}
        for each_site in sites:
            each_site_url = each_site.get_attribute('href')
            key = each_site_url.rsplit('/',1)[-1]    # fetches the site name from the site url
            sites_urls[key]=each_site_url
        return sites_urls
    
    def sitename_exists_in_search_results(self,sitename):
        all_sites = self.__get_all_sites_from_search_results()
        # print("This the dict of all sites",all_sites)
        if sitename in all_sites.keys():
            return (sitename,all_sites[sitename])

    def go_to_site_from_search_results(self,sitename):
        all_sites = self.__get_all_sites_from_search_results()
        # print("This the dict of all sites",all_sites)
        if sitename in all_sites:
            xparth_string_part1 = str("//a[contains(text(),")
            xparth_string_part2 = str(")]")
            complete_xpath = xparth_string_part1 + '"' + sitename + '"'+ xparth_string_part2
            site_to_go_to = self._selenium.find_element(by=By.XPATH,value=complete_xpath)
            site_to_go_to.click()   # clicks the site link in the search results
            self._wait.static_wait(5)

    def is_prepare_mtp_link_exists_in_hamburger_menu(self):
        self._wait.static_wait(5)
        hamburger_menu = self._selenium.find_element(by=By.XPATH, value=HamburgerMenuLinksLocators.hamburger_icon)
        hamburger_menu.click()
        prepare_mtp_link = self._selenium.find_element(by=By.XPATH, value=HamburgerMenuLinksLocators.prepare_mtp_link_in_hamburger_menu)
        prepare_mtp_link.click()
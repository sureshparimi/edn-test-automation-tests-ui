from assertpy import assert_that
from pytest_bdd import then, parsers
from pytest_selenium_enhancer import CustomWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from page_objects.selenium_generics import SeleniumGenerics
from utils.locators import Locators
from page_objects.dashboard_homepage import DashboardHomePage
from page_objects.dashboard_homeObject import DashboardWebsitePage
from page_objects.dashboard_websitepageObject import DashboardWebsitesPage
from page_objects.dashboard_mtps_pageObject import DashboardMTPsPage
from page_objects.locators import DashboardLoginPageLocators


@then(parsers.re("I expect that the title is '(?P<title>.*)'"))
def check_title_is(selenium, title):
    assert_that(selenium.title).is_equal_to(title)


@then(parsers.re("I expect that the title is not '(?P<title>.*)'"))
def check_title_is_not(selenium, title):
    assert_that(selenium.title).is_not_equal_to(title)


@then(parsers.re("I expect that the title contains '(?P<title>.*)'"))
def check_title_contains(selenium, title):
        assert_that(selenium.title).contains(title)


@then(parsers.re("I expect that the title does not contain '(?P<title>.*)'"))
def check_title_not_contains(selenium, title):
    assert_that(selenium.title).does_not_contain(title)


@then(parsers.re("I expect that element '(?P<locator_path>.*)' appears exactly '(?P<occurrence_count>.*)' times"))
def check_element_exists(selenium, locators: Locators, locator_path, occurrence_count):
    locator = locators.parse_and_get(locator_path)
    assert_that(selenium.find_elements(By.XPATH, locator).__len__()).is_equal_to(occurrence_count)


@then(parsers.re("I expect that element '(?P<locator_path>.*)' does not appear exactly '(?P<occurrence_count>.*)' times"))
def check_element_not_exists(selenium, locators: Locators, locator_path, occurrence_count):
    locator = locators.parse_and_get(locator_path)
    assert_that(selenium.find_elements(By.XPATH, locator).__len__()).is_not_equal_to(occurrence_count)


@then(parsers.re("I expect that element '(?P<locator_path>.*)' is displayed"))
def element_displayed(selenium, locators: Locators, locator_path):
    assert_that(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)).is_displayed()).is_true()


@then(parsers.re("I expect that element '(?P<locator_path>.*)' is not displayed"))
def element_not_displayed(selenium, locators: Locators, locator_path):
    assert_that(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)).is_displayed()).is_false()


@then(parsers.re("I expect that element '(?P<locator_path>.*)' becomes visible"))
def wait_for_displayed(selenium, locators: Locators, locator_path):
    CustomWait(selenium).wait_for_element_visible(value=locators.parse_and_get(locator_path))


@then(parsers.re("I expect that element '(?P<locator_path>.*)' becomes invisible"))
def wait_for_not_displayed(selenium, locators: Locators, locator_path):
    CustomWait(selenium).wait_for_element_not_visible(value=locators.parse_and_get(locator_path))


@then(parsers.re("I expect that element '(?P<locator_path>.*)' is within the viewport"))
def check_within_viewport(selenium, locators: Locators, locator_path):
    assert_that(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)).is_in_viewport()).is_true()


@then(parsers.re("I expect that element '(?P<locator_path>.*)' is not within the viewport"))
def check_within_viewport(selenium, locators: Locators, locator_path):
    assert_that(selenium.find_element(By.XPATH, locators.parse_and_get(locator_path)).is_in_viewport()).is_false()


@then(parsers.re("I expect that element '(?P<locator_path>.*)' exists"))
def check_is_existing(selenium, locators: Locators, locator_path):
    CustomWait(selenium).wait_for_element_present(value=locators.parse_and_get(locator_path))


@then(parsers.re("I expect that element '(?P<locator_path>.*)' does not exist"))
def check_element_not_existing(selenium, locators: Locators, locator_path):
    CustomWait(selenium).wait_for_element_not_visible(value=locators.parse_and_get(locator_path))


@then(parsers.re("I expect that element '(?P<locator_path1>.*)' contains the same text as element'(?P<locator_path2>.*)'$"))
def check_contains_same_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path1, locator_path2):
    actual_text1 = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path1))
    actual_text2 = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path2))
    assert_that(actual_text1).is_equal_to(actual_text2)


@then(parsers.re("I expect that element '(?P<locator_path1>.*)' does not contain the same text as element'(?P<locator_path2>.*)'$"))
def check_does_not_contain_same_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path1, locator_path2):
    actual_text1 = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path1))
    actual_text2 = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path2))
    assert_that(actual_text1).is_not_equal_to(actual_text2)


@then(parsers.re("The button '(?P<locator_path>.*)' text is '(?P<text>.*)'"))
@then(parsers.re("The element '(?P<locator_path>.*)' text is '(?P<text>.*)'"))
def check_element_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, text):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).is_equal_to(text)


@then(parsers.re("The button '(?P<locator_path>.*)' text is not '(?P<text>.*)'"))
@then(parsers.re("The element '(?P<locator_path>.*)' text is not '(?P<text>.*)'"))
def check_element_not_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, text):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).is_not_equal_to(text)


@then(parsers.re("The button '(?P<locator_path>.*)' contains the text '(?P<text>.*)'"))
@then(parsers.re("The element '(?P<locator_path>.*)' contains the text '(?P<text>.*)'"))
def check_contains_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, text):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).contains(text)


@then(parsers.re("The button '(?P<locator_path>.*)' does not contain the text '(?P<text>.*)'"))
@then(parsers.re("The element '(?P<locator_path>.*)' does not contain the text '(?P<text>.*)'"))
def check_not_contains_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, text):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).does_not_contain(text)


@then(parsers.re("The button '(?P<locator_path>.*)' does not contain any text"))
@then(parsers.re("The element '(?P<locator_path>.*)' does not contain any text"))
def check_contains_no_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).matches(r'^$')


@then(parsers.re("The button '(?P<locator_path>.*)' contains any text"))
@then(parsers.re("The element '(?P<locator_path>.*)' contains any text"))
def check_contains_any_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    actual_text = selenium_generics.get_text_from_element(locators.parse_and_get(locator_path))
    assert_that(actual_text).matches(r'(.*?)')


@then(parsers.re("The page url is '(?P<url>.*)'"))
def check_page_url(selenium, url):
    assert_that(selenium.current_url).is_equal_to(url)


@then(parsers.re("The page url is not '(?P<url>.*)'"))
def check_page_url_is_not(selenium, url):
    assert_that(selenium.current_url).is_not_equal_to(url)


@then(parsers.re("The page path is '(?P<url>.*)'"))
@then(parsers.re("The page url contains '(?P<url>.*)'"))
def check_page_url_contains(selenium, url):
    assert_that(selenium.current_url).contains(url)


@then(parsers.re("The page path is not '(?P<url>.*)'"))
@then(parsers.re("The page url does not contain '(?P<url>.*)'"))
def check_page_url_not_contains(selenium, url):
    assert_that(selenium.current_url).does_not_contain(url)


@then(parsers.re("The attribute '(?P<attribute>.*)' from element '(?P<locator_path>.*)' is '(?P<value>.*)'"))
def check_property_is(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, value, attribute):
    actual_value = selenium_generics.get_attribute_of_element(locators.parse_and_get(locator_path), attribute)
    assert_that(actual_value).is_equal_to(value)


@then(parsers.re("The attribute '(?P<attribute>.*)' from element '(?P<locator_path>.*)' is not '(?P<value>.*)'"))
def check_property_is_not(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, value, attribute):
    actual_value = selenium_generics.get_attribute_of_element(locators.parse_and_get(locator_path), attribute)
    assert_that(actual_value).is_not_equal_to(value)


@then(parsers.re("The css attribute '(?P<attribute>.*)' from element '(?P<locator_path>.*)' is '(?P<value>.*)'"))
def check_css_property_is(attribute, selenium_generics: SeleniumGenerics, locators: Locators, locator_path, value):
    actual_value = selenium_generics.get_css_attribute_of_element(locators.parse_and_get(locator_path), attribute)
    assert_that(actual_value).is_equal_to(value)


@then(parsers.re("The css attribute '(?P<attribute>.*)' from element '(?P<locator_path>.*)' is not '(?P<value>.*)'"))
def check_css_property_is_not(attribute, selenium_generics: SeleniumGenerics, locators: Locators, locator_path, value):
    actual_value = selenium_generics.get_css_attribute_of_element(locators.parse_and_get(locator_path), attribute)
    assert_that(actual_value).is_not_equal_to(value)


@then(parsers.re("The element '(?P<locator_path>.*)' is selected"))
def check_element_selected(selenium, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path)
    CustomWait(selenium).wait_for_element_visible(value=locator)
    assert_that(selenium.find_element(By.XPATH, locator).is_selected()).is_true()


@then(parsers.re("The element '(?P<locator_path>.*)' is not selected"))
def check_element_not_selected(selenium, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path)
    CustomWait(selenium).wait_for_element_visible(value=locator)
    assert_that(selenium.find_element(By.XPATH, locator).is_selected()).is_false()


@then(parsers.re("The element '(?P<locator_path>.*)' is enabled"))
def check_element_enabled(selenium, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path)
    CustomWait(selenium).wait_for_element_visible(value=locator)
    assert_that(selenium.find_element(By.XPATH, locator).is_enabled()).is_true()


@then(parsers.re("The element '(?P<locator_path>.*)' is not enabled"))
def check_element_not_enabled(selenium, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path)
    CustomWait(selenium).wait_for_element_visible(value=locator)
    assert_that(selenium.find_element(By.XPATH, locator).is_enabled()).is_false()


@then(parsers.re("The url '(?P<url>.*)' is opened in a new tab"))
@then(parsers.re("The url '(?P<url>.*)' is opened in a new window"))
def check_is_opened_in_new_window(selenium, url):
    windows = selenium.window_handles
    window = windows[-1]
    selenium.switch_to_window(window)
    assert_that(selenium.current_url).is_equal_to(url)


@then(parsers.re("A alertbox is opened"))
@then(parsers.re("A confirmbox is opened"))
@then(parsers.re("A prompt is opened"))
def check_modal():
    from selenium.webdriver.support import expected_conditions as EC
    assert_that(EC.alert_is_present()).is_true()


@then(parsers.re("A alertbox is not opened"))
@then(parsers.re("A confirmbox is not opened"))
@then(parsers.re("A prompt is not opened"))
def check_modal_not_present():
    from selenium.webdriver.support import expected_conditions as EC
    assert_that(EC.alert_is_present()).is_false()


@then(parsers.re("There are '(?P<count>.*)' tabs currently opened"), converters=dict(count=int))
@then(parsers.re("There are '(?P<count>.*)' windows currently opened"), converters=dict(count=int))
def check_number_of_tabs(selenium, count: int):
    assert_that(len(selenium.window_handles)).is_equal_to(count)


@then(parsers.re("A new tab is opened"))
@then(parsers.re("A new window is opened"))
def check_new_window(selenium):
    windows = selenium.window_handles
    assert_that(windows.__len__()).is_greater_than(1)


@then(parsers.re("A new tab is not opened"))
@then(parsers.re("A new window is not opened"))
def check_no_new_window(selenium):
    windows = selenium.window_handles
    assert_that(windows.__len__()).is_equal_to(1)

@then("user should see <fullname> on the dashboard")
@then(parsers.re("user should see'(?P<fullname>.*)'on the dashboard"))
def test_username_on_dashboard(selenium,fullname):
    home_page = DashboardWebsitePage()
    #assert welcomebacktext == home_page.welcome_back_text_on_dashboard()
    assert fullname == home_page.fullname_on_dashboard()


@then("the user should see websites header on the websites page")
def test_websites_page(selenium,base_url):
    homepage = DashboardWebsitePage(selenium,base_url)
    websites_page_header_text = homepage.get_text_on_websites_page()
    assert  websites_page_header_text == "Websites"
    
@then("the user should see <offering_type> as selected offering type in filters")
def test_selected_offering_type_from_filters(selenium,base_url,offering_type):
    homepage = DashboardWebsitesPage(selenium,base_url)
    offering_type_from_filters = homepage.get_selected_offering_from_filters()
    assert  offering_type_from_filters == offering_type
    

@then("the search results contain <sitename_value>")
def test_site_displayed_in_search_results(selenium,base_url,sitename_value):
    websitespage = DashboardWebsitesPage(selenium,base_url)
    site_from_search_results = websitespage.sitename_exists_in_search_results(sitename_value)
    assert site_from_search_results[0] is not None
    assert site_from_search_results[0] == sitename_value

@then("the user clicks on <sitename_value> from the search results")
def test_go_to_site_in_search_results(selenium,base_url,sitename_value):
    websitespage = DashboardWebsitesPage(selenium,base_url)
    websitespage.go_to_site_from_search_results(sitename_value)


@then("MTP should not be available on the dashboard")
def test_if_deleted_mtp_is_available(selenium,base_url):
    pass

@then("an MTP should be created successfully with Preparation state on <sitename>")
def test_is_MTP_created_successfully(selenium,base_url,sitename):
    MTPPage = DashboardMTPsPage(selenium, base_url)
    current_active_state = MTPPage.get_current_active_MTP_state().text
    StringList = current_active_state.split('\n')
    assert StringList[1] == "PREPARATION"
    MTPPage.write_mtps_to_dashboard_mtp_test_dataJson(sitename)
    
@then("MTP is in Ready for deployment state")
def test_mtp_is_in_ready_for_deployment_state(selenium,base_url):
    MTPPage = DashboardMTPsPage(selenium, base_url)
    MTPPage.reload_page()
    current_active_state = MTPPage.get_current_active_MTP_state().text
    StringList = current_active_state.split('\n')
    print("This is the current state of",StringList[1])
    assert StringList[1] == "READY FOR DEPLOYMENT"
    perform_button = MTPPage.perform_mtp_button_ready_for_deployment_state()
    if perform_button.is_displayed():
        print("The mtp is in Ready for deployment state")
    else:
        print("The PERFORM MTP button is not available")

@then("MTP is in deployment progress state")
def test_mtp_is_in_ready_for_deployment_state(selenium,base_url):
    MTPPage = DashboardMTPsPage(selenium, base_url)
    MTPPage.reload_page()
    current_active_state = MTPPage.get_current_active_MTP_state().text
    StringList = current_active_state.split('\n')
    print("This is the current state of",StringList[1])
    if StringList[1] == "DEPLOYMENT IN PROGRESS":
        print("The mtp is in DEPLOYMENT IN PROGRESS state")
    elif StringList[1] == "VERIFICCATION":
        print("The MTP automatically moved to Verification state")
    else:
        print("Something went wrong, The MTP is neither in deployment in progress or verification state")
import json
import os
import re

from assertpy import soft_assertions, assert_that
from lxml import etree

import pytest
import requests

from pytest_bdd import when, parsers, given, then
from pytest_selenium_enhancer import CustomWait
from requests import HTTPError
from selenium.webdriver.common.by import By

from actions.browser import BrowserActions
from page_objects.selenium_generics import SeleniumGenerics
from utils.gherkin_utils import data_table_vertical_converter, data_table_horizontal_converter
from utils.locators import Locators


@given("I navigate to external page <url>")
@given(parsers.re("I navigate to external page '(?P<url>.*)'"), converters=dict(url=str))
def navigate_to_external_page(browser: BrowserActions, url):
    browser.go_to_url(url)


@when("I click on <locator_path>")
@when(parsers.re("I click on '(?P<locator_path>.*)'"), converters=dict(locator_path=str))
def click_on_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.scroll_into_view(selector=xpath)
    selenium_generics.click(selector=xpath)


@when("I click on shadowElement <element_path>")
@when(parsers.re("I click on shadowElement:(?P<element_path>.*)", flags=re.S),
      converters=dict(element_path=data_table_horizontal_converter))
def click_on_shadow_element(selenium_generics: SeleniumGenerics, locators: Locators, element_path):
    parent_xpath = locators.parse_and_get(element_path['parent_xpath'][0])
    locator_paths = [ locators.parse_and_get(path) for path in element_path['shadow_path'][0].split(' ~ ') ]
    selenium_generics.shadow_click(parent_xpath, *locator_paths)


@when("I hover over <locator_path>")
@when(parsers.re("I hover over '(?P<locator_path>.*)'"), converters=dict(locator_path=str))
def hover_over_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.scroll_into_view(selector=xpath)
    selenium_generics.hover(selector=xpath)


@when("I hover over shadowElement <element_path>")
@when(parsers.re("I hover over shadowElement:(?P<element_path>.*)", flags=re.S),
      converters=dict(element_path=data_table_horizontal_converter))
def hover_over_shadow_element(selenium_generics: SeleniumGenerics, locators: Locators, element_path):
    parent_xpath = locators.parse_and_get(element_path['parent_xpath'])
    locator_paths = [ locators.parse_and_get(path) for path in element_path['shadow_path'].split(' ~ ') ]
    selenium_generics.shadow_hover(parent_xpath, *locator_paths)


@when(parsers.re("I set '(?P<component_locator>.*)' component style:(?P<data_table>.*)", flags=re.S),
      converters=dict(html_block=str, paragraph=int, data_table=data_table_vertical_converter))
def nextgen_simple_card_style(selenium_generics: SeleniumGenerics, component_locator, data_table):
    selenium_generics.set_component_style(component_locator, data_table)


@when("I collect all urls from sitemap")
def urls_from_sitemap(base_url):
    response = requests.get(f'{base_url}/sitemap.xml')
    if response.status_code != 200:
        raise HTTPError('Status Code was not 200. Exiting!!')

    root = etree.fromstring(response.content)

    urls = []
    for sitemap in root:
        children = sitemap.getchildren()
        urls.append(children[0].text)

    pytest.scenarioDict['urls'] = urls


@when(parsers.re("I fetch all urls from external site '(?P<site_url>.*)' sitemap"))
def urls_from_sitemap(site_url, log):
    log.info(f'Collecting sitemap URLs for {site_url}')
    response = requests.get(f'{site_url}/sitemap.xml')
    if response.status_code != 200:
        raise requests.HTTPError('Status Code was not 200. Exiting!!')

    root = etree.fromstring(response.content)

    urls = []
    for sitemap in root:
        children = sitemap.getchildren()
        urls.append(children[0].text)

    pytest.scenarioDict['urls'] = urls


@then(parsers.re("Sitemap urls are fetching"))
def sitemap_urls_loading(log):
    urls = pytest.scenarioDict['urls']
    with soft_assertions():
        for url in urls:
            log.info(f'Loading URL: {url}')
            response = requests.get(url, allow_redirects=False)
            assert_that(response.url, description=f'URL {response.url} is not the same with {url}').is_subset_of(url)
            assert_that(response.status_code, description=f'URL {url} load status code is {response.status_code}').is_less_than_or_equal_to(307)


@then(parsers.re("External site '(?P<site_url>.*)' url is fetching"))
@then(parsers.re("External url '(?P<site_url>.*)' url is fetching"))
def check_external_site_loading(site_url):
    status_code = pytest.scenarioDict['status_code']
    with soft_assertions():
        assert_that(status_code, description=f'URL {site_url} load status code is {status_code}').is_less_than(300)


@when(parsers.re("Sitemap pages, take a full page screenshot with actions:(?P<data_table>.*)", flags=re.S),
      converters=dict(data_table=data_table_vertical_converter))
def take_full_page_screenshot_from_sitemap_with_actions(selenium, selenium_generics, base_url, data_table):
    pytest.scenarioDict['screenshots'] = pytest.scenarioDict['screenshots'] \
        if 'screenshots' in pytest.scenarioDict else []
    pytest.scenarioDict['pdf_file_name'] = \
        f"{pytest.globalDict['actual_screenshot_dir']}/full_page/{data_table['site']}_{selenium.get_window_size()['width']}_{selenium.get_window_size()['height']}.pdf"
    urls = pytest.scenarioDict['urls']
    custom_wait = CustomWait(selenium)

    for url in urls:
        response = requests.get(url, allow_redirects=False)
        if response.status_code >= 300:
            continue
        selenium.get(url)
        custom_wait.static_wait(10)

        page_size = selenium_generics.page_size()
        if page_size['height'] < 100 or page_size['width'] < 100:
            continue

        actual_screenshot_dir = selenium_generics.get_actual_screenshot_dir(url, base_url, '01', data_table)
        elements_to_hide = selenium_generics.get_elements_to_hide(data_table)
        device_offset = selenium.capabilities['deviceOffset'] if 'deviceOffset' in selenium.capabilities else 0

        if data_table['pre_action_screenshot'] == 'true':
            selenium.get_full_page_screenshot_as_png(actual_screenshot_dir, elements_to_hide, device_offset)
            pytest.scenarioDict['screenshots'].append(actual_screenshot_dir)
            base_screenshot_dir = actual_screenshot_dir

        for action in json.loads(data_table['actions']):
            selenium_generics.execute_action(action)

        custom_wait.static_wait(2)
        selenium.execute_script('window.scrollTo({ left: 0, top: 0});')
        custom_wait.static_wait(2)

        actual_screenshot_dir = selenium_generics.get_actual_screenshot_dir(url, base_url, '02', data_table)
        selenium.get_full_page_screenshot_as_png(actual_screenshot_dir, elements_to_hide, device_offset)

        if data_table['pre_action_screenshot'] == 'true':
            from utils.utils import compare_images
            base_score = 0.999
            score = compare_images(None, base_screenshot_dir, actual_screenshot_dir, None, base_score)
            if score >= base_score:
                import os
                os.remove(actual_screenshot_dir)
            else:
                pytest.scenarioDict['screenshots'].append(actual_screenshot_dir)


@when(parsers.re("Take screenshots of elements with actions:(?P<data_table>.*)", flags=re.S),
      converters=dict(data_table=data_table_vertical_converter))
def take_element_screenshot_with_actions(selenium, selenium_generics, base_url, data_table):
    pytest.scenarioDict['screenshots'] = pytest.scenarioDict['screenshots'] \
        if 'screenshots' in pytest.scenarioDict else []

    custom_wait = CustomWait(selenium)

    actions = json.loads(data_table['actions'])
    if 'menu_button' in actions:
        selenium_generics.click(selector=actions['menu_button'])
        custom_wait.static_wait(4)

        actual_screenshot_dir = selenium_generics. \
            get_actual_screenshot_dir(base_url, base_url, 'megamenu_0', data_table)
        selenium.find_element(By.XPATH, actions['menu']).screenshot(actual_screenshot_dir)
        pytest.scenarioDict['screenshots'].append(actual_screenshot_dir)

    elements = selenium.find_elements(By.XPATH, actions['hover']) if 'hover' in actions \
        else selenium.find_elements(By.XPATH, actions['click']) if 'click' in actions \
        else []

    i = 1
    for element in elements:
        if 'hover' in actions:
            selenium_generics.hover(element=element)
            element = element.find_element(By.XPATH, actions['expanded'])
            custom_wait.static_wait(2)
            image_b = element.screenshot_as_base64
            element = selenium.find_element(By.XPATH, '//div[contains(@class, "bg-image")]')
            custom_wait.static_wait(2)
            image_a = element.screenshot_as_base64

            import base64
            from io import BytesIO
            from PIL import Image
            image_a = Image.open(BytesIO(base64.b64decode(image_a)))
            image_b = Image.open(BytesIO(base64.b64decode(image_b)))

            stitched_image = Image.new('RGB', (image_a.width, image_a.height + image_b.height))
            stitched_image.paste(im=image_a, box=(0, 0))
            stitched_image.paste(im=image_b, box=(0, image_a.height))

            i = i + 1
            actual_screenshot_dir = selenium_generics. \
                get_actual_screenshot_dir(base_url, base_url, f'megamenu_{i}', data_table)
            stitched_image.save(actual_screenshot_dir)
            pytest.scenarioDict['screenshots'].append(actual_screenshot_dir)

        if 'click' in actions:
            selenium_generics.click(element=element)
            custom_wait.static_wait(2)
            element = element.find_element(By.XPATH, actions['expanded'])
            actual_screenshot_dir = selenium_generics. \
                get_actual_screenshot_dir(base_url, base_url, f'megamenu_{i}', data_table)
            element.screenshot(actual_screenshot_dir)
            i = i + 1
            pytest.scenarioDict['screenshots'].append(actual_screenshot_dir)
            if 'click' in actions:
                selenium_generics.click(element=selenium.find_elements(By.XPATH, actions['click'])[0])


@then("Element <locator_path> state should be displayed")
@then(parsers.re("Element '(?P<locator_path>.*)' state should be displayed"),
      converters=dict(locator_path=str, state=str))
def element_is_displayed(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.is_element_visible(xpath)


@then("Element <locator_path> state should be hidden")
@then(parsers.re("Element '(?P<locator_path>.*)' state should be hidden"),
      converters=dict(locator_path=str, state=str))
def element_is_hidden(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.is_element_invisible(xpath)


@then("Element <locator_path> text should be <expected_text>")
@then(parsers.re("Element '(?P<locator_path>.*)' text should be '(?P<expected_text>.*)'"),
      converters=dict(locator_path=str, expected_text=str))
def element_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, expected_text):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.validate_element_text(xpath, expected_text)


@then(parsers.re("Element '(?P<locator_path>.*)' style should be:(?P<data_table>.*)", flags=re.S),
      converters=dict(locator_path=str, data_table=data_table_vertical_converter))
def header_menu_button_style(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, data_table):
    xpath = locators.parse_and_get(locator_path)
    selenium_generics.validate_element_style(xpath, data_table)


@then(parsers.re("ShadowElement style should be:(?P<data_table>.*)", flags=re.S),
      converters=dict(button_text=str, data_table=data_table_vertical_converter))
def header_menu_button_style(selenium_generics: SeleniumGenerics, data_table):
    selenium_generics.validate_shadow_element_style(data_table)


@then("Page <page_url> is loaded")
@then(parsers.re("Page '(?P<page_url>.*)' is loaded"), converters=dict(page_url=str))
def page_loaded(selenium_generics: SeleniumGenerics, page_url):
    selenium_generics.validate_page_loaded(page_url)


@then(parsers.re("Page scroll position is '(?P<scroll_position>.*)'"), converters=dict(scroll_position=str))
def page_scroll_position(selenium_generics: SeleniumGenerics, scroll_position):
    selenium_generics.validate_scroll_position(scroll_position)


@then(parsers.re("Page visual regression is correct:(?P<data_table>.*)", flags=re.S),
      converters=dict(data_table=data_table_horizontal_converter))
def page_visual_is_valid(selenium, selenium_generics: SeleniumGenerics, data_table):
    custom_wait = CustomWait(selenium)

    custom_wait.static_wait(2)
    selenium.execute_script(
        'window.scrollTo({ left: 0, top: 0});')
    custom_wait.static_wait(4)

    base_screenshot_dir = f"{pytest.globalDict['base_screenshot_dir']}/full_page/{data_table['page_name'][0]}_{selenium_generics._file_extension()}"
    actual_screenshot_dir = f"{pytest.globalDict['actual_screenshot_dir']}/full_page/{data_table['page_name'][0]}_{selenium_generics._file_extension()}"
    diff_screenshot_dir = f"{pytest.globalDict['diff_screenshot_dir']}/full_page/{data_table['page_name'][0]}_{selenium_generics._file_extension()}"

    device_offset = selenium.capabilities['deviceOffset'] \
        if 'deviceOffset' in selenium.capabilities else 0
    elements_to_hide = {
        "start": data_table['start'] if data_table['start'][0] != 'None' else None,
        "all": data_table['all'] if data_table['all'][0] != 'None' else None,
        "end": data_table['end'] if data_table['end'][0] != 'None' else None,
    }
    image_cv2 = selenium.get_full_page_screenshot_as_base64(elements_to_hide, device_offset)

    from utils.utils import compare_images
    base_score = 0.999
    score = compare_images(image_cv2, base_screenshot_dir, actual_screenshot_dir, diff_screenshot_dir, base_score)
    assert score >= base_score, f"Actual component screenshot is different from Base with {score}. Diff saved here: {diff_screenshot_dir}"


@then("I generate a pdf for the screenshots taken")
def generate_pdf():
    from PIL import Image

    screenshots = pytest.scenarioDict['screenshots']
    pdf_file_name = pytest.scenarioDict['pdf_file_name']

    images = []
    for screenshot in screenshots:
        images.append(Image.open(screenshot).convert('RGB'))

    first_image = images[0]
    del images[0]
    first_image.save(pdf_file_name, save_all=True, append_images=images)


@then("I generate pdfs for the screenshots taken")
def generate_pdfs():
    from PIL import Image
    screenshots = pytest.scenarioDict['screenshots']

    for screenshot in screenshots:
        image = Image.open(screenshot).convert('RGB')
        image.save(screenshot.replace('.png', '.pdf'))


@when(parsers.re("I set '(?P<component_locator>.*)' component style:(?P<data_table>.*)", flags=re.S),
      converters=dict(html_block=str, paragraph=int, data_table=data_table_vertical_converter))
def nextgen_simple_card_style(selenium_generics: SeleniumGenerics, component_locator, data_table):
    selenium_generics.set_component_style(component_locator, data_table)


@then("root folder structure is correct")
def check_feature_folder():
    assert_that(os.path.isfile('./.editorconfig')).is_true()
    assert_that(os.path.isfile('./.gitignore')).is_true()
    assert_that(os.path.isfile('./.local.env')).is_true()
    assert_that(os.path.isfile('./.pylintrc')).is_true()
    assert_that(os.path.isfile('./conftest.py')).is_true()
    assert_that(os.path.isfile('./i18n.json')).is_true()
    assert_that(os.path.isfile('./install.sh')).is_true()
    assert_that(os.path.isfile('./pytest.ini')).is_true()
    assert_that(os.path.isfile('./README.md')).is_true()
    assert_that(os.path.isfile('./requirements.txt')).is_true()
    assert_that(os.path.isfile('./variables.json')).is_true()


@then("features folder structure is correct")
def check_feature_folder():
    assert_that(os.path.isdir('./features')).is_true()
    assert_that(os.path.isdir('./features/codeless')).is_true()
    assert_that(os.path.isdir('./features/installation_check')).is_true()


@then("page_objects folder structure is correct")
def check_page_objects_folder():
    assert_that(os.path.isdir('./page_objects')).is_true()
    assert_that(os.path.isfile('./page_objects/base_component.py')).is_true()
    assert_that(os.path.isfile('./page_objects/base_page.py')).is_true()
    assert_that(os.path.isfile('./page_objects/selenium_generics.py')).is_true()


@then("screenshots folder structure is correct")
def check_screenshots_folder():
    assert_that(os.path.isdir('./screenshots')).is_true()
    assert_that(os.path.isdir('./screenshots/base')).is_true()


@then("scripts folder structure is correct")
def check_scripts_folder():
    assert_that(os.path.isdir('./scripts')).is_true()
    assert_that(os.path.isdir('./scripts/installation_scripts')).is_true()


@then("step_definitions folder structure is correct")
def check_step_definitions_folder():
    assert_that(os.path.isdir('./step_definitions')).is_true()
    assert_that(os.path.isfile('./step_definitions/steps_custom.py')).is_true()
    assert_that(os.path.isfile('./step_definitions/steps_given.py')).is_true()
    assert_that(os.path.isfile('./step_definitions/steps_then.py')).is_true()
    assert_that(os.path.isfile('./step_definitions/steps_when.py')).is_true()
    assert_that(os.path.isfile('./step_definitions/test_installation_check.py')).is_true()


@then("test_data folder structure is correct")
def check_test_data_folder():
    assert_that(os.path.isdir('./test_data')).is_true()
    assert_that(os.path.isfile('./test_data/faker_data.py')).is_true()


@then("utils folder structure is correct")
def check_utils_folder():
    assert_that(os.path.isdir('./utils')).is_true()
    assert_that(os.path.isfile('./utils/env_variables.py')).is_true()
    assert_that(os.path.isfile('./utils/gherkin_utils.py')).is_true()
    assert_that(os.path.isfile('./utils/utils.py')).is_true()


@then("webdriver folder structure is correct")
def check_webdriver_folder():
    assert_that(os.path.isdir('./webdriver')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_android_app.json')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_android_web.json')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_ios_app.json')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_ios_web.json')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_web.json')).is_true()
    assert_that(os.path.isfile('./webdriver/capabilities_web_local.json')).is_true()
    assert_that(os.path.isfile('./webdriver/custom_commands.py')).is_true()
    assert_that(os.path.isfile('./webdriver/local_storage.py')).is_true()

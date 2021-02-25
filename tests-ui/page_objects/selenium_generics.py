import traceback

import pytest
import re
from pytest_selenium_enhancer import CustomWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class SeleniumGenerics:

    def __init__(self, selenium):
        self._os = re.sub(r"[\s]*", "", selenium.desired_capabilities['platformName'].lower()) \
            if 'platformName' in selenium.desired_capabilities else \
            re.sub(r"[\s]*", "", selenium.desired_capabilities['platform'].lower())
        self._device = 'mobile' if self._os in ['android', 'ios'] else 'desktop'

        self._selenium = selenium
        self._custom_wait = CustomWait(selenium)

    def click(self, selector=None, element=None):
        if selector is not None:
            element = self.__find_element(selector)
        self._selenium.execute_script('arguments[0].click();', element)

    def execute_action(self, action):
        if 'execute_script_on_elements' in action.keys():
            elements = self.__find_elements(action['execute_script_on_elements']['elements'])
            for element in elements:
                if element.is_displayed() is True:
                    self._custom_wait.static_wait(2)
                    self._selenium.execute_script(action['execute_script_on_elements']['script'], element)
        if 'click' in action.keys():
            elements = self.__find_elements(action['click'])
            for element in elements:
                if element.is_displayed() is True:
                    self._custom_wait.static_wait(2)
                    self.scroll_into_view(element=element)
                    self.click(element=element)

    def shadow_click(self, parent_selector, shadow_path):
        elem = self.__find_shadow_element(parent_selector, shadow_path)
        self._selenium.execute_script('arguments[0].click();', elem)

    def get_actual_screenshot_dir(self, url, base_url, count, data_table):
        page_name = f"{data_table['site']}_{url.replace(base_url, '').replace('/', '_')}_{count}.png"
        resolution = f"{self._selenium.get_window_size()['width']}_{self._selenium.get_window_size()['height']}"
        return f"{pytest.globalDict['actual_screenshot_dir']}/full_page/{data_table['site']}/{resolution}/{page_name}"

    def get_elements_to_hide(self, data_table):
        start_elements = []
        start_elements_locators = data_table['start'].split(' ~ ') if data_table['start'] != 'None' else []
        for start_element_locator in start_elements_locators:
            elements = self._selenium.find_elements(By.XPATH, start_element_locator)
            if elements.__len__():
                start_elements.append(elements[0])

        all_elements = []
        all_elements_locators = data_table['all'].split(' ~ ') if data_table['all'] != 'None' else []
        for all_element_locator in all_elements_locators:
            elements = self._selenium.find_elements(By.XPATH, all_element_locator)
            if elements.__len__():
                all_elements.append(elements[0])

        end_elements = []
        end_elements_locators = data_table['end'].split(' ~ ') if data_table['end'] != 'None' else []
        for end_element_locator in end_elements_locators:
            elements = self._selenium.find_elements(By.XPATH, end_element_locator)
            if elements.__len__():
                end_elements.append(elements[0])

        return {
            "start": start_elements,
            "all": all_elements,
            "end": end_elements,
        }

    def hover(self, selector=None, element=None):
        if selector is not None:
            element = self.__find_element(selector)
        actions = ActionChains(self._selenium)
        actions.move_to_element(element).perform()

    def shadow_hover(self, parent_selector, shadow_path):
        elem = self.__find_shadow_element(parent_selector, shadow_path)
        actions = ActionChains(self._selenium)
        actions.move_to_element(elem).perform()

    def navigate_to_url(self, url):
        self._selenium.get(url)

    def page_size(self):
        return {
            'height': self._selenium.execute_script('return document.body.offsetHeight'),
            'width': self._selenium.execute_script('return document.body.offsetWidth')
        }

    def set_component_style(self, component_locator, data_table):
        script = f'document.body.insertAdjacentHTML("beforeend", ' \
                 f'  "<style>{component_locator} {{ '
        for key in data_table:
            script += f'    --{key}: {data_table[key]}; ' if key in data_table else ''
        script += f'  }}</style>");'
        self._selenium.execute_script(script)

    def scroll_into_view(self, selector=None, element=None):
        if selector is not None:
            element = self.__find_element(selector)
        script = 'arguments[0].scrollIntoView(true)'
        self._selenium.execute_script(script, element)

    def is_element_visible(self, selector) -> bool:
        return self._custom_wait.wait_for_element_visible(selector) is not None

    def is_element_invisible(self, selector) -> bool:
        return self._custom_wait.wait_for_element_not_visible(selector) is not None

    def validate_element_style(self, selector, data_table):
        elem = self.__find_element(selector)
        self.__validate_style(elem, data_table)

    def validate_shadow_element_style(self, data_table):
        elem = self.__find_shadow_element(data_table['parent_xpath'], *data_table['shadow_path'].split(' ~ '))
        data_table.pop('parent_xpath', None)
        data_table.pop('shadow_path', None)
        self.__validate_style(elem, data_table)

    def validate_element_text(self, selector, expected_text):
        elem = self.__find_element(selector)
        inner_text = elem.get_attribute('innerText')
        inner_text = re.sub(r"[\n\t]*", "", inner_text).strip()
        text_content = elem.get_attribute('textContent')
        text_content = re.sub(r"[\n\t]*", "", text_content).strip()

        expected_text = re.sub(r"[\n\t]*", "", str(expected_text)).strip()
        self._custom_wait.wait_until(lambda: inner_text == expected_text or text_content == expected_text,
                                     description=f'Element text is not correct: \nExpected text: {expected_text} '
                                                 f'\nActual inner_text: {inner_text} \nActual text_content: #{text_content}')

    def validate_page_loaded(self, page_url):
        self._custom_wait.wait_until(lambda: self._selenium.current_url == page_url,
                                     description=f'Page not loaded. \nExpected: {page_url} \nActual: {self._selenium.current_url}')
        self._custom_wait \
            .wait_for_the_attribute_value(self._selenium.find_element(By.XPATH, '//html'), 'class', 'hydrated')
        self._custom_wait.static_wait(5)

    def validate_scroll_position(self, scroll_position):
        self._custom_wait.wait_until(
            lambda: self._selenium.execute_script("return window.pageYOffset;") == scroll_position,
            description="Scroll to position %s failed" % scroll_position)

    def _file_extension(self):
        if self._device == 'mobile':
            return '_%s.png' % self._os
        elif 'browserName' in self._selenium.desired_capabilities:
            if self._selenium.desired_capabilities['browserName'] in ['Chrome', 'chrome']:
                return '_%s_chrome.png' % self._os
            if self._selenium.desired_capabilities['browserName'] == 'internet explorer':
                return '_%s_ie.png' % self._os
            if self._selenium.desired_capabilities['browserName'] == 'MicrosoftEdge':
                return '_%s_edge.png' % self._os
            if self._selenium.desired_capabilities['browserName'] in ['Safari', 'safari']:
                return '_%s_safari.png' % self._os
            if self._selenium.desired_capabilities['browserName'] in ['Firefox', 'firefox']:
                return '_%s_firefox.png' % self._os
        return '.png'

    def get_text_from_element(self, xpath) -> str:
        element = self.__find_element(xpath)

        if element.get_attribute('value') in [None, ""]:
            actual_text = element.text
        else:
            actual_text = element.get_attribute('value')

        return actual_text

    def get_attribute_of_element(self, xpath, attribute) -> str:
        element = self.__find_element(xpath)
        return element.get_attribute(attribute)

    def get_css_attribute_of_element(self, xpath, attribute) -> str:
        element = self.__find_element(xpath)
        return element.value_of_css_property(attribute)

    def __find_element(self, xpath):
        return self._selenium.find_element(By.XPATH, xpath)

    def __find_elements(self, xpath):
        return self._selenium.find_elements(By.XPATH, xpath)

    def __find_shadow_element(self, parent_xpath, shadow_path):
        elem = self._selenium.find_element(By.XPATH, parent_xpath)
        return elem.shadow_cascade_find_element(*shadow_path.split(' ~ '))

    def find_shadow_element_by_xpath_within_host(self, shadow_host: WebElement, debug: bool = False, *args) -> WebElement:
        """Returns an element identified by the given list of XPATH selectors within shadow DOM(s) of the provided host element

            Returns:
            WebElement: returns the element as WebElement
        """
        script: str = 'var result = arguments[0];'
        js_shadow_xpath_template: str = '\n result = document.evaluate("{}", result.shadowRoot.firstChild, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
        for xpath_locator in args:
            script += js_shadow_xpath_template.format(xpath_locator)
        script += '\n return result;'

        if debug:
            print('recursive js shadow xpath evaluator script - ' + script)

        return self._selenium.execute_script(script, shadow_host)

    def find_shadow_element_by_xpath(self, debug: bool = False, *args) -> WebElement:
        """Returns an element identified by the given list of XPATH selectors.
            The first element in the list should be part of the main DOM
            Every other element in the list except the last one should be a shadow DOM host
            The last element in the list is treated as a normal element

            Returns:
            WebElement: returns the element as WebElement
        """
        script: str = 'var result = document.evaluate("{}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'.format(args[0])
        js_shadow_xpath_template: str = '\n result = document.evaluate("{}", result.shadowRoot.firstChild, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
        for xpath_locator in args[1:]:
            script += js_shadow_xpath_template.format(xpath_locator)
        script += '\n return result;'

        if debug:
            print('recursive js shadow xpath evaluator script - ' + script)

        return self._selenium.execute_script(script)

    @staticmethod
    def __validate_style(elem, data_table):
        error_messages = []
        for key, value in data_table.items():
            if key == 'font-family':
                if value.lower() not in elem.value_of_css_property(key).lower():
                    error_messages.append(
                        f'\n{key} not correct. \nActual: {elem.value_of_css_property(key)} \nExpected: {value}')
            else:
                if elem.value_of_css_property(key).lower() not in value.lower():
                    error_messages.append(
                        f'\n{key} not correct. \nActual: {elem.value_of_css_property(key)} \nExpected: {value}')

            assert error_messages.__len__() == 0, f'Element style failed with errors: {"".join(error_messages)}'

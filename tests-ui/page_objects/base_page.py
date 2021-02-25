import re

from pytest_selenium_enhancer import CustomWait
from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self, selenium, base_url):
        self._base_url = base_url
        self._selenium = selenium
        self._os = re.sub(r"[\s]*", "", selenium.desired_capabilities['platformName'].lower()) \
            if 'platformName' in selenium.desired_capabilities else \
            re.sub(r"[\s]*", "", selenium.desired_capabilities['platform'].lower())
        if self._os == 'macos':
            self._os = 'macosx'
        self._device = 'mobile' if self._os in ['android', 'ios'] else 'desktop'
        self._wait = CustomWait(self._selenium)

    def open(self, **kwargs):
        pass

    def is_loaded(self, **kwargs):
        pass
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver


class BrowserActions:

    def __init__(self, driver):
        self._driver: WebDriver = driver

    def get_current_url(self) -> str:
        return self._driver.current_url

    def get_title(self) -> str:
        return self._driver.title

    def get_current_tab_name(self) -> str:
        return self._driver.current_window_handle

    def get_page_source(self) -> str:
        return self._driver.page_source

    def get_number_of_tabs(self) -> int:
        return len(self._driver.window_handles)

    def get_tab_list(self) -> List[str]:
        return self._driver.window_handles

    def switch_to_tab_index(self, index: int):
        tab_name: str = self._driver.window_handles[index]
        self.switch_to_tab(tab_name)

    def switch_to_tab(self, tab_name: str):
        self._driver.switch_to.window(tab_name)

    def close_current_tab(self):
        self._driver.close()

    def close_tab_at_index(self, index: int):
        self.switch_to_tab_index(index)
        self._driver.close()

    def close_tab(self, name: str):
        self.switch_to_tab(name)
        self._driver.close()

    def navigate_back(self):
        self._driver.back()

    def refresh(self):
        self._driver.refresh()

    def resize_to(self, width, height):
        self._driver.set_window_size(width, height)

    def go_to_url(self, url: str):
        self._driver.get(url)

    def go_to_protected_url(self, full_url: str, username: str, password: str):
        https = "https://"
        http = "http://"

        protocol = ""
        if full_url.startswith(https):
            protocol = https
        elif full_url.startswith(http):
            protocol = http

        url = full_url
        if protocol:
            url = full_url.replace(protocol, "")

        self._driver.get(f'{protocol}{username}:{password}@{url}')

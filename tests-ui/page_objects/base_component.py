import re

from pytest_selenium_enhancer import CustomWait


class BaseComponent:

    def __init__(self, selenium, os, device, name=''):
        self._selenium = selenium
        self._os = os
        self._device = device
        self._name = name

        self._wait = CustomWait(self._selenium)

    def is_loaded(self, **kwargs):
        pass

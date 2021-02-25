# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
import logging
from collections import defaultdict
import os
from pathlib import Path
# from utils.env_variables import EnvVariables
from utils.locators import Locators
from utils.utils import initialize_screenshot_dirs
from cucumber_tag_expressions import parse
from step_definitions.steps_given import *
from step_definitions.steps_then import *
from step_definitions.steps_when import *
from step_definitions.steps_custom import *
from webdriver.custom_commands import my_custom_commands

# pytest_plugins = [
#     'pytest_testrail',
# ]

def pytest_configure(config):
    config.option.keyword = 'automated'
    config.option.markexpr = 'not not_in_scope'
    pytest.globalDict = defaultdict()
    pytest.scenarioDict = defaultdict()

def pytest_addoption(parser):
    parser.addoption('--language',
                     action='store',
                     default='en',
                     type=str,
                     help='Application language')
    # parser.addoption('--export_tests_path',
    #                 metavar="str",
    #                 help='Will export tests form given file or directory to TestRail')
    # parser.addoption('--export_results',
    #                  action='store_true',
    #                  help='If false will not publish results to TestRail')
    parser.addoption('--tags',
                     metavar="str",
                     help='Will filter tests by given tags')

def pytest_collection_modifyitems(config, items):
    if 'pytest_testrail_export_test_cases' not in config.option \
        or config.option.pytest_testrail_export_test_cases is False:
        raw_tags = config.option.tags
        if raw_tags is not None:
            for item in items:
                item_tags = [marker.name for marker in item.own_markers]
                if not parse(raw_tags).evaluate(item_tags):
                    item.add_marker(pytest.mark.not_in_scope)

def pytest_sessionstart(session):
    initialize_screenshot_dirs(session.config.rootdir)

def pytest_bdd_before_scenario(request, feature, scenario):
    pytest.scenarioDict = defaultdict()

@pytest.fixture
def selenium(selenium, selenium_patcher, variables):
    my_custom_commands()
    # selenium.delete_all_cookies()
    return selenium

@pytest.fixture
def selenium_generics(selenium) -> SeleniumGenerics:
    return SeleniumGenerics(selenium)

@pytest.fixture
def browser(selenium) -> BrowserActions:
    return BrowserActions(selenium)

@pytest.fixture
def chrome_options(chrome_options, variables):
    if 'headless' in variables['capabilities'] and variables['capabilities']['headless'] == 'True':
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    return chrome_options

@pytest.fixture
def capabilities(capabilities):
    if 'browser' in capabilities and capabilities['browser'] in ['Edge', 'MicrosoftEdge']:
        capabilities['browserstack.edge.enablePopups'] = 'true'
    if 'browser' in capabilities and capabilities['browser'] in ['safari', 'Safari']:
        capabilities['browserstack.safari.enablePopups'] = 'true'
    return capabilities

@pytest.fixture(scope='session')
def language(request):
    config = request.config
    language = config.getoption('language')
    if language is not None:
        return language
    return None

@pytest.fixture(scope='session')
def project_dir(request, pytestconfig) -> str:
    path_str = request.session.config.known_args_namespace.confcutdir
    # the value above is None in some cases(not sure why). so, adding the fallback below
    return path_str if path_str else str(pytestconfig.rootdir)

@pytest.fixture(scope='session', autouse=True)
def locators(project_dir) -> Locators:
    return Locators(f"{project_dir}/locators.json")

@pytest.fixture(scope='session')
def env_variables(project_dir):
    env_vars_file_path = "%s/.local.env" % project_dir
    return EnvVariables(env_vars_file_path)

@pytest.fixture(scope='session')
def log():
    # Get the top-level logger object
    log = logging.getLogger()
    # make it print to the console.
    console = logging.StreamHandler()
    log.addHandler(console)
    return log
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from collections import defaultdict

import pytest
from cucumber_tag_expressions import parse

from step_definitions.test_common import *
from step_definitions.test_assertions import *
from utils.env_variables import EnvVariables


def pytest_configure(config):
    config.option.keyword = 'automated'
    config.option.markexpr = 'not not_in_scope'
    pytest.globalDict = defaultdict()


def pytest_addoption(parser):
    parser.addoption('--language',
                     action='store',
                     default='en',
                     type=str,
                     help='Application language')
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


@pytest.fixture(scope='session')
def language(request):
    config = request.config
    language = config.getoption('language')
    if language is not None:
        return language
    return None


@pytest.fixture(scope='session')
def env_variables(request):
    env_vars_file_path = "%s/.local.env" % request.session.config.known_args_namespace.confcutdir
    return EnvVariables(env_vars_file_path)


from os import environ

import pytest
import requests as requests

from pytest_bdd import when, scenarios

scenarios('../features/demo/get_user.feature', strict_gherkin=False)


@when('I call for <verb> <endpoint>')
def call_api(base_url, verb, endpoint):
    auth_type = pytest.globalDict['auth_type']
    if auth_type == '':
        github_token = ''
    else:
        github_token = environ.get("GITHUB_TOKEN")

    response = requests.get(f'{base_url}{endpoint}', headers={"Authorization": "token %s" % github_token})

    pytest.globalDict['response'] = response

import pytest
from pytest_bdd import given


@given('I am using <auth_type>')
def using_auth_type(auth_type):
    pytest.globalDict['auth_type'] = auth_type

import pytest
from assertpy import assert_that
from pytest_bdd import then


@then('I get <response_code> and <response_message>')
def validate_response(base_url, response_code, response_message):
    response = pytest.globalDict['response']

    assert_that(response.status_code).is_equal_to(int(response_code))
    assert_that(response.text).is_equal_to_ignoring_case(response_message)

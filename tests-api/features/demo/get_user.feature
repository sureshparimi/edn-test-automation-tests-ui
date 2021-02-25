@ID-of-Epic @ID-of-Story @navigation @nondestructive
Feature: Navigation
    Navigation to ComplicatedPage

    @automated
    Scenario Outline: Gets user
        Given I am using <auth_type>
        When I call for <verb> <endpoint>
        Then I get <response_code> and <response_message>
        Examples:
            | auth_type | verb | endpoint | response_code | response_message                                                                    |
            |           | GET  | /user    | 401           | {"message":"Bad credentials","documentation_url":"https://developer.github.com/v3"} |



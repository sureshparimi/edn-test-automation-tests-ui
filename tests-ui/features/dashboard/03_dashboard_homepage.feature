@regression @smoke @automated @nondestructive @EDN002
Feature: Go to websites page from dashboard homepage
    Background: 
        Given the dashboard homepage is displayed

    Scenario Outline: Go to websites page from dashboard homepage
        When the user clicks on websites menu
        When the user clicks on <offering_type>
        Then the user should see websites header on the websites page
        Then the user should see <offering_type> as selected offering type in filters

        Examples:
            | offering_type  |
            | Edison Custom  |
            | Edison Lite    |
            | Edison Legacy  |


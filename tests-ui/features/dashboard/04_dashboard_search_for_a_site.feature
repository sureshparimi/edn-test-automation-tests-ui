@regression @smoke @critical @EDN003 @automated @nondestructive
Feature: Search for a website in the dashboard
    Background: 
        Given the user is on the websites page

    Scenario Outline: Search for a website in the dashboard 
        When the user enters <sitename_value> into sitename field
        When the user clicks the Filter button
        Then the search results contain <sitename_value>
        Then the user clicks on <sitename_value> from the search results

        Examples:
            | sitename_value |
            | sandbox03 |
            | sandbox02 |
            | sandbox |
            
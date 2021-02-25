@regression @smoke @automated @nondestructive @EDN007

Feature: Create change log records
    Background: 
            Given the user logs into the <changelog_site>

    Scenario Outline: Create change log records
        Given the user is on the create change record page
        When  the user publishes a changelog with <title><change_record_Type><event_date><affects><summary><body><notifications><contacts><save_as><revision_log_message>
        Then  changelog is published successfully
        And   email notification should be sent

        Examples:
        |changelog_site|title|change_record_Type|event_date |affects|summary|body|notifications|contacts|save_as|revision_log_message|
        |https://pfmobilechangelog.pfizersite.io/pfizer-login|This is the pytest test title|36|event_date |affects|summary-test|body-test|notifications|contacts|save_as|test_revision_log_message|


@regression @smoke @critical @EDN005 @automated @nondestructive 
Feature: As an Engineering role, I should be able to delete the MTPs for a site on the dashboard

    Background: 
        Given the dashboard homepage is displayed
        
    Scenario Outline: Delete MTPs on the dashboard
        Given existing MTPs available for the <sitename>
        When  the user deletes the MTP
        Then  MTP should not be available on the dashboard

        Examples: 
            | sitename  |
            | sandbox02 |
            | sandbox03 |
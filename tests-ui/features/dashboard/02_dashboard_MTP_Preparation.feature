@regression @smoke @critical @EDN004 @automated @nondestructive @mtps
Feature: Prepare an MTP from the dashboard
        Creates MTPs in preparation state. Stores them in test_data/dashboard_mtp_test_data.json file. Other scenarios will make use of them
    
    Background: 
        Given the dashboard homepage is displayed
        # Given the user cancells the existing MTPs


    Scenario Outline: Prepare an MTP from the dashboard 
        Given the user is on the <sitename> page
        Given the user on the Prepare MTP form
        When  the user fills the MTP form with <mtp_type>,<mtp_date>,<mtp_date_time_zone>,<service_request>,<SCO>,<vendor_assignee>,<manual_verification_text>
        Then  an MTP should be created successfully with Preparation state on <sitename>

        Examples:
            | sitename | mtp_type|mtp_date|mtp_date_time_zone |service_request |SCO |vendor_assignee |manual_verification_text |
            | sandbox02 |1|24/02/2021|Kolkata|987456|parims03|parims03|This MTP is created by pytest automation script.No action is necessary,please ignore it.|
            | sandbox03 |3|24/02/2021|Kolkata|987456|parims03|parims03|This MTP is created by pytest automation script.No action is necessary,please ignore it.|


    Scenario Outline: Advance MTP from Preparation to Ready for deployment state by the site
    When  the user advances MTP of the <site> into Ready for deployment state
    Then   MTP is in Ready for deployment state
    
    Examples:
        |site|
        |sandbox02|
        |sandbox03|

    
    Scenario Outline: Advance MTP from Ready for deployment to Deployment in progress
    When  the user advances MTP of the <site> into Deployment progress state
    Then  MTP is in deployment progress state
    Examples:
        |site|
        |sandbox02|
        |sandbox03|

    Scenario Outline: Verify MTP when MTP is in verification state
    When  the user verifies MTP using verify MTP button
    Then  The Verify MTP button should be enabled
    Examples:
        |site|
        |sandbox02|
        |sandbox03|
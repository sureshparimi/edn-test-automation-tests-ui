# @regression @smoke @automated @nondestructive @EDN005
# Feature: Run a build on custom environment
#     Background: 
#         Given the dashboard homepage is displayed
#         Given the user has <role>

#     Scenario Outline: Go to websites page from dashboard homepage
#         Given the user is on the <Custom_website>
#         When the user clicks on <environment>
#         Then the user should be on <environment>
#         Then user should see <the_build_icon_displayed>
#         When the user clicks on Build icon
#         Then user should be on Build page
#         When the user clicks on Trigger build button
#         Then user should be redirected to <environment> page
#         Then <message> should be displayed indicating triggered build status

#         Examples:
#             | role  | Custom_website|environment |the_build_icon_displayed|message|
#             |Developer|pftest03|Dev|Yes|Yes|
#             ||
#             ||
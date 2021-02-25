# Python Test Automation Boilerplate


## Description:
This is a boilerplate for testing web, PWAs and hybrid apps on Web, iOS & Android.

## Dependencies:
`Python` `pip` `pyenv` `virtualenv`


## Installation Steps
In order to get the tests to run locally, you need to install the following pieces of software.<br />
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

### MacOS
1. Install Homebrew with `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
 1.1. Fix commandline `sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /`
2. Install Pyenv with `brew install pyenv` This is a python version manager.<br />
   Add the following to *~/.bash_profile* 
   ```# Pyenv
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   export PATH="$PYENV_ROOT/shims:$PATH"
   export PATH="$PYENV_ROOT/completions/pyenv.bash:$PATH"
    ```
3. Install python 3.8.2 with `pyenv install 3.8.2`
4. Set python version 3.8.2 to be used globally with `pyenv global 3.8.2`
5. Install virtualenv with `python3 -m pip install --user virtualenv`
6. Create new virtual env with `python3 -m virtualenv .venv`
7. Activate new virtual env with `source ./.venv/bin/activate`
8. Install all project dependencies with `pip install -r requirements.txt`
9. Check python version used with `which python`. <br />
   Shall be `[PROJECT_DIR]/tests/.venv/bin/python`
10. Run the Demo tests included. For more instructions, please see Notes at the bottom of this file.

### Windows / Linux
1. Install GitBash
2. Uninstall any previous python version
3. Install python 3.8.2 using official installation file
4. Install all project dependencies with `pip install -r requirements.txt`

### Installing drivers
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

webdrivermanager Python module is available to facilitate downloading and deploying WebDriver binaries. 

 - Usage example:
  ```
  webdrivermanager chrome -d ./selenium_drivers/
  ```

For more details on how to use webdrivermanager visit [website](https://pypi.org/project/webdrivermanager/)


## Test execution
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

### Local run
 - Chrome Headless example:
  ```
  python -m pytest -v --reruns 1 --reruns-delay 1 --gherkin-terminal-reporter --driver Chrome --driver-path ./selenium_drivers/chromedriver_mac --capability headless True --base-url http://localhost:6006 --variables webdriver/capabilities_web_local.json --variables i18n.json --variables variables.json --tags="visual-regression"
  ```

### Browserstack (BS) Configuration:
Add BrowserStack API credentials to `./.browserstack` file
```
[credentials]
username=TODO
key=TODO
```

**!DO NOT PUSH your credentials into git repo**

### Browserstack (BS) run
1. Start BS local
 - ./scripts/BrowserStackLocal_linux --daemon start --key [BS_API_KEY] --force-local --local-identifier local_testing [UNIQUE_CONNECTION_NAME]
 - See [here](https://www.browserstack.com/local-testing/automate#multiple-local-testing-connections) for more details

2. Run tests on different browsers using the below commands:
 - See [here](https://www.browserstack.com/local-testing/automate#test-localhost-websites) for more details on how to run tests on localhost sites
 - See [here](https://www.browserstack.com/local-testing/automate#test-websites-hosted-private-internal-servers) for more details on how to run tests on private networks and networks behind firewalls
 - For any other details about [BS usage with Python](https://www.browserstack.com/automate/python)
 
Please read BS documentation for more details on configurations:
 - https://www.browserstack.com/automate/python
 - https://www.browserstack.com/app-automate/appium-python

 - Usage example for Windows 10 - Chrome:   
   ```
   ./scripts/BrowserStackLocal_mac --daemon start --force-local --key [BS_KEY] --local-identifier local_testing_01
   -v --reruns 1 --reruns-delay 1 --gherkin-terminal-reporter --driver Browserstack --capability browser 'Chrome' --capability build 'eucrisahcpcom-qa' --capability browserstack.localIdentifier local_testing_01 --base-url https://eucrisahcpcom-qa.dev.pfizerstatic.io --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags="(not visual-regression and not pages-visuals) and not ie-required and not production-required and not cf-required and not mobile"
   ```
 
### Tests filtering
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

cucumber-tag-expressions Python module is available to facilitate filtering of Scenarios based on tags.
 - Usage example:
  ```
  --tags=""
  ```

For more details on how to use cucumber-tag-expressions visit:
 - [website](https://pypi.org/project/cucumber-tag-expressions/)
 - [pytest-bdd](https://pytest-bdd.readthedocs.io/en/latest/#organizing-your-scenarios)  
 - [cucumber-tags](https://cucumber.io/docs/cucumber/api/#tags)


## TestRail Configuration
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

pytest-testrail-client Python module is available to facilitate exporting of Test Cases and Test Results.

Append the following to pytest.ini file:
  ```
  [pytest-testrail-client]
  pytest-testrail-client = True / False
  testrail-url = [URL of TestRail instance]
  testrail-email = [email [of user to be used for communication]]
  testrail-key = key [of user to be used for communication]
  testrail-project-id = [project id to which the data is sent]
  jira-project-key = [Jira project key for integration with Jira]
  ```

For more details on how to use pytest-testrail-client visit [website](https://pypi.org/project/pytest-testrail-client/)

**!DO NOT PUSH your credentials into git repo**
  
### Export test cases to TestRail
- From project root directory
- Run: 
  **To import/update test Scenarios for ALL feature files**
  - ```python -m pytest -v --pytest-testrail-export-test-cases --pytest-testrail-feature-files-relative-path "features"```

  **To import/update test Scenarios for INDIVIDUAL .feature file**
  - ```python -m pytest -v --pytest-testrail-export-test-cases --pytest-testrail-feature-files-relative-path "features/[DIR_NAME]/[FILE_NAME].feature"``` 

#### Implementation details
- Each *.feature* file is a product functionality
  - Unique key is the pair of **Feature Name - Functionality** + **feature description**
  ```gherkin
   Feature: Create User - Email registration
     As an anonymous user
     I open the app for the first time
     I want to be able to register with email
  ```
  - It will create a new **Test Suite** for each unique *Feature Name* file published
  - It will create a new **Section** within the **Test Suite** for each unique **Functionality**
  - If **test suite** was previously imported it will update all the tests within
- Each *Scenario* is a TestRail *Case*
  - Unique key is pair of **scenario name** + **data set** (The Examples line in json format)
  ```gherkin
  Scenario: Add two numbers
    Given I have powered calculator on
    When I enter <50> into the calculator
    When I enter <70> into the calculator
    When I press add
    Then The result should be <120> on the screen
    Examples:
      | number_1 | number_2 | result |
      | 10       | 20       | 30     |
      | 50       | 60       | 120    |
  ```
  - It will create a new **case** for each *Scenario* published
  - If **case** was imported it will update it with latest changes
  - Scenario *tags*:
    - **@automation** = **case** is automated
    - **@JIRA-1** = **case ref** to Jira ticket (the feature ticket)
    - **@smoke** / **@sanity** / **@regression** / **None** = **case priority** Critical / High / Medium / Low
    - **@market_us** = **case** is for USA market
    - **@not_market_ca** = **case** is not for Canada market
  - *Steps* are imported as separate ones with empty *Expected Results*
  - Do **NOT** use *And* and *But* keys as it will fail the match of test cases during results publishing
  
## Publish test results to TestRail
### Create Test Plan in TestRail
- You have to manually create the test plan in TestRail
  - Naming convention: [JIRA_PROJECT_NAME]_[SPRINT_NAME]_[MARKET] - MARKET only if applied
    - eg: *JIRA_Sprint-1_us* or *JIRA_Regression_us*

### Test run details in `project`
  - ```--pytest-testrail-export-test-results --pytest-testrail-test-plan-id 3445 --pytest-testrail-test-configuration-name "Windows 10 - Chrome"``` 
  - Info
    - **pytest-testrail-test-plan-id** = **mandatory**, TestRail Test Plan id (can be found in URL.
    - **pytest-testrail-test-configuration-name** = **mandatory**, TestRail project configurations
      - Read more about [TestRail Test Plans and Configurations](https://www.gurock.com/testrail/videos/test-plans-configurations)


## Code Quality
Linting = the process of analyzing the source code to flag programming errors, bugs, stylistic errors, and suspicious constructs.

**IMPORTANT:** Lint your code before any commit

  - Go to _tests_root_ folder
  - Run `pylint ./**/**.py`
  - There should be only one Error: `E:  4, 0: invalid syntax (<string>, line 4) (syntax-error)`
    - This is due to a _pylint_ issue: root files or folders cannot be ignored from linting. Will follow the fix
    - A rating above 9.00 should be kept for the code


## Notes
### Tips and Tricks
On Pycharm: <br />
To benefit from autocomplete, please set *tests* folder as **Sources Root**
 - Right click on *tests*
 - Click on *Mark Directory As*
 - Click on *Sources Root*
 
 You should see that the Folder Icon has now changed colors to blue. That means it was successfully marked as Sources Root.


************************************************
Version 2.1 - Python Test Automation Boilerplate
************************************************

.. contents:: **Table of Contents**
    :depth: 2

Description
===========
Version 2.1 is the supported version of the Python Test Automation Boilerplate.

It contains contains specific third party features to enable you to create tests within your local projects. See Features below, for full details.

Installation
============

Installing for the First Time
-----------------------------

- To clone v2.1 of this boilerplate, see `DSE Test Guild Knowledge Base`_.

- To customize installation using an advanced process, see `for UI testing`_ and `for API testing`_

Upgrading From Version 2.0 to 2.1
---------------------------------

See `Upgrading your version of the boilerplate`_


Features
========

- Powerful test library to to support complex functional testing
   - Using `pytest`_
- `Cucumber`_ integration to employ Behavior-Driven Development (BDD)
   - Using `pytest-bdd`_
- 100+ predefined Cucumber StepDefinitions
   - Using `predefined_steps`_
- Easy handle flaky tests by re-running them
   - Using `pytest-rerunfailures`_
- Selenium integration, industry de-facto in web automation
   - Using `pytest-selenium`_
- Easy manage webdriver versions on your machine
   - Using `webdrivermanager`_
- Enhance Selenium functionality with custom commands. Take full page screenshots on multiple browsers/devices. Screenshots comparison and Visual Regression testing
   - Using `pytest-selenium-enhancer`_
- Multi-Browser and Multi-device support integration
   - Using `BrowserStack`_
- Mobile devices testing capabilities
   - Using `Appium`_
- Simple assertions using fluent API
   - Using `assertpy`_
- TestRail integration
   - Using `pytest-testrail-client`_
- API testing with an elegant and simple HTTP library
   - Using `requests`_

_NOTE:_ Please read inner README.md files for more technical details.

Contributing
============

If you want to contribute to this project, see Contributing_

Resources
=========

- `ChangeLog`_
- `Issue Tracker`_
- `GitHub Code`_

.. [#f1] Git for Windows provides a BASH emulation used to run Git from the command line. .NIX users should feel right at home, as the BASH emulation behaves just like the "git" command in LINUX and UNIX environments.

.. _Digital Solutions & Enablement: https://teams.microsoft.com/l/team/19%3a983bec845cee4b08a1023f7b8ece093e%40thread.skype/conversations?groupId=5f70f02d-fc1d-41d0-ab99-2043005d8107&tenantId=7a916015-20ae-4ad1-9170-eefd915e9272
.. _DSEQualityTest: https://pfizer.sharepoint.com/sites/DSEQualityTest
.. _for UI testing: https://github.com/pfizer/python-test-automation-boilerplate/blob/release/2.1/tests
.. _for API testing: https://github.com/pfizer/python-test-automation-boilerplate/blob/release/2.1/tests-api
.. _DSE Test Guild Knowledge Base: https://pfizer.sharepoint.com/sites/DSEQualityTest/SitePages/Test-Guild-Knowledge-Base.aspx
.. _Upgrading your version of the boilerplate: https://pfizer.sharepoint.com/sites/DSE-TestGuild/SitePages/Upgrading-your-version-of-the-boilerplate.aspx

.. _v2.0: https://github.com/pfizer/python-test-automation-boilerplate/tree/release/2.0
.. _v2.1: https://github.com/pfizer/python-test-automation-boilerplate/tree/release/2.1

.. _pytest: http://pytest.org
.. _installation_scripts.zip: https://github.com/pfizer/python-test-automation-boilerplate/blob/release/2.1/installation_scripts.zip

.. _Setting up the Pfizer test environment within Windows: https://pfizer.sharepoint.com/sites/DSE-TestGuild/SitePages/Setting-up-the-Pfizer-test-environment-within-Windows.aspx

.. _Cucumber: https://cucumber.io/
.. _pytest-bdd: https://pytest-bdd.readthedocs.io/en/latest/
.. _predefined_steps: https://github.com/pfizer/python-test-automation-boilerplate/blob/release/2.1/docs/GHERKIN_STEPS.rst
.. _pytest-rerunfailures: https://pypi.org/project/pytest-rerunfailures/
.. _pytest-selenium: https://pytest-selenium.readthedocs.io/en/latest/
.. _webdrivermanager: https://pypi.org/project/webdrivermanager/
.. _pytest-selenium-enhancer: https://pypi.org/project/pytest-selenium-enhancer/
.. _Appium: http://appium.io/docs/en/about-appium/intro/?lang=en
.. _assertpy: https://github.com/assertpy/assertpy
.. _pytest-testrail-client: https://pypi.org/project/pytest-testrail-client/
.. _requests: https://requests.readthedocs.io/en/master/

.. _Contributing: https://github.com/pfizer/python-test-automation-boilerplate/blob/master/docs/CONTRIBUTING.rst
.. _BrowserStack: https://browserstack.com

.. _ChangeLog:  https://github.com/pfizer/python-test-automation-boilerplate/blob/master/docs/CHANGELOG.rst
.. _Issue Tracker: https://github.com/pfizer/python-test-automation-boilerplate/issues
.. _GitHub Code: https://github.com/pfizer/python-test-automation-boilerplate/tree/release/2.1

----

Ruby Test Edit

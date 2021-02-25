**********************
Implemented Test Steps
**********************

.. contents:: **Table of Contents**
    :depth: 2


Usage examples
==============

Examples can be found here: **./features/codeless**

Available steps
===============

Given Steps
-----------
Describe an initial context

- I set browser resolution to '.*' per '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "width", "(str:)", "Valid browser width. Eg: 1367, 1980"
       "height", "(str:)", "Valid browser 768, 1020"

|

- I navigate to page <url_path>
- I navigate to page '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "url_path", "(str:)", "Part of an URI - scheme:[//authority]path[?query][#fragment], as described |wiki_url|_"

|

- I navigate to external page <url>
- I navigate to external page '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "url", "(str:)", "URI = scheme:[//authority]path[?query][#fragment], as described |wiki_url|_"

When Steps
----------
Describe an event (When steps)

- I click on <xpath>
- I click on '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "xpath", "(str:XPath)", "Valid XPath selector, as described |wiki_xpath|_"

|

- I click on shadowElement <element_path>
- I click on shadowElement '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "element_path", "(dict:{ parent_xpath:XPath, shadow_path:CSS Selector })", "Dictionary containing keys _parent_xpath_ and _shadow_path_ , valid XPath and CSS selectors as described |wiki_xpath|_ and |wiki_css|_"

|

- I hover over <xpath>
- I hover over '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "xpath", "(str:XPath)", "Valid XPath selector, as described |wiki_xpath|_"

|

- I hover over shadowElement <element_path>
- I hover over shadowElement '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "element_path", "(dict:{ parent_xpath:XPath, shadow_path:CSS Selector })", "Dictionary containing keys _parent_xpath_ and _shadow_path_ , valid XPath and CSS selectors as described |wiki_xpath|_ and |wiki_css|_"


Then Steps
----------
Describe an expected outcome (Then steps)

- Page <page_url> is loaded
- Page '.*' is loaded

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "url", "(str:)", "URI = scheme:[//authority]path[?query][#fragment], as described |wiki_url|_"

|

- Page scroll position is '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "scroll_position", "(int:)", "Valid browser vertical scroll position. Eg: >=0"

|

- Page visual regression is correct:.*

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "data_table", "(dict:{ parent_xpath:XPath, shadow_path:CSS Selector })", "Dictionary containing keys _page_name_,  _start_, _all_, _end_. _page_name_ is string representative to the screenshot taken. _start_, _all_, _end_ are valid XPaths selectors representing elements you want to make transparent on screenshot (Useful when you have to deal with dynamic content)."

|

- Element <xpath> state should be <state>
- Element '.*' state should be '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "xpath", "(str:XPath)", "Valid XPath selector, as described |wiki_xpath|_"
       "state", "(str:)", "displayed|hidden"

|

- Element <xpath> text should be <expected_text>
- Element '.*' text should be '.*'

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "xpath", "(str:XPath)", "Valid XPath selector, as described |wiki_xpath|_"
       "state", "(str:)", "Text that needs to be checked within an element"

|

- Element '.*' style should be:.*

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "xpath", "(str:XPath)", "Valid XPath selector, as described |wiki_xpath|_"
       "data_table", "(dict:{ css_attribute_key:str })", "Dictionary containing keys _css_attribute_key_. _css_attribute_key_ as pairs of key:value representing attribute name and computed value"

|

- ShadowElement style should be:.*

   *Parameters*

   .. csv-table::
       :header: "Name", "Type", "Details"
       :widths: 20, 30, 50

       "data_table", "(dict:{ parent_xpath:XPath, shadow_path:CSS Selector, css_attribute_key:str })", "Dictionary containing keys _parent_xpath_, _shadow_path_ , _css_attribute_key_. Valid XPath selector as described |wiki_xpath|_. _css_attribute_key_ as pairs of key:value representing attribute name and computed value"


.. |wiki_url| replace:: here
.. _wiki_url: https://en.wikipedia.org/wiki/URL

.. |wiki_xpath| replace:: here
.. _wiki_xpath: https://www.w3schools.com/xml/xpath_intro.asp

.. |wiki_css| replace:: here
.. _wiki_css: https://www.w3schools.com/cssref/css_selectors.asp

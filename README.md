# web_scraping_tool

#### Overview

> Web scraping tool includes CLI for communication with users and prints the desired information from websites in JSON format.
A command line tool takes two required input parameters for a page to be scraped and sport to be filtered and optional parameters. If a user enters an optional parameter - html element, he must also specify html attribute. Html attribute has three options that are mutually exclusive. After download the source code of the project you run code with input format: 
python scrape.py url sport [--html_elem {table, tr, td}][--element_id ELEMENT_ID | --element index ELEMENT_INDEX | --element_class ELEMENT_CLASS ] 

#### Example

> python scrape.py http://www.goseattleu.com/StaffDirectory.dbml "Track and Field" --html_elem tr --element_class sport-name

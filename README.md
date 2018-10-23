# web_scraping_tool

#### Overview

> Web scraping tool includes CLI for communication with users and prints the desired information from websites in JSON format.
A command line tool takes two required input parameters for a page to be scraped and sport to be filtered and optional parametrs. If a user enters an optional  parameter html element, he must also specify html attribute. Html atribute has three options that are mutually exclusive. After download the source code of the project you run code with input format: 
python scrape.py url sport --html_elem = element [--element_id |--element class |--element_index ] = value 

#### Example

> python scrape.py http://www.goseattleu.com/StaffDirectory.dbml "Track and Field" --html_elem tr --element_class sport-name

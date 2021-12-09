# Bazos scrapy scraper
Scrapy project to scrapy all advertisements on Bazos page (famous czech and slovak advertisement site). project is made for fun, to improve web scraping skills.

Requirements
---

- [Poetry](https://python-poetry.org/) python package manager (will install all dependencies, like Scrapy...)

Instalation
---
```
poetry install
```

## Usage
To run scrapy from virtual environment provided by poetry  
```
poetry run task scrapy [commands]
``` 
or if you want scrape advertisements into bazos.json you can use   
```
poetry run task crawl_json
```
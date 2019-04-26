# Log Analysis
Log Analysis is a reporting tool used to display the information regarding most popular articles, most popular article authors of all time, Statistical information like "On which day more than 1% of requests leads to errors".
# Quickstart

## Install
* Make sure vagrant and virtual machine is up and running. After its installation, execute the code below to get the **news** database :
```
psql -d news -f newsdata.sql

```
* Execute _view_ code below:
```
SELECT articles.slug || '%'::text AS match,articles.author,                   articles.title,articles.slug,articles.lead,articles.body,
articles."time",articles.id  FROM articles;
```

* Execute _Python Main_ code below to start the server:
```
Python Report.py

```
* Reporting tool can be accessed on browser [here](http://localhost:8000/)

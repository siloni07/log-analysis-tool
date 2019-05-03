# Log Analysis
Log Analysis is a reporting tool based on **python** which will display the information regarding most popular articles, most popular article authors of all time, Statistical information like "On which day more than 1% of requests leads to errors" for  data fed to it from **POSTGRESQL** Database.

## Quick-Installation
* Virtual Machine Installation :- Clone the [project](https://github.com/siloni07/log-analysis-tool) Install [Vagrant](https://www.vagrantup.com/downloads.html) and [Virtual Machine set-up](https://www.oracle.com/technetwork/server-storage/virtualbox/downloads/index.html)
In Git Bash run the following command to make your virtual machine up and running
```
cd log-analysis-tool/
vagrant up
```
Please note it may take sometime for "vagrant up" command to get completed. Now, The system is ready to use. Use _Vagrant ssh_ command afterwards to fastly configure your virtual machine.

## Install
* Execute the following command to get data of newsdata.sql in  psql database:
```
psql -d news -f newsdata.sql

```
* Execute _view_ code below:
```
create view log_view as (select substring(path,10) as path_new,status,time,id from log);

```

* Execute _Python Main_ code below to start the server:
```
Python Reportdb.py

```
* Once Above Steps are performed. Server is ready to listen any request on port 8000. Feed the request from browser by clicking [here](http://localhost:8000/). In the console, data of the reporting tool will be published and an **output.txt** file will be generated in your project directory. If you want to stop the server press (Clt + C).

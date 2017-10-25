# Kanban.py
Simple [Kanban](https://en.wikipedia.org/wiki/Kanban_(development)) Server written in Python using web.py. Styling with [materializecss](https://materializecss.com/).

## About Kanban
Kanban is a software development technique that orders task in different categories. In this pre-release version, there are only three static ones: To-Do, Work in Progress and Done. 
The individual tasks can be moved between them, eventually by drag and drop.

It is basically a glorified To-Do list.

## Requirements

### Linux
Requirements for Arch Linux or any other Distro that uses Python 3 by default:
```bash
pip install web.py==0.40.dev0
pip install tinydb
```
Requirements for Debian, Ubuntu etc.:
```bash
pip3 install web.py==0.40.dev0
pip3 install tinydb
```
### Windows
Requirements are:
* [Python 3](https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe)
* PIP (comes with Python)
* Some modules, installed through pip:
```bash
pip3 install web.py==0.40.dev0
pip3 install tinydb
```
I would advise you to add Python to your PATH on installation, otherwise there could be problems installing these packages.

## How to start
Run main.py with Python 3. The webserver is started on Port 8080.

Please report any bugs you find.

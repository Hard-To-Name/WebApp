# UCI Course Lookup

An web application for UCI students to look up course status and schedule courses. More functions will be in the "Toolbox" section.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Tools / Libraries Used

MySQL
Git
Bootstrap
Angular JS
JQuery

Python Libraries:

```
Django, MySQLdb, requests
```

### Installation (on server)

```
1. Download or clone this repository on computer
2. Install tools / libraries above
3. Change the connection information of MySQL Database in /project/app/Websoc.py and /project/app/views.py
4. Run /project/app/Websoc.py to generate local database (first call init() then update_db())
5. Open command line, cd to /project, and execute "manage.py runserver"
```

Example Database:
![](/samples/MySQL.png "")

Example Webpage:
![](/samples/Index.png)
![](/samples/Status.png)

## Authors

* **Ran Duan**
- Webpage style designed by Jonathan Klughertz

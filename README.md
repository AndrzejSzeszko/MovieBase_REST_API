# MovieBase_REST_API
My first Django REST API

### Disclaimer 1
This project is based on code delivered by CodersLab team.

### Disclaimer 2
Following set up steps are valid for Ubuntu 16.04 and higher. If you use some other distro, there could be need to use different commands.

## Prerequisites
Check if there is Postgres installed on your machine:
```
$ psql --version
```
If don't, install it:
```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get -y install postgresql-10
```
If above commands didn't succeed, it means that your distro's repos don't have Postgres included. You need to add Postgres' repo to the list of used repos (follow this steps: https://wiki.postgresql.org/wiki/Apt) and run above commands once again.

Log in as user named "postgres" and create new database called "moviebase":
```
$ sudo -u postgres -i
$ createdb moviebase
```

Access any database (eg. just created "moviebase") and set password "coderslab" for user named "postgres":
```
$ psql moviebase
# \password postgres
```

Leave psql and return to your regular user account:
```
# \q
$ exit
```

## Setting up project
Navigate to directory you want project to be placed, and create local copy of repo on your machine using git:
```
$ cd path/to/directory/you/want/to/place/project/in
$ git clone https://github.com/AndrzejSzeszko/MovieBase_REST_API.git
```
or download and unzip compressed version (button "clone or download" -> "download zip" on project's main page).

Navigate to directory that contains "manage.py" file:
```
$ cd path/to/directory/that/contains/metioned/file
```
Populate database with project's tables:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Create superuser:
```
$ python manage.py createsuperuser
```
Run server locally:
```
$ python manage.py runserver
```
At this moment all endpoints are accessible but there's nothing to behold, because database is empty. You can populate it relatively painlessly using Django Admin that you can access via browser by visiting 127.0.0.1/admin/ page and using superuser credentials to log in.

## Endpoints examples:
Get all movies (method: GET), create new movie (method: POST):
```
/movies/
```
Get (GET), update (PUT) and delete (DELETE) particular movie:
```
/movies/movie_id/
e.g. /movies/12/
```
Get all cinemas (GET), create new cinema (POST):
```
/cinemas/
```
Get (GET), update (PUT) and delete (DELETE) particular cinema:
```
/cinemas/cinema_id/
e.g. /cinema/11/
```
Get (GET), update (PUT) and delete (DELETE) particular cinema, but in "movies" key show only movies screened within nearest 30 days:
```
/cinemas_current_movies/cinema_id/
e.g. /cinemas_current_movies/11/
```
Get all screenings (GET), create new screening (POST):
```
/screenings/
```
Get all screenings with given cinema name (GET), create new screening (POST):
```
/screenings/?cinema__name=xxx/
e.g. /screenings/?cinema__name=Femina/
```
Get all screenings with given movie title (GET), create new screening (POST):
```
/screenings/?movie_title=yyy/
e.g. /screenings/?movie_title=Arrival/
```
Get all screenings with given cinema name and movie title (GET), create new screening (POST):
```
/screenings/?movie_title=yyy&cinema__name=xxx/
e.g. /screenings/?movie_title=Arrival&cinema__name=Femina/
```
Get (GET), update (PUT) and delete (DELETE) particular screening:
```
/screenings/screening_id/
e.g. /screenings/11/
```

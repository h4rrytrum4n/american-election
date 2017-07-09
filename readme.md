# DBS Project: Data Mining und Visualisation
## Introduction
Projektziel 


Das Ziel des Projektes, ist die Entstehung einer Web Anwendung. Sie soll dabei Daten aus dem Datensatz american-election in geeigneter Form, visuell darstellen sowie das Abfragen von Informationen ermöglichen. 

Das sekundäre Ziel ist dabei, das Auseinandersetzen mit relationale Datenbanken und deren Anwendung. 


Des Weiteren ist der Weg ebenso ein Ziel, welcher sich aus folgenden Punkten zusammen setzt. 

* Phase 1: 
Hierbei liegt der Fokus auf der Festlegung der zu implementierenden Features sowie das Entwerfen des Konzeptes für das Datenmodell. 

* Phase 2: 
Erstellung des Datenbankschemas sowie die Aufbereitung und das Pflegen der Daten. Des Weiteren folgt Einbindung in den Webserver.

* Phase 3:
Bestimmung der Datenabhängigkeit sowie dessen visuelle Darstellung.

Das Team in der alphabetischen Reihenfolge:

* Adrian Gruszczynski (Informatik Bachelor)

* Pit Ronk (Mathematik Bachelor)

* Remi Toudic (Mathematik Master)

## Getting started
Clone Repo
```bash
git clone https://gitlab.spline.inf.fu-berlin.de/h4rrytrum4n/DBS_PR
```

### Requirements

Make sure Python 3, Postgres and autoenv is installed
```bash
brew install python3
brew install Postgres
brew install autoenv
```
### Install dependencies
```bash
pyvenv venv
source venv/bin/activate
pip3 install psycopg2
```
## Database setup:

```bash
# start Postgres
brew services start postgresql

# create database
createdb election

# create tables
psql postgres -h localhost -d election
```
```sql
CREATETABLE tweet (tweet id serial primary key, handle varchar(20) NOT NULL, body varchar(200) NOT NULL,
time timestamp NOT NULL, retweet count int , favorite count int);
CREATETABLE hashtag(hash id serial primary key, tweet id int , text varchar(100) NOT NULL) ;
```
### Import data 
```bash
# go to it02/src directory
cd it02/src
# careful the scripts have been written in python 2.7
python clean_data.py
python import_data.py
```

### Do the migrations and make sure you have sourced the env variables
```bash
source .env
./manage.py migrate
./manage.py runserver
```


# Description
This is the codebase for vending-machine-api using flask framework in python

Dependencies needed:

python

pip

flask

flask_sqlalchemy

flask_cors

flask_jwt_extended

marshmallow_mysqlalchemy

mysqlclient

flask-mysqldb


# Files

## manage.py (run this to start the application)

This is the file that runs the application. It resides in the root directory with the app folder.

Imports the database and create_app() from app directory.

Creates the database using create_all().

Runs the app.


## app/

This is the directory that has the elements of the app

## init.py

Declares instances of database, marshmallow for serialization and deserialization and jwt manager to handle session authentication.

Initializes the function create_app() which performs the necessary initializations and imports for the app to run.

## config.py (database settings here)

Config class that contains configurations for mySQL database using SQLAlchemy and jwt_secret_key needed for jwt token generation.

Contains configurations for logging.

## user/ and product/

These directories contain the model, schema and view for user and product respectively.


## services/

This directory has two files userservices and productservices which manage interaction with each table in the  database respectively.

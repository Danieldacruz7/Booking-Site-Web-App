# Booking-Site-Web-App
A web application that allows artists and venues to display upcoming and past shows at various venues. 

![Fyyur Home Page](./Screenshots/Fyyur%20Home%20Page.jpg)

## Table of Contents

1. Project Motivation
2. Installations
3. File Descriptions
4. How to Interact with the Project

## Project Motivation:

Fyyur is a web application that artists and venues can let the world know all the events they are taking part in. It is a convienant way for fans to see where their favorite artist will be performing. 

The web application uses ORM for the backend and all changes made to the database are tracked using migrations. The frontend incorporates HTML and CSS templates for the user interface. 

## Installations:

The required installations include: 
- babel
- python-dateutil
- flask-moment
- flask-wtf
- flask_sqlalchemy

However, simply run the following command to download libraries: 

```
pip install -r requirements.txt
```

## File Descriptions

The project includes the main progam, app.py, which is used to run the backend of the web application. 

The frontend can be was built using various templates in HTML and CSS, which can be found in the templates folder. 

The database changes are being tracked and saved within the migrations folder. The migrations are carried out by Flask-Migrate. 

## How to Interact with the Project
By running the app.py program, the application will be run as a Flask application. The application can be run on a local machine or hosted on a site such as Heroku. 


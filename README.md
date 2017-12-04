# Getting started with Django on Google Cloud Platform on App Engine Standard

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google App Engine Standard Environment. It uses the 
[Writing your first Django app](https://docs.djangoproject.com/en/1.9/intro/tutorial01/) as the 
example app to deploy.


# Tutorial
See our [Running Django in the App Engine Standard Environment](https://cloud.google.com/python/django/appengine) tutorial for instructions for setting up and deploying this sample application.
#Rachit Tibrewal
For connecting to cloud sql proxy use the command
>./cloud_sql_proxy -instances="webtestgen:asia-south1:testdata01"=tcp:3306
before running gcloud app deploy
always run
python manage.py makemigrations
python manage.py makemigrations polls
python manage.py migrate
python manage.py collectstatic

To run the python shell in the django environment settings
use
python manage.py shell


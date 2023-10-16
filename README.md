# Home Test

Restaurant's python backend

This repository contains the code for the backend in Python,
it uses Django as ORM

to run:

- copy .env-example to .env
- Edit .env with your settings
- Install requirements:
    * pip install -r requirements.txt
- Make migrations:
    * python manage.py makemigrations
    * python manage.py migrate
- Run: python manage.py runserver
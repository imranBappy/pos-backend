#!/bin/bash
echo "Running Django project setup..."
python3 manage.py makemigrations clients
python3 manage.py migrate clients
python3 manage.py makemigrations outlet
python3 manage.py migrate outlet
python3 manage.py makemigrations accounts
python3 manage.py migrate accounts
python3 manage.py makemigrations kitchen
python3 manage.py migrate kitchen
python3 manage.py makemigrations product
python3 manage.py migrate product
python3 manage.py migrate

python3 manage.py createadmin --email=admin@gmail.com --password=pass123

python3 manage.py runserver

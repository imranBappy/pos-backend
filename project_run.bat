@echo off
py manage.py makemigrations clients
py manage.py migrate clients
py manage.py makemigrations outlet
py manage.py migrate outlet
py manage.py makemigrations accounts
py manage.py migrate accounts
py manage.py makemigrations kitchen
py manage.py migrate kitchen
py manage.py makemigrations product
py manage.py migrate product
py manage.py migrate

py manage.py createadmin --email=admin@gmail.com --password=pass123

py manage.py runserver

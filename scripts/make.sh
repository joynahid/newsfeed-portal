#!/bin/bash

python manage.py makemigrations
python manage.py migrate

./manage.py shell < /scripts/startup.py
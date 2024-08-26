#!/bin/bash

python manage.py createsuperuser
python manage.py createusers
python manage.py createresources
python manage.py createprofiles
python manage.py createassignments


#!/bin/bash

# List of apps to create
APPS=("accounts" "assignments" "events" "group_production" "individual_production" "miscellaneous_production" "reports_and_remarks" "resources")

for APP in "${APPS[@]}"
do
	python manage.py startapp $APP
done


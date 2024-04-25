#!/bin/bash

# Set environment variable
export DJANGO_SUPERUSER_PASSWORD='root'

# Create superuser
python ./manage.py createsuperuser --no-input --username=root --email "ruslanpopov1512@gmail.com"

commands=(
    "add_groups"
    "add_users"
)

# Execute commands
for cmd in "${commands[@]}"; do
    python ./manage.py "$cmd"
done

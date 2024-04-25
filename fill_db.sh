#!/bin/bash

commands=(
    "makemigrations"
    "migrate"
    "add_faculties"
    "add_specialities"
    "add_educational_programs"
    "add_offers"
    "add_persons"
    "add_accepted_offers"
    "add_documents"
)

for cmd in "${commands[@]}"; do
    python ./manage.py "$cmd"
done

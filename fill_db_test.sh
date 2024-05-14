#!/bin/bash

commands=(
    "add_specialities"
    "add_educational_programs"
    "add_offers"
    "add_persons"
    "add_accepted_offers"
)

for cmd in "${commands[@]}"; do
    python ./manage.py "$cmd"
done

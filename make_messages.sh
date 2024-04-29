#!/bin/bash

langs=(
    "en"
    "uk"
)

for lang in "${langs[@]}"; do
    django-admin makemessages -l "$lang"
done

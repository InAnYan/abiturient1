pip install -r requirements.txt
python ./manage.py collectstatic --no-input
python ./manage.py migrate
python ./manage.py add_faculties
python ./manage.py add_dnu_2024
python ./manage.py add_documents
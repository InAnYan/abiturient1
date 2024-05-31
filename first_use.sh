pip install -r requirements.txt
python ./manage.py collectstatic --no-input
python ./manage.py migrate
bash add_users.sh
python ./manage.py add_faculties
# python ./manage.py add_documents
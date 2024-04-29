pip install -r requirements.txt
python ./manage.py collectstatic --no-input
python ./manage.py migrate
bash fill_db.sh
bash add_users.sh
pip install -r requirements.txt
python ./manage.py collectstatic --no-input
bash fill_db.sh
bash add_users.sh
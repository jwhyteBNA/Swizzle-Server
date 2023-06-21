#!/bin/bash
# chmod u+x ./seed_database.sh
# ./seed_database.sh

rm -rf swizzleapi/migrations
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations swizzleapi
python3 manage.py migrate swizzleapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata mixologists
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata recipes
python3 manage.py loaddata comments
python3 manage.py loaddata recipe_tags
python3 manage.py loaddata subscriptions

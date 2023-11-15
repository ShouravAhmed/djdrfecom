# packages

Django
python-dotenv

djangorestframework

djangorestframework-simplejw
django-cors-headers

pytest==7.2.0

# commands

python3.10 -m venv .venv
source .venv/bin/activate
deactivate

django-admin startproject djdrfecom

./manage.py runserver

from django.core.management.utils import get_random_secret_key

python3.10 -m pip install --upgrade pip
pip3.10 install -r requirements.txt
 
python manage.py startapp app_name

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

python manage.py createsuperuser

pip freeze > requirements.txt



# Git & Github

*create a new repository on the command line*
```
echo "# DJEcom" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ShouravAhmed/DJEcom.git
git push -u origin main
```

*push an existing repository from the command line*
```
git remote add origin https://github.com/ShouravAhmed/DJEcom.git
git branch -M main
git push -u origin main
```

*default branch name change*
```
git branch -m main dev
git fetch origin
git branch -u origin/dev dev
git remote set-head origin -a
```
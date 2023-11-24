# packages

Django==4.1
django-cors-headers==4.3.0
django-redis==5.4.0
django-rest-swagger==2.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
drf-spectacular==0.26.5
drf-yasg==1.21.7
python-dotenv==1.0.0
redis==5.0.1
requests==2.31.0

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

./manage.py spectacular --file schema.yml

# Git & Github

*create a new repository*
```
echo "# DJEcom" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ShouravAhmed/DJEcom.git
git push -u origin main
```

*push an existing repository*
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
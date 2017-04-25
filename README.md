# Blog
My blog using py3, Django1.9. Checkout how it works: [bigborg.top](http://www.bigborg.top)

# Installation
## Step1: Virtual Environment  
clone the repository, create a virtual env with all dependencies installed.

```buildoutcfg
git clone https://github.com/BigBorg/Blog
cd Blog/Blog
conda create -n web3 -f condarequirement python=3.6
source activate web3
```

## Step2: Configuration  
**db_password.txt** and **secret.txt** are required to be in the Blog directory ( the same directory where **manage.py** is).  
secret.txt stores a randomly generated key used as SECRET setting for django.  
db_password.txt is acutally DATABASES variable dumped by json package. You could use the following string but remember to put in your setting.
```buildoutcfg
{"default": {"ENGINE": "django.db.backends.mysql", "NAME": "your_database_name", "USER": "your_db_username", "PASSWORD": "Your password"}}
``` 

## Step3: Mysql Database  
Remember to create database and database user in mysql.

## Step4: Deploy or Debug  
To debug just run **python manage.py runserver**. For deployment, I recommend gunicorn and nginx. Note that you need to set up nginx to serve static and media files. This is important! Don't use django to serve static files.
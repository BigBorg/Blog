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
Go to the file Blog/Blog/private_settings.py and customize your setting. The variables are self-explanatory.

## Step3: Mysql Database  
Remember to create database and database user in mysql.

## Celery
You need to start celery worker process so that the blog could send activation email asynchronously.
```buildoutcfg
celery -A Blog worker
```

## Step4: Deploy or Debug  
To debug just run **python manage.py runserver**. For deployment, I recommend gunicorn and nginx. Note that you need to set up nginx to serve static and media files. This is important! Don't use django to serve static files.
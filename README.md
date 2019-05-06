# Blog
My blog using py3, Django2.2. Checkout how it works: [bigborg.top](http://www.bigborg.top)

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
 - Go to the file Blog/Blog/private_settings.py and customize your setting. The variables are self-explanatory. 
 - Remove the **baidu-site-verification** meta line in the file Blog/Blog/templates/posts/base.html since the code is just for  myself.

## Step3: Mysql Database
**mysqlclient** library is needed. Conda is recommended way to install it rather than pip because conda handles c dependencies better than pip.(I went into segmentation fault using pip. It took me hours to find out what was wrong.)
Remember to create database and database user in mysql.

## Celery
Celery is used to send account activation email asynchronously.
#### redis
To run celery, you need to deploy redis first. Please refer to redis official website for instructions. When you get redis running, you could start celery with the following command.
```buildoutcfg
celery -A Blog worker
```

## Step4: Deploy or Debug  
To debug just run **python manage.py runserver**. For deployment, I recommend gunicorn and nginx. Note that you need to set up nginx to serve static and media files. This is important! Don't use django to serve static files.
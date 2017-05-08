from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')


from celery import Celery
from smtplib import SMTP
import logging
from Blog.private_settings import EMAIL_SMTP_PASSWORD, EMAIL_SMTP_USERNAME
from email.mime.text import MIMEText

celery_app = Celery("Tasks", broker="redis://localhost")

celery_app.autodiscover_tasks()

@celery_app.task
def send_html_email(from_addr:str, to_addr:str, html:str, subject:str):
    try:
        smtp_client = SMTP("smtp.163.com", 25)
        smtp_client.login(EMAIL_SMTP_USERNAME, EMAIL_SMTP_PASSWORD)  # Change this
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject
        msg['To'] = to_addr
        msg['From'] = from_addr
        smtp_client.send_message(msg)
        smtp_client.quit()
    except Exception as e:
        logging.error(str(e))
        return False
    return True

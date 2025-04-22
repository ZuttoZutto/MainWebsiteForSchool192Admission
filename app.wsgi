#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Admission192/website")
from app import app as application
application.secret_key = "yandexlyceum_secret_key"

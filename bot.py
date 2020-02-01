from database import DBHelper
from telegram.ext import(
    Updater, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    Filters
)

import requests, sqlite3
from datetime import date
import calendar
import logging, operator
import config, json

db = DBHelper()

TOKEN = '1063572352:AAGwEtOQHbjao1Xuv5CbrX-Bqqao0r1UUFw'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def attendance_calculator():
    for 

# TimeTable
my_date = date.today()
day = calendar.day_name[my_date.weekday()]

if day == 'Monday':
    table = ['os', 'toc', 'os[p]', 'cp2', 'dc']

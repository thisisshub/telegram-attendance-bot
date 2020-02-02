from todoist.api import TodoistAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters

# imports
import requests
from datetime import datetime
import uuid
import json
import configparser

# API_TOKEN
api_token = 'df864d9cbf7b4e669e50bf626fa088eef855ff5e'
bot_token = '1063572352:AAGwEtOQHbjao1Xuv5CbrX-Bqqao0r1UUFw'

class APIHandler:

    def __init__(self, api_token, api_url):
        # initiate a todoist api instance
        self.api = TodoistAPI(api_token)
        self.api_token = api_token
        self.api_url = api_url

    def get_project_list(self):
        self.api.sync()
        project_list = self.api.state['projects']
        return project_list

    def get_tasks_by_project(self, project_id):
        tasks_list = requests.get(
            "%s/tasks" % self.api_url,
            params={
                "project_id": project_id
            },
            headers={
                "Authorization": "Bearer %s" % self.api_token
            }).json()

        return tasks_list

    def create_project(self, project_name):
        self.api.projects.add(project_name)
        self.api.commit()
        return True

    def get_all_tasks(self):
        tasks_list = requests.get(
            "%s/tasks" % self.api_url,
            headers={
                "Authorization": "Bearer %s" % self.api_token
            }).json()
        return tasks_list

    def get_today_tasks(self):
        all_tasks = self.get_all_tasks()
        today_tasks = []

        today = datetime.today().date()
        for task in all_tasks:
            task_due = task.get('due')
            if task_due:
                task_due_date_string = task_due.get('date')
                task_due_date = datetime.strptime(task_due_date_string, '%Y-%m-%d').date()
                if task_due_date == today:
                    today_tasks.append(task)

        return today_tasks

    def create_task(self, task_content):
        result = requests.post(
            "%s/tasks" % self.api_url,
            data=json.dumps({
                "content": task_content,
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % self.api_token
            }).json()

        return result

class TodoistBot:
    class Flags:
        new_project = False
        new_task = False
        select_project_for_task = False
    
        def __init__(self, flag=False):
            self.new_project = flag
            self.new_task = flag
            self.select_project_for_task = flag

    flags = Flags()
    
    def __init__(self):
        # Read Configs from file
        config = configparser.ConfigParser()
        config.read("config.ini")

        # set Telegram bot token
        bot_token = config['telegram']['bot_token']
        # set Todoist API token
        api_token = config['todoist']['api_token']
        # set Todoist API URL
        api_url = config['todoist']['api_url']

        # initiate a Telegram updater instance
        self.updater = Updater(bot_token)

        # initiate a Todoist API handler
        self.api = APIHandler(api_token, api_url)

    def new_task(self, bot, update):
        chat_id = update.message.chat_id
        self.flags.new_task = True
        bot.send_message(chat_id=chat_id, text="enter name for new task")

    def general_handler(self, bot, update):
        chat_id = update.message.chat_id
        text = update.message.text

        if self.flags.new_task:
            if self.api.create_task(text):
                bot.send_message(chat_id=chat_id, text="task created: " + text)

    def projects(self, bot, update):
        chat_id = update.message.chat_id
        project_list = self.api.get_project_list()

        keyboard = []
        for project in project_list:
            keyboard.append(
                [InlineKeyboardButton(project['name'], callback_data=project['id'])])

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text="Choose a Project to see tasks list", reply_markup=reply_markup)

    def main(self):
        updater = self.updater
        dp = updater.dispatcher

        # Add command handlers
        dp.add_handler(CommandHandler('projects', self.projects))
        # other commands will goes here
        dp.add_handler(CommandHandler('newtask', self.new_task))
        # Add callback handlers for buttons
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))

        # general message handler
        updater.dispatcher.add_handler(MessageHandler(Filters.all, self.general_handler))
        updater.start_polling()
        updater.idle()

    # handler for buttons
    def button(self, bot, update):
        query = update.callback_query

@staticmethod
def task_button_markup(tasks):
    keyboard = []
    for task in tasks:
        keyboard.append(
            [InlineKeyboardButton(task['content'], url=task['url'], callback_data=task['id'])])

    markup = InlineKeyboardMarkup(keyboard)
    return markup

todoist_object = TodoistBot()
APIHandler_object = APIHandler()


from crontab import CronTab
import os

cron = CronTab(tab='')

ROOT_DIR = os.path.dirname(os.path.abspath('C:/Users/bbogd/PycharmProjects/manage_patient_medication'))
file_name = os.path.join(ROOT_DIR, 'popup_reminder.py')

job = cron.new(command='python C:/Users/bbogd/PycharmProjects/manage_patient_medication/popup_reminder.py')
job.minute.every(1)

cron.write()


import argparse
import sys
import time
from time import localtime
import datetime
from dateutil.relativedelta import relativedelta

import logging
from utils import within_1d, convert_to_s

def allow(website):
    with open('/etc/hosts', 'w') as hostfile:
        logging.debug(f"Allowing {website}")
        # TODO: delete line in hostfile
        pass

def block(website):
    with open('/etc/hosts', 'w+') as hostfile:
        logging.debug(f"Blocking {website}")
        hostfile.write(f'127.0.0.1 {website}')


def scheduler(schedule_list):
    while True:
        current = time.localtime()
        today = datetime.date.today()
        filtered_schedule = [schedule for schedule in schedule_list if within_1d(current, schedule)]
        logging.debug(f"Filtered schedule: {filtered_schedule}")
        s = []
        
        for schedule in filtered_schedule:
            block_time = datetime.datetime(today.year, today.month, today.day, schedule['start'], 0, 0)
            allow_time = datetime.datetime(today.year, today.month, today.day, schedule['end'], 0, 0)
            s.append((block_time, schedule['website'], 'BLOCK'))
            s.append((allow_time, schedule['website'], 'ALLOW'))

        s = sorted(s)
        s.append((None, None, "reset")) # This is ugly

        logging.debug(f"Today's scheduled events: {s}")
        for item in s:
            yield item
            
            
def run(config_args):
    schedule = scheduler(config_args)
    while True:
        next_execution, website, action = next(schedule)
        sleep_time = relativedelta(next_execution, datetime.datetime.now())
        sleep_time_s = convert_to_s(sleep_time)

        # Pause until next scheduled item
        logging.info(f"{action},{allow} scheduled at {next_execution}")
        logging.debug(f"Sleeping for {sleep_time_s} seconds")
        time.sleep(sleep_time_s)

        if action == 'allow':
            allow(website)
        elif action == 'block':
            block(website)
        else: # Reset
            schedule = scheduler(config_args)

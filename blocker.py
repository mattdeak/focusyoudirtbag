import argparse
import sys
import time
from time import localtime
import datetime
from dateutil.relativedelta import relativedelta
import logging
from utils import within_1d, convert_to_s

def hostfile_contains(target_string):
    with open('/etc/hosts', 'r') as hostfile:
        lines = hostfile.readlines()
        for line in lines:
            if target_string in line:
                return True

    return False

def allow(website):
    target_string = f'127.0.0.1 {website}'

    if not hostfile_contains(target_string):
        logging.warning(f"Allow action scheduled for currently permitted website: {website}. Skipping")
        return

    with open('/etc/hosts', 'r+') as hostfile:
        logging.debug(f"Allowing {website}")
        # TODO: delete line in hostfile
        lines = hostfile.readlines()
        hostfile.seek(0)
        for line in lines:
            if target_string not in line:
                hostfile.write(line)
        hostfile.truncate()

def block(website):
    target_string = f'127.0.0.1 {website}\n'
    if hostfile_contains(target_string):
        logging.warning(f"Block action scheduled for currently blocked website: {website}. Skipping.")
        return

    with open('/etc/hosts', 'a+') as hostfile:
        logging.debug(f"Blocking {website}")
        hostfile.write(target_string)


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

        tomorrow = today + datetime.timedelta(days=1)
        reset_execution_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0) # Restart at midnight
        s.append((reset_execution_time, None, "reset"))

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
        logging.info(f"{action},{website} scheduled at {next_execution}")
        logging.debug(f"Sleeping for {sleep_time_s} seconds")

        # If two events are scheduled simultaneously, it's possible to sleep time to be slightly
        # negative due to latency. If that's the case, just don't sleep at all
        if sleep_time_s > 0:
            time.sleep(sleep_time_s)

        if action == 'ALLOW':
            allow(website)
        elif action == 'BLOCK':
            block(website)
        else: # Reset
            schedule = scheduler(config_args)

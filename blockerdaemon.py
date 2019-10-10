import sys
import daemon
from time import localtime
import datetime
from dateutil.relativedelta import relativedelta

def within_1d(time, schedule):
    """Determines if schedule is relevant for the current data"""
    return (schedule['day'] == 'weekdays' and time.tm_wday <= 5
            or schedule['day'] == time.tm_wday)

def convert_to_ms(timedelta):
    """"""

def block(website):
    with open('/etc/hosts', 'w+') as hostfile:
        hostfile.write(f'127.0.0.1 {website}')


def scheduler(schedule_list):
    
    while True:
        current = time.localtime()
        filtered_schedule = [schedule for schedule in schedule_list if within_1d(schedule)]
        s = []
        
        for item in filtered_schedule:
            block_time = datetime.time(schedule['start'], 0, 0)
            allow_time = datetime.time(schedule['end'], 0, 0)
            s.append(block_time, schedule['website'], 'BLOCK')
            s.append(allow_time, schedule['website'], 'ALLOW')

        s = sorted(s)
        for item in s:
            yield item
            
            

def daemon(config_args):
    schedule = scheduler(config_args)
    while True:
        next_execution, website, action = next(schedule)
        sleep_time = relativedelta()
        if action == 'allow':
            # Allow
        elif action == 'block':
            # Block
            block(website)
        else: # Reset
            schedule = scheduler(config_args)


def init_daemon():
    with open('blocked.config', 'r') as config_file:
        lines = config_file.readlines()

    lines = [line.strip().split() for line in lines]
    
# focusyoudirtbag
A simple python daemon that schedules websites to be blocked over certain time intervals. Only supported on linux.
Just run `python run.py` after filling up the config file. I needed this because I can't stay off chess.com.

### Config file
Add websites you want to block as follows:

WEBSITE WEEKDAY START_HOUR END_HOUR

DAY can be numeric (0 is monday - 7 is sunday) or "weekdays". 
START_HOUR and END_HOUR are the hour as represented on a 24 hour clock.

Example config file is provided. Better customization coming eventually.

#### How it works
This daemon basically just alters the /etc/hosts at scheduled intervals. As such it needs to be run with enough privilege to do so.
The easiest way is to run as root.

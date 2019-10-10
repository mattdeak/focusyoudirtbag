#!/usr/bin/python3
from blocker import run
import argparse
import daemon
import logging
import os
import sys

def cmdline_args():
    parser = argparse.ArgumentParser(description='Focus you dirtbag. Stop visiting timewaster sites.')
    parser.add_argument('--loglevel', help='Set Log Level', choices=['DEBUG','INFO','WARNING','ERROR'], default='INFO')
    parser.add_argument('--logfile', help='Path to log file', default='./app.log')
    parser.add_argument('-fg', action='store_true', help='Run in foreground')
    return parser.parse_args()

def logger_config(logfile, loglevel):
    format_str = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    handler = logging.FileHandler(logfile, 'w+')
    
    logging.basicConfig(
        level=loglevel,
        format=format_str,
        handlers=[handler])

    return handler


def parse_config():
    with open('websites.config', 'r') as config_file:
        lines = config_file.readlines()

    lines = [line.strip().split() for line in lines]
    config_args = [{'website': l[0], 'day': l[1], 'start': int(l[2]), 'end': int(l[3])} for l in lines]
    return config_args

def has_sufficient_access():
    return os.access('/etc/hosts', os.W_OK)

if __name__ == '__main__':

    args = cmdline_args()

    if args.loglevel == 'DEBUG':
        loglevel = logging.DEBUG
    elif args.loglevel == 'INFO':
        loglevel = logging.INFO
    elif args.loglevel == 'WARNING':
        loglevel = logging.WARNING
    else:
        loglevel = logging.ERROR

    handler = logger_config(args.logfile, loglevel)

    if not has_sufficient_access():
        error_msg = "This program was not run with sufficient priviledge to modify to /etc/hosts"
        print(error_msg)
        logging.error(error_msg)
        sys.exit(1)

    config_args = parse_config()
    if args.fg:
        run(config_args)
    else: # Run in background
        with daemon.DaemonContext(files_preserve=[handler.stream.fileno()]):
            run(config_args)


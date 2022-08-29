"""gph_logging.py
Implements simple logging functions for use in Gold Partyhat.
"""
from datetime import *
from gph_config import *


def log_message(msg):
    """Logs messages to file LOG_FILE set in gph_config.py

    :param msg: String to print to logfile with timestamp.
    :return: No return, prints to logfile.
    """
    logfile = open(LOG_NAME, 'a')
    now = datetime.now()
    timestamp = now.strftime('[%d %b %Y - %H:%M:%S] ')
    logfile.write(timestamp + msg + '\n')
    logfile.close()

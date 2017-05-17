import logging
import sys
import os
import datetime

from colorama import *
from functools import wraps


class Retry_Error(Exception):
    pass


def ignore(level=logging.INFO, message=None):
    def decorate(func):
        msg = message if message else ''
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logging.log(level, msg + " ignored.\t" + repr(e))
            else:
                return result
        return wrapper
    return decorate


def retry(retry_time=3, level=logging.INFO, message=None):
    def decorate(func):
        msg = message if message else ''
        @wraps(func)
        def wrapper(*args, **kwargs):
            d_time = 1
            feedback_queue = kwargs.get('feedback_queue', None)
            feedback_pool = kwargs.get('feedback_pool', None)
            feedback_index = kwargs.get('feedback_index', None)
            while True:
                if d_time > retry_time:
                    if feedback_queue != None:
                        feedback_queue.put(Retry_Error)
                    if feedback_index != None and feedback_pool != None:
                        feedback_pool[feedback_index] = Retry_Error
                    break
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logging.log(level, msg + " Retrying... " + str(d_time) + " time(s).\t" + repr(e))
                    d_time += 1
                else:
                    break
        return wrapper
    return decorate


def init_all(level=logging.INFO):
    if not os.path.exists('log'):
        os.mkdir('log')

    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(threadName)s: %(message)s")
    fileHandler = logging.FileHandler(os.path.join('log', str(datetime.datetime.now()).replace(':', '_') + '.log'))
    fileHandler.setFormatter(logFormatter)
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(Log_Formatter())
    rootLogger.addHandler(consoleHandler)
    rootLogger.addHandler(fileHandler)


class Log_Formatter(logging.Formatter):
    def __init__(self, style='{'):
        logging.Formatter.__init__(self, style=style)

    def format(self, record):
        stdout_template = '{levelname}' + Fore.RESET + '] {threadName}: ' + '{message}'
        stdout_head = '[%s'

        allFormats = {
            logging.DEBUG: logging.StrFormatStyle(stdout_head % Fore.LIGHTBLUE_EX + stdout_template),
            logging.INFO: logging.StrFormatStyle(stdout_head % Fore.GREEN + stdout_template),
            logging.WARNING: logging.StrFormatStyle(stdout_head % Fore.LIGHTYELLOW_EX + stdout_template),
            logging.ERROR: logging.StrFormatStyle(stdout_head % Fore.LIGHTRED_EX + stdout_template),
            logging.CRITICAL: logging.StrFormatStyle(stdout_head % Fore.RED + stdout_template)
        }

        self._style = allFormats.get(record.levelno, logging.StrFormatStyle(logging._STYLES['{'][1]))
        self._fmt = self._style._fmt
        result = logging.Formatter.format(self, record)

        return result



def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        print(s, end='')
    else:  # total size is unknown
        print("read %d\n" % (readsofar,), end='')



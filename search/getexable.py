"""
1단계
- 공격 가능한 페이로드 찾는 부분
- 김시영
"""

#def attack(...) -> ...

from typing import Callable
from requests import Response
from multiprocessing.pool import ThreadPool

from web import Link, ExploitLink
from utils.threading_extend import ThreadResult, startall
import tqdm
import time


class GetExableError(Exception): ...
class NoExableError(GetExableError): ...

class GetExAble:
    is_exed: Callable[[Response], bool]
    def __init__(self, is_exed) -> None:
        self.is_exed = is_exed
   
    def run(self, link: Link, cheatsheet: tuple[list[str], list[str]], delay_time: float) -> ExploitLink:
        # pool = ThreadPool(processes=50)
        # def _tester(exploit_link: ExploitLink):
        #     try_response = exploit_link.request()
        #     return self.is_exed(try_response)
        pbar: tqdm.tqdm
        def _tester(exploit_link: ExploitLink):
            try_response = exploit_link.request()
            pbar.set_description(f"[{time.strftime('%X')}] Exploit")
            pbar.update(1)
            return try_response
        exploit_links = create_exploit_links(link, cheatsheet, delay_time)
        threads = [ThreadResult(target=_tester, args=(exlink,)) for exlink in exploit_links]
        pbar = tqdm.tqdm(total=len(threads), desc=f"[{time.strftime('%X')}] Exploit")
        results = [self.is_exed(response) for response in startall(threads)]
        pbar.close()
        # result = pool.map(_tester, exploit_links)
        # succeed = [exploit_links[i] for i in range(len(exploit_links)) if result[i]]
        succeed = tuple(filter(lambda x:results[exploit_links.index(x)], exploit_links))
        if not succeed:
            raise NoExableError("No Exploitable payload detected.")
        return succeed[0]       #굳이 여러개 필요없음
        
def create_exploit_links(link: Link, cheatsheet: tuple[list[str], list[str]], delay_time: float) -> list[ExploitLink]:
    exploit_links = []
    cheatsheet_form = cheatsheet[0]
    cheatsheet_toexec = [i.format(delay_time=delay_time) for i in cheatsheet[1]]
    for key in link.params.keys():
        for form in cheatsheet_form:
            for delay_command in cheatsheet_toexec:
                # payload = self.create_payload(form, toexec)
                payload = form.format(toexec=delay_command)
                exploit_link = link.to_exploit(key, payload, form, delay_command, params={key:payload})
                #print(exploit_link)
                exploit_links.append(exploit_link)
    return exploit_links




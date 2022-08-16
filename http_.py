from requests import Response

import requests


class DefaultHttpClient:
    def get(self, url: str) -> Response:
        return requests.get(url)

    def check_time(self, response: Response, time: int) -> bool:
        return response.elapsed.total_seconds() < time
    
    def default_time(self, response: Response) -> int:
        return response.elapsed.total_seconds()

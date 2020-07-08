import time
import json
import requests
from requests.exceptions import RequestException
from monitor.exceptions import MaxRequestAttempts

class RequestsManager:
    def __init__(self, arguments):
        self.__uri = arguments["uri"]
        self.__attempts = arguments["attempts"]

    def send(self, stats):
        for attempt in range(self.__attempts):
            try:
                stats = json.dumps(stats)
                response = requests.post(self.__uri, data=stats)
            except RequestException as err:
                time.sleep(5)
            else:
                if response.status_code == 200:
                    break
        else:
            raise MaxRequestAttempts
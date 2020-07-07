import requests

class RequestsManager:
    def __init__(self, arguments):
        self.__uri = arguments.uri
        self.__attempts = arguments.attempts

    def send(self):
        pass
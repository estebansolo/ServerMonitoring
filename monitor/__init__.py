from monitor.requests_manager import RequestsManager

class Monitor:
    def __init__(self, arguments):
        self.__disks = arguments.disks
        self.__requests = RequestsManager(arguments)

    def statistics(self):
        pass
import json
import time
import socket
import psutil
import platform

from datetime import datetime
from monitor.utils import bytes_to_human
from monitor.requests_manager import RequestsManager

class Monitor:
    def __init__(self, arguments):
        self.__disks = arguments.disks
        self.__requests = RequestsManager(arguments)

    def statistics(self, debug=False):
        stats = {
            "cpu": "cpu",
            "disks": "_disks",
            "memory": "memory",
            "uptime": "uptime",
            "swap": "swap_memory",
            "system": "system_data",
            "timestamp": "current_time"
        }
        
        for key, fn in stats.items():
            stats[key] = getattr(self, fn)()

        if debug:
            self.print_debug(stats)
            return
        
        self.__requests.send(stats)
        return stats

    def _disks(self):
        disks = []
        disk_info = psutil.disk_partitions()
        
        for disk in disk_info:
            if disk.fstype in self.__disks:
                continue
            
            try:
                disk_usage = psutil.disk_usage(disk.mountpoint)
            except:
                pass
            else:
                disks.append({
                    "name": disk.device,
                    "type": disk.fstype,
                    "mount_point": disk.mountpoint,
                    "used_size": bytes_to_human(disk_usage.used),
                    "total_size": bytes_to_human(disk_usage.total),
                    "percent_used": bytes_to_human(disk_usage.percent)
                })

        return disks

    @staticmethod
    def memory():
        memory = psutil.virtual_memory()
        return {
            "memory_used_percent": memory.percent,
            "memory_used": bytes_to_human(memory.used),
            "memory_total": bytes_to_human(memory.total),
            "memory_available": bytes_to_human(memory.available),
        }

    @staticmethod
    def cpu():
        cpu_frequency = []
        for freq in psutil.cpu_freq(percpu=True):
            cpu_frequency.append({
                "min": freq.min,
                "max": freq.max,
                "current": freq.current
            })

        return {
            "cpu_frequency": cpu_frequency,
            "cpu_count": psutil.cpu_count(),
            "cpu_usage": psutil.cpu_percent(interval=1),
        }
    
    @staticmethod
    def swap_memory():
        swap = psutil.swap_memory()
        return {
            "swap_used_percent": swap.percent,
            "swap_used": bytes_to_human(swap.used),
            "swap_total": bytes_to_human(swap.total),
        }

    @staticmethod
    def system_data():
        """ Return Platform Details """

        return {
            "system": platform.system(),
            "user": socket.gethostname(),
            "version": platform.release()
        }
    
    @staticmethod
    def uptime():
        return int(time.time() - psutil.boot_time())

    @staticmethod
    def current_time():
        now = datetime.utcnow()

        return {
            "$date": now.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def print_debug(stats):
        print(json.dumps(stats, indent=4))

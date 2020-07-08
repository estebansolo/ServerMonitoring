import json
import time
import socket
import psutil
import platform

from datetime import datetime
from monitor.utils import bytes_to_human
from monitor.requests_manager import RequestsManager

NIC = {
    "mac": "",
    "name": "",
    "address": "",
    "netmask": "",
    "address6": "",
}

class Monitor:
    def __init__(self, arguments):
        self.__disks = arguments["disks"]
        self.__server_name = arguments["name"]
        self.__requests = RequestsManager(arguments)

    def statistics(self, debug=False):
        stats = {
            "cpu": "cpu",
            "disks": "_disks",
            "memory": "memory",
            "uptime": "uptime",
            "network": "network",
            "swap": "swap_memory",
            "system": "system_data",
            "bandwidth": "bandwidth",
            "timestamp": "current_time"
        }
        
        for key, fn in stats.items():
            stats[key] = getattr(self, fn)()

        stats["server_name"] = self.__server_name

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
        cpu_freq = psutil.cpu_freq()

        return {
            "cpu_frequency": {
                "min": round(cpu_freq.min, 2),
                "max": round(cpu_freq.max, 2),
                "current": round(cpu_freq.current, 2)
            },
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
    def network():
        nics = []
        cards = psutil.net_if_addrs()
        for name, snics in cards.items():
            nic = NIC.copy()
            
            nic["name"] = name
            for snic in snics:
                if snic.family == -1:
                    nic["mac"] = snic.address
                elif snic.family == 2:
                    nic["address"] = snic.address
                    nic["netmask"] = snic.netmask
                elif snic.family == 23:
                    nic["address6"] = snic.address
            
            nics.append(nic)

        return nics

    @staticmethod
    def bandwidth():
        # First in/out
        first = psutil.net_io_counters()
        
        time.sleep(1)
        
        # Last in/out
        last = psutil.net_io_counters()

        # Current Speed
        # Download/Upload speed in bytes per seconds.
        return {
            "upload": 0 if first[0] > last[0] else last[0] - first[0],
            "download": 0 if first[1] > last[1] else last[1] - first[1]
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

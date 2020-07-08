import os
import argparse
from dotenv import load_dotenv
from monitor import Monitor

__author__ = "Esteban Solorzano"
__version__ = '1.0.0'

def load_envs(args):
    load_dotenv()

    env_disks = os.getenv("DISKS", "").strip().split()
    disks = [disk.strip() for disk in env_disks if disk.strip()]
    
    return {
        "disks": disks,
        "debug": args.debug,
        "name": os.getenv("NAME", "server1"),
        "attempts": int(os.getenv("ATTEMPTS", 3)),
        "uri": os.getenv("URI", "http://localhost/"),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitoring tool to track server status.')
    parser.add_argument('--debug', dest='debug', action="store_true")
    parser.add_argument('--no-debug', dest='debug', action="store_false")
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    args = load_envs(args)

    app = Monitor(args)
    app.statistics(args["debug"])

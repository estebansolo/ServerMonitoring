import json
import argparse
from monitor import Monitor

__author__ = "Esteban Solorzano"
__version__ = '0.0.0'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitoring tool to track server status.')
    parser.add_argument('-u', '--uri', default='http://localhost/', help='Endpoint to send Monitoring Data (Default http://localhost/)')
    parser.add_argument('-a', '--attempts', default=3, type=int, help='Attempts to send data if case of failure (Default 3)')
    parser.add_argument('-d', '--disks', default=[], nargs='+', help='Avoid specific disks (Default None)')
    parser.add_argument('--debug', dest='debug', action="store_true")
    parser.add_argument('--no-debug', dest='debug', action="store_false")
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    app = Monitor(args)
    server_stats = app.statistics()
    if args.debug:
        print(
            json.dumps(
                server_stats, indent=4
            )
        )

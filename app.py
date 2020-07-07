
__author__ = "Esteban Solorzano"
__version__ = '0.0.0'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitoring tool to track server status.')
    parser.add_argument('-u', '--uri', default='http://localhost/', help='Endpoint to send Monitoring Data (Default http://localhost/)')
    parser.add_argument('-a', '--attempts', default=3, type=int, help='Attempts to send data if case of failure (Default 3)')
    parser.add_argument('-d', '--disks', default=[], nargs='+', help='Avoid specific disks (Default None)')
    args = parser.parse_args()

import os
import re
from prettytable import PrettyTable
import argparse
import requests


def tracert(address):
    ip_regular = re.compile("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}")
    p = os.popen(f"tracert {address}")
    stdout = p.read()
    return ip_regular.findall(stdout)[1:]


def ip_to_as(ip):
    res = requests.request('GET', f'http://ip-api.com/json/{ip}?fields=27137')
    data = res.json()
    if data['status'] == 'success':
        return [data['query'], data['as'].split()[0], data['country'], data['isp']]
    else:
        return [ip, 'local', 'local', 'local']


def format_answer(iterable_ip):
    table = PrettyTable(["hop", "ip", "as", "country", "provider"])
    for i, record in enumerate(iterable_ip):
        table.add_row([i + 1] + record)
    print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Run traceroute and get IP information"
    )
    parser.add_argument("target_ip", help="Target IP address or dns name")
    args = parser.parse_args()

    ip_address = tracert(args.target_ip)
    generate_data = (ip_to_as(ip) for ip in ip_address)
    format_answer(generate_data)


if __name__ == '__main__':
    main()

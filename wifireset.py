
import os
import sys
import time
import subprocess
import requests

currDir = os.path.dirname(__file__)

def parser(key : str):
    idx = lines.find(key)
    idx2 = lines.find("\n", idx)
    s = lines[idx:idx2]
    return s.split(" ")[1]


lines = ""
with open(os.path.join(currDir, ".passwords.txt"), "r") as f:
    lines = f.read()

SSID = parser("SSID")
pwd1 = parser("pwd1")
pwd2 = parser("pwd2")


subprocess.run(['whoami'])
subprocess.run(['ls'])
# subprocess.run(['nmcli'], shell=True)
# subprocess.run(['nmcli', 'dev', 'wifi', 'list'], shell=True) # connect {SSID} password "{pwd2}"').stderr)
print(subprocess.run(['nmcli', 'dev', 'wifi', 'connect', SSID, 'password', pwd2]))

session = requests.Session()

resp = session.get('http://192.168.1.1')

print(resp.status_code)
print(resp.cookies.items())
print(resp.headers)
print(resp.content)

cookies = {
    "s_cc": "true",
    "s_fid": "741A73152523558E-21C25CBD0CB7A98F",
    "s_sq": "[[B]]",
    "xAuth_SESSION_ID": "+guhrFiyC+3cSz2HX0ZN2QA="
}

resp = session.get('http://192.168.1.1/frame_alertWifi.lp', cookies=cookies)
print(resp.status_code)
print(resp.cookies.items())
print(resp.headers)
print(resp.content)
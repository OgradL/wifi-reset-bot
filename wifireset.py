
import os
import sys
import time
import subprocess
import requests
import platform

currDir = os.path.dirname(__file__)

def parser(key : str):
    idx = lines.find(key)
    idx2 = lines.find("\n", idx)
    s = lines[idx:idx2]
    return s.split(" ")[1]

def local_pwd(SSID : str, pwd : str):
    if platform.system() == 'Linux':
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', SSID, 'password', pwd])
    elif platform.platform() == 'Windows':
        # TODO
        pass
    pass

def change_wifi_pwd(pwd):
    # TODO
    pass


lines = ""
with open(os.path.join(currDir, ".passwords.txt"), "r") as f:
    lines = f.read()

SSID = parser("SSID")
pwd1 = parser("pwd1")
pwd2 = parser("pwd2")


local_pwd(SSID, pwd2)

change_wifi_pwd(pwd2)

local_pwd(SSID, pwd2)


import os
import sys
import time
import subprocess
import requests
import platform

from change_local_pwd import change_local_pwd
from change_wifi_pwd import change_wifi_pwd

currDir = os.path.dirname(__file__)

def parser(key : str, stringa : str):
    idx = stringa.find(key)
    idx2 = stringa.find("\n", idx)
    s = stringa[idx:idx2]
    return s.split(" ")[1]


lines = ""
with open(os.path.join(currDir, ".passwords.txt"), "r") as f:
    lines = f.read()

SSID = parser("SSID", lines)
pwd1 = parser("pwd1", lines)
pwd2 = parser("pwd2", lines)


change_local_pwd(SSID, pwd2)

change_wifi_pwd(pwd2)

change_local_pwd(SSID, pwd2)

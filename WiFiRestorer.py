import subprocess
import requests
import os
import platform
from playwright.sync_api import Playwright, sync_playwright, expect

ProfileName = "WiFi-Telecom-57112448.xml"
dirName = os.path.dirname(__file__)
ProfilePath = os.path.join(dirName, ProfileName)

def parser(key : str, stringa : str):
    idx = stringa.find(key)
    if idx == -1:
        return ""
    idx2 = stringa.find("\n", idx)
    s = stringa[idx:idx2]
    return s.split(" ")[1]

def modProfile(NewPwd):
    file = open(ProfilePath, "r")
    contenutoProfilo = file.read()
    contenutoProfilo = contenutoProfilo.replace("PlaceHolderPwd", pwd2)
    if NewPwd != pwd1:
        contenutoProfilo = contenutoProfilo.replace(pwd1, NewPwd)
    else:
        contenutoProfilo = contenutoProfilo.replace(pwd2, NewPwd)
    file.close()
    file = open(ProfilePath, "w")
    file.write(contenutoProfilo)
    file.close()

def resetProfile():
    file = open(ProfilePath, "r")
    contenutoProfilo = file.read()
    contenutoProfilo = contenutoProfilo.replace(pwd2, "PlaceHolderPwd")
    contenutoProfilo = contenutoProfilo.replace(pwd1, "PlaceHolderPwd")
    file.close()
    file = open(ProfilePath, "w")
    file.write(contenutoProfilo)
    file.close()

def connect_to_wifi(ssid, password):
    if platform.system() == 'Linux':
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password])
    elif platform.platform() == 'Windows':
        modProfile(password)
        try:
            subprocess.run(['netsh', 'wlan', 'add', 'profile', 'filename="' + ProfilePath + '"'])
            subprocess.run(['netsh', 'wlan', 'connect', 'name=' + ssid])
        except subprocess.CalledProcessError as e:
            print("Errore durante la connessione al WiFi:", e)
    else:
        print("platform not supported :\\")

def is_internet_available():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://192.168.1.1/index_auth.lp")

    currUrl = page.url
    i=0
    print('ignora:')
    while currUrl != 'http://192.168.1.1/AlertWiFi.lp' and currUrl != 'http://192.168.1.1/frame_alertWifi.lp':
        page.get_by_role("button", name="Avanti >").click()
        print(f'Avanti {i} OK')
        page.get_by_role("button", name="Accedi").click()
        print(f'Accedi {i} OK')
        i=i+1
        currUrl = page.url

    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("button", name="Continua").click()
    page.wait_for_timeout(2000)
    print('continuando..')
    page.wait_for_timeout(5000)
    print('tentativo modifica pwd')
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("button", name="Modifica Sicurezza").click()
    #page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("textbox").click()
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("textbox").focus()
    page.wait_for_timeout(1000) ###### forse si può lasciare ma max 1 sec
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("textbox").press("Control+a")
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("textbox").fill(pwd2)
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("button", name="Conferma").click()
    print('Password modificata')
    page.frame_locator("iframe[name=\"mainFrame\"]").get_by_role("button", name="Avanti >").click()
    page.wait_for_load_state("networkidle") ######OK
    print('processo terminato.')

    # ---------------------
    context.close()
    browser.close()

##COSE
#connect_to_wifi("nome_rete_wifi", "password_wifi")
#disconnect_from_wifi()

#########
        
##codice

#accesso a passwords
passwordsPath = os.path.join(dirName, ".passwords.txt")
passwordFile = open(passwordsPath, "r")
passwordContent = passwordFile.read()
passwordFile.close()
SSID = parser("SSID", passwordContent)
pwd1 = parser("pwd1", passwordContent)
pwd2 = parser("pwd2", passwordContent)
# print('Vuoi iniziare la procedura o uscire?')
# print('Comincia/esci [qualunque tasto/E]')
# azione = input()
# 
# if azione == 'E' or azione == 'e':
#     exit()

#controllo connessione
if not is_internet_available():
    #connessione con PWD vecchia
    connect_to_wifi(SSID, pwd1)

#controllo connessione
print('Provo a connettermi...')
while(not is_internet_available()):
    is_internet_available()
print('Connesso!\n')

#va sul browser
#SPOSTA su la riga import E sposta su la funzione
with sync_playwright() as playwright:
    run(playwright)

#riconnessione a internet
print('Mi riconnetto...')
connect_to_wifi(SSID, pwd2)

resetProfile()

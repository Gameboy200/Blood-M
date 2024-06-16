import os
import rumps
import requests
import schedule
import time
import threading
import pygame
import tkinter as tk
from tkinter import *
from tkinter import messagebox
key = 'url.key'
api_url = ''
BG = '___'
mute = False
##api_url = "https://testpmg.chickenkiller.com/api/v1/entries/sgv.json?count=1&token=max-009021062b4989e3"
def read_blood(app):
    with open(key, 'r') as f:
        api_url = f.read().strip()
    if api_url == '':
        print('couldnt find url')
        return
    else:
        print('found url')
    print(api_url)
    response = requests.get(api_url)
    print(response)
    datadist = response.json()
    data = datadist[0]
    sgv = data['sgv']
    dirc = data['direction']
    print(sgv)
    xrBG = sgv * 0.0555
    print(xrBG)
    global BG
    BG = round(xrBG, 1)
    if dirc == 'SingleUp' or dirc == 'DoubleUp' or dirc == 'FortyFiveUp':
        arrow = '↑'
        BG = str(BG) + arrow
    elif dirc == 'SingleDown' or dirc == 'DoubleDown' or dirc == 'FortyFiveDown':
        arrow = '↓'
        BG = str(BG) + arrow
    else:
        arrow = '→'
        BG = str(BG) + arrow
    ABG = BG.replace(arrow, '')
    currentdir = os.path.dirname(__file__)
    if float(ABG) < 4.0:
        pygame.mixer.init()
        low_path = os.path.join(currentdir, 'low.wav')
        low_blood = pygame.mixer.Sound(low_path)
        low_blood.play(loops=-1)
    elif float(ABG) > 10.5:
        pygame.mixer.init()
        high_path = os.path.join(currentdir, 'high.wav')
        high_blood = pygame.mixer.Sound(high_path)
        high_blood.play(loops=-1)
    print (BG)
    app.title = str(BG)
##    schedule.every(1).minutes.do(read_blood)
##    while True:
##        schedule.run_pending()
##        time.sleep(1)

def refresh():
    while True:
        schedule.run_pending()
        time.sleep(1)

def sloop():
        print('snooze')    
        loopmin = 15
        loopsec = loopmin * 60
        looptim = time.time()
        while time.time() - looptim < loopsec:
            pygame.mixer.stop()
            time.sleep(0.5)

def mloop():
    global mute
    while mute:
        pygame.mixer.stop()
        time.sleep(0.5)
    return

def eloop():
    print('unmuted2')
    global mute
    mute = False
    print('unmuted3')


##schedule.every(1).minutes.do(read_blood)

class Fun(rumps.App):
    def __init__(self):
        super(Fun, self).__init__(str(BG))
        smute = 'Mute'
        self.menu = ["Change url", "Snooze", "Mute"]
        schedule.every(1).minutes.do(read_blood, self)
        read_blood(self)
        threading.Thread(target=refresh, daemon=True).start()
        self.title = str(BG)
        print('run')

    @rumps.clicked("Change url")
    def Changeurl(self, _):
        self.open_tkinter_window()

    def open_tkinter_window(self):
        # Creating a new Tkinter window
        window = rumps.Window("Enter URL", "Change URL")
        inpu = window.run()
        if inpu.clicked:
            url = inpu.text
            print(url)
            check = requests.get(url)
            print(check)
            check2 = check.json()
            print(check2)
            check3 = check2[0]
            check4 = check3['sgv']
            if check4:
                with open(key, 'w') as f:
                    f.write(f'{url}')
                rumps.alert("successfully changed")
                read_blood(self)
            else:
                rumps.alert('invalid url')

    @rumps.clicked("Snooze")
    def Snooze(self, _):
        loop_thread = threading.Thread(target=sloop)
        loop_thread.start()

    @rumps.clicked("Mute")
    def Mute(self, _):
        global mute
        if not mute:
            print('muted')
            global smute
            self.menu["Mute"].title = 'Unmute'
            mute = True
            global loop_thread
            loop_thread = threading.Thread(target=mloop)
            loop_thread.start()
        elif mute:
            print('unmuted')
            self.menu["Mute"].title = 'Mute'
            mute = False
            eloop_thread = threading.Thread(target=eloop)
            eloop_thread.start()
            
##schedule.every(1).minutes.do(read_blood)
##while True:
##    schedule.run_pending()
##    time.sleep(1)

if __name__ == "__main__":
    Fun().run()

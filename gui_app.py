# pyinstaller -–onefile -–windowed --icon="images\myicon.ico" myApp.py
# for making executable
from timer import *
import tkinter as tk
import requests
from bs4 import BeautifulSoup
from notifier import Notifier
import argparse
import time
import sys
from tkinter import *
import signal


WAIT_TIME_SECONDS = 120

root= tk.Tk()
root.title('Notifier')

# photo = PhotoImage(file = 'icon.jpeg')
# tk.iconphoto(False, photo) 
canvas1 = tk.Canvas(root, width = 400, height = 450,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='New Entry Notifier')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 40, window=label1)

label2 = tk.Label(root, text='Registration number:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)



label3 = tk.Label(root, text='Email:')
label3.config(font=('helvetica', 10))
canvas1.create_window(200, 180, window=label3)

entry2 = tk.Entry (root) 
canvas1.create_window(200, 220, window=entry2)

label4 = tk.Label(root, text='Password:')
label4.config(font=('helvetica', 10))
canvas1.create_window(200, 260, window=label4)

entry3 = tk.Entry (root) 
canvas1.create_window(200, 300, window=entry3)


text = """\
Information is  available now!!
Registration Number: {}
Exporter name: {}
Address: {}
City: {}
State: {}
Pin: {}
Phone Number: {}
Email id: {}
Firm name: {}
Regards,
Zaid Khan"""
def fetch_info(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')    
    name = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblExpName').text
    address = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblAddress').text
    city = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblCity').text
    state = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblState').text
    pin = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblPIN').text
    phone_number = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblPhone').text
    email = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblEmail').text
    registration_number = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblRegNo').text
    firm_name = soup.find(id = 'ctl00_ContentPlaceHolderMain_lblFirmType').text
    # nonlocal text
    global text
    not_empty = False
    text = text.format(registration_number, name, address, city, state, pin, phone_number, email, firm_name)
    if name != "":
        not_empty = True
    return text, not_empty

def notify ():
    registration_number = entry1.get()
    email = entry2.get()
    password = entry3.get()
    # x1 = entry1.get()

    apedia_url = 'http://itrack.apeda.gov.in/RCMCAPEDA/StatusExporterDetails.aspx?rcmc=' + registration_number
    # name, address, city, state, pin, phone_number, email, registration_number, firm_name = fetch_info(apedia_url)
    
    
    label5 = tk.Label(root, text = 'Request taken!! Processing', font = ('helvetica', 10))
    canvas1.create_window(200, 400, window=label5)

    notifier = Notifier(email, email, password)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=fetch_info)
    job.start()
    
    while(True):
        try:
            text, not_empty = fetch_info(apedia_url)
            if not_empty:
                notifier.notify(text, subject="Information for registration number: {}".format(registration_number))
                sys.exit(0)
            time.sleep(120)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            job.stop()
            break

    # label3 = tk.Label(root, text= 'The Square Root of ' + x1 + ' is:',font=('helvetica', 10))
    # canvas1.create_window(250, 350, window=label3)
    
    # label4 = tk.Label(root, text= float(x1)**0.5,font=('helvetica', 10, 'bold'))
    # canvas1.create_window(250, 380, window=label4)
    
button1 = tk.Button(text='Notify', command=notify, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 360, window=button1)

root.mainloop()
import requests
from bs4 import BeautifulSoup
from notifier import Notifier
import argparse
import time
import sys

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
    text = text.format(registration_number, name, address, city, state, pin, phone_number, email, firm_name)
    if name != "":
        not_empty = True
    return text, not_empty

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--password", type=str, required=True,
        help="enter your gmail password")
    ap.add_argument('-rn', "--registration_number", type = str, required=True, 
        help="enter registration number")
    # ap.add_argument("-c", "--crop", type=int, default=0,
    #     help="whether to crop out largest rectangular region")
    args = vars(ap.parse_args())
    apedia_url = 'http://itrack.apeda.gov.in/RCMCAPEDA/StatusExporterDetails.aspx?rcmc='+ args["registration_number"]
    # name, address, city, state, pin, phone_number, email, registration_number, firm_name = fetch_info(apedia_url)
    
    

    notifier = Notifier('zaid.kv5@gmail.com', 'khan.2@iitj.ac.in', args['password'])
    while(True):
        text, not_empty = fetch_info(apedia_url)
        if not_empty:
            notifier.notify(text, subject="Information for registration number: {}".format(args["registration_number"]))
            sys.exit(0)
        time.sleep(120)

if __name__ == "__main__":
    main()


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
import time

URL = "https://manganelo.com/manga/read_one_punch_man_manga_online_free3"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

def epcheck():  # check if there is new episode
    lastdate = datetime.strptime(open("lastDate.txt", "r").read(), '%d/%m/%y')
    newdate = soup.find_all("span", {'class': "chapter-time"})[0].get_text().replace(",", "").replace(" ", "")
    month = newdate[0:3].lower()
    day = newdate[3:5]
    year = newdate[5:7]

    monthlist = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                 'jul', 'aug', 'sep', 'okt', 'nov', 'des']  # define month as a number
    month = str(monthlist.index(month)+1)
    date_time = datetime.strptime(day+'/'+month+'/'+year, '%d/%m/%y')

    if date_time > lastdate:  # compare last episode date with new episode date
        send_mail()
        lastdate = open("lastDate.txt", "w")
        lastdate.write(day+'/'+month+'/'+year)  # update the last episode date to lastDate.txt
        lastdate.close()
        print("EMAIL HAS BEEN SENT")

    else:  # no new episode yet :(
        print("There's still no new episode :(")

def send_mail():  # send an email if new episode came out
    password = open("password.txt", "r").read()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('smanti.pilketos2020@gmail.com', password)

    message = """\
    Subject: One Punch Man New Episode

Hey! New episode of One Punch Man just came out. Check it out!
    """

    server.sendmail("smanti.pilketos2020@gmail.com", "armand.dwi@gmail.com", message)

    server.quit()

while True:
    epcheck()
    time.sleep(60*60*24)  # these codes will loop every 1 day

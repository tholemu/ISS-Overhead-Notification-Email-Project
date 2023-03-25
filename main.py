import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "name@yahoo.com" #Enter your valid email address
MY_PASSWORD = "password" #Enter your email password
MY_LAT = 38.627003 # Your latitude
MY_LONG = -90.199402 # Your longitude


#Function for findout out if the ISS is close to my current position
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

#Function for finding out if it is currently dark
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

#While loop for determining if ISS is overhead and if its dark, then send yourself an email to look up in the sky
#Make sure you've got the correct smtp address for your email provider:
#Gmail: smtp.gmail.com
#Hotmail: smtp.live.com
#Outlook: outlook.office365.com
#Yahoo: smtp.mail.yahoo.com
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.mail.yahoo.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky!"
        )





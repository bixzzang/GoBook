import datetime
import json
import os
import subprocess
import time

from datetime import date

webhook_msg = ""

def send_webhook(content, title, url):
    global webhook_msg
    if webhook_msg == content:
        return "duplicated message"
    webhook_msg = content
    webhook_url = "https://discordapp.com/api/webhooks/1291732609482887169/xJq9FagwA2yC7msNMeZ5O2wMi-jvb-pNqTPZBJUBAaDjPMMgSDjBgmN_M72Dnsoz51nE"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': 'Golf Booking Notice',
        'content': content,
        'embeds': [
            {
                "title" : title,
                "url": url
            }

        ]
    }

    import requests
    print("Send webhook " + content)
    response = requests.post(webhook_url, json=data, headers=headers)
    subprocess.call(["afplay", "./warn.wav"])
    #return ""
    return response.status_code


weekday_str = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

print(">>>>> Choose golf course:")
print("1. Vancouver")
print("2. Burnaby")
print("3. UBC")
print("4. Vancouver + Burnaby")
print("5. All")
mode = input("Select:").strip()

print(">>>>>> Input Date")
today = date.today() + datetime.timedelta(days=1)
year = input('Year[{}]:'.format(str(today.year))).strip()
month = input('Month[{}]:'.format(str(today.month))).strip()
day = input('Day[{}]:'.format(str(today.day))).strip()

if year == '':
    year = str(today.year)
if month == '':
    month = str(today.month)
if day == '':
    day = str(today.day)


target_date = date(int(year), int(month), int(day))
print("Target date is " + str(target_date))

burnaby_date = weekday_str[target_date.weekday()] + "%20" + target_date.strftime("%b%%20%d%%20%Y")
van_date = "{}-{}-{}".format(str(target_date.year), str(target_date.month), str(target_date.day))

burnaby_url = "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23"
van_url = "https://secure.west.prophetservices.com/CityofVancouver/Home/nIndex?CourseId=2,1,3&Date={}&Time=AnyTime&Player=99&Hole=18".format(van_date)
ubc_url = "https://www.chronogolf.ca/club/university-golf-club#?course_id=525&nb_holes=18&date=2024-10-05&affiliation_type_ids=2897,2897,2897,2897".format(target_date)

print(burnaby_url)
print(van_url)
print(ubc_url)
print(">>>>> Player Number")
player = input("Number of Player [0:Any/1/2/3/4]:").strip()
burnaby_player = player
van_player = player
if player == "0":
    van_player = "99"

print(">>>>> Time")
print(">>>>> Search from:")
burnaby_start_time = int(input("24H: "))
print(">>>>> Search to:")
burnaby_end_time = int(input("24H: "))

van_time = "AnyTime"


burnaby_script = open("./burnaby.sh").read()

burnaby_script = burnaby_script.replace("<DATE>", burnaby_date)
burnaby_script = burnaby_script.replace("<PLAYER>", burnaby_player)
burnaby_script = burnaby_script.replace("<START>", '0')
burnaby_script = burnaby_script.replace("<END>", '21')

van_script = open("./van.sh").read()
van_script = van_script.replace("<DATE>", van_date)
van_script = van_script.replace("<PLAYER>", van_player)
van_script = van_script.replace("<TIME>", van_time)

script_ubc = open("./chrono_ubc.sh").read()

script_ubc = script_ubc.replace("<DATE>", str(target_date))

while True:
    found = False
    try:

        if mode == "1" or mode == "4" or mode == "5":
            print("checking Vancouver {} {} {}".format(van_date, van_player, van_time))
            res = os.popen(van_script).read()
            result = res.split("teetime='")
            for element in result[1:]:

                hour = int(element[0:2])
                print(element[:5], hour)

                if burnaby_start_time <= hour < burnaby_end_time:
                    found = True
                    print("Found in Vancouver " + element[:5])
                    send_webhook("Tee Time found in Vancouver course " + str(target_date) + "  " + element[:5],
                                 "Vancouver Golf", van_url)
                    break

        if mode == "3" or mode == "5":
            print("checking UBC  {} {} {}".format(str(target_date), burnaby_start_time, burnaby_end_time))
            res = os.popen(script_ubc).read()
            result = json.loads(res)

            for element in result:
                if "start_time" not in element:
                    continue
                booking_hour = int(element['start_time'][:2])
                if int(burnaby_start_time) <= booking_hour < int(burnaby_end_time):
                    if not element['out_of_capacity']:
                        print("UBC {}".format(element['start_time']))
                        send_webhook("Tee Time found in UBC course " + str(target_date) + "  " + element['start_time'],
                                     "UBC Golf", ubc_url)
                        found = True
                        break
        if mode == "2" or mode == "4" or mode == "5":
            print("checking Burnaby {} {} {} {}".format(burnaby_date, burnaby_player, burnaby_start_time, burnaby_end_time))
            #print(burnaby_script)
            res = os.popen(burnaby_script).read()
            result = json.loads(res)
            #print(result)
            if "messageKey" in result and result["messageKey"] == "NO_TEETIMES":
                print("no teetime")
                time.sleep(5)
                continue
            for element in result:
                print(element['startTime'])
                hour = int(element['startTime'].split('T')[1][:2])
                if burnaby_start_time <= hour < burnaby_end_time:
                    found = True
                    print("Found in Burnaby " + element['startTime'])
                    send_webhook("Tee Time found in Burnaby course " + str(target_date) + "  " + element['startTime'],
                                 "Burnaby Golf", burnaby_url)
                    break

    except:
        print("Error")
        time.sleep(5)
    if found:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>FOUND")
    time.sleep(5)

subprocess.call(["afplay", "./warn.wav"])
time.sleep(5)
subprocess.call(["afplay", "./warn.wav"])

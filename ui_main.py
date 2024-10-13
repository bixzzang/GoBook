import datetime
from datetime import date

import PySimpleGUI as sg
from PySimpleGUI import LISTBOX_SELECT_MODE_BROWSE, LISTBOX_SELECT_MODE_MULTIPLE

days = []
today = ""
for i in range(6):
    day = date.today() + datetime.timedelta(days=i)
    day_str = "%02d-%02d" % (day.month, day.day)
    if i == 0:
        today = day_str

    days.append(day_str)
print(days)

font_main = ("Arial", 20)
sg.set_options(font=font_main)
layout = [
    [sg.Listbox(["UBC", "Vancouver", "Burnaby", "Savage Creek"], size=(15, 5),
                select_mode=LISTBOX_SELECT_MODE_MULTIPLE)],
    [sg.Combo(values=days, size=(15,5), default_value=today)],
    [sg.Slider(range=(0, 16), orientation="h")],
    [sg.Slider(range=(7, 21), orientation="h")],
    [sg.Button(button_text="Start")],
]
window = sg.Window(title="Hello World", layout=layout, margins=(100, 50), font=font_main).read()
while True:                             # The Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()

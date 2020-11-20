from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from PIL import Image, ImageTk
import requests
import getpass

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Fetching Data config File
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

# Function to Extract Data From JSON
def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # Creating Tuple of JSON Data Wanted
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        weather = json['weather'][0]['description']
        final = (city, country, temp_celsius, weather)
        return final

    else:
        return None

# Function to Determine The Data to Fetch From JSON Depending on City Entered
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        temp_lbl['text'] = '{:.2f}°C'.format(weather[2])
        weather_lbl['text'] = weather[3]

    else:
        messagebox.showerror('Error', 'Cannot Find City {}'.format(city))

window = Tk()
window.title("Weather App")
window.geometry('500x250')
window.config(bg = "#8e97a8")

# Search is Limited When Searching for City
city_text = StringVar()
city_entry = Entry(window, textvariable = city_text, bg = '#8e97a8')
city_entry.pack()

# Search Button
search_btn = Button(window, text = "Get Weather", width = 12, command = search)
search_btn.configure(foreground = "#8c0034", background = "#8e97a8")
search_btn.pack()

# Displaying Location
location_lbl = Label(window, text = "", bg = '#8c0034', font = ('bold', 20))
location_lbl.pack()

# Displaying Temperature
temp_lbl = Label(window, text = '', width=0,  
             bg='#8c0034', font=('bold', 15))
temp_lbl.pack()

# Displaying Weather Description
weather_lbl = Label(window, text = '', width = 0, 
            bg = '#8c0034', font = ('bold', 15))
weather_lbl.pack()

window.mainloop()
# imports need to be pip installed
from logging import currentframe
from re import MULTILINE
import requests
import json
import geocoder
import datetime
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require("2.0.0") # indicate kivy version

api_key = "" # this is where people will insert their api key

class WindowManager(ScreenManager): # for managing our three screens
    pass
class MainWindow(Screen): # this is the main window
    # initialize variables
    cityName = ObjectProperty("Undetermined")
    city = ObjectProperty(None)
    currentTemp = ObjectProperty(None)
    feelsLikeTemp = ObjectProperty(None)
    precProb = ObjectProperty(None)
    lat = ObjectProperty(None)
    lon = ObjectProperty(None)

    def searchLocation(self):
        ''' searchLocation() takes the text box input and searches for that location
        arguments:
        -- self
         return:
        -- N/A
        '''
        try: # try except block for exception handling such as invalid input
            cityurl = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric" % (self.city.text, api_key) # url to get response using the city name
            response = requests.get(cityurl) # send a request and get response
            data = json.loads(response.text) # convert json to plain text
            self.cityName = data["name"] # retrieve the city name
            self.city.text = "" # clear the text box
            self.currentTemp = data["main"]["temp"] # get the current temperature
            self.feelsLikeTemp = data["main"]["feels_like"] # get the feels like temperature
            self.lat = data["coord"]["lat"] # get the latitutude
            self.lon = data["coord"]["lon"] # get the longitude
            latlonurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, api_key) # use the lat and lon to send another type of request, this url is different
            latlonresponse = requests.get(latlonurl) # send a request and get response
            latlondata = json.loads(latlonresponse.text) # convert json to plain text
            self.precProb = latlondata["hourly"][0]["pop"] * 100 # get the probability of precipitation and convert it to percentage
        except: # exception handling, notify the user that they inputted an invalid city
            self.city.text = "Invalid city!"

    def findMe(self):
        ''' findMe() uses the users ip to determine their location
        arguments:
        -- self
         return:
        -- N/A
        '''
        self.lat = str(geocoder.ip('me').lat) # use current ip to get latitude
        self.lon = str(geocoder.ip('me').lng) # use current up to get longitude
        # the following code is similar to searchLocation
        cityurl = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, api_key) # use the latitude and longitude to get information
        response = requests.get(cityurl) # send a request and get response
        data = json.loads(response.text) # convert json to plain text
        self.cityName = data["name"] # get the city name 
        self.city.text = "" # clear the text box
        self.currentTemp = data["main"]["temp"] # get the current temperature
        self.feelsLikeTemp = data["main"]["feels_like"] # get the feels like temperature 
        latlonurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, api_key) # use the lat and lon to send another type of request, this url is different
        latlonresponse = requests.get(latlonurl) # send a request and get the response
        latlondata = json.loads(latlonresponse.text) # convert json to plain text
        self.precProb = latlondata["hourly"][0]["pop"] * 100 # get the probability of precipitation and convert it to percentage 
    pass



class DetailedWeatherWindow(Screen): # this window will show in depth details about the weather
    # initialize variables
    cityName = ObjectProperty("Undetermined")
    lat = ObjectProperty(None)
    lon = ObjectProperty(None)
    minTemp = ObjectProperty(None)
    maxTemp = ObjectProperty(None)
    curTemp = ObjectProperty(None)
    feelsLike = ObjectProperty(None)
    pressure = ObjectProperty(None)
    humidity = ObjectProperty(None)
    sunrise = ObjectProperty(None)
    sunset = ObjectProperty(None)

    def on_pre_enter(self): 
        ''' on_pre_enter is a keyword function in kivy
        arguments:
        -- self
         return:
        -- N/A
        '''
        self.updateVar()
    def updateVar(self): 
        ''' updateVar() will update the local variables from information form the main window and get new information for the window
        arguments:
        -- self
         return:
        -- N/A
        '''
        # update local variables from information from the main window
        self.cityName = self.manager.get_screen('mainW').cityName
        self.lat = self.manager.get_screen('mainW').lat
        self.lon = self.manager.get_screen('mainW').lon
        url = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric" % (self.cityName, api_key) # url to make api call using the city name
        response = requests.get(url) # send a request and get response
        data = json.loads(response.text) # convert json to plain text
        # use our data to extract information and assign it to our variables.
        self.minTemp = data["main"]["temp_min"]
        self.maxTemp = data["main"]["temp_max"]
        self.curTemp = data["main"]["temp"]
        self.feelsLike = data["main"]["feels_like"]
        self.pressure = data["main"]["pressure"]
        self.humidity = data["main"]["humidity"]
        # get the sunrise and sunset time, but because it is in unix time, we have to use datetime to convert it to EST
        self.sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
        self.sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
    pass

class HourlyWeatherWindow(Screen):  # this window will show hourly details for the weather
    # initialize all the variables that will have to be used
    cityName = ObjectProperty("Undetermined")
    lat = ObjectProperty(None)
    lon = ObjectProperty(None)
    currentTime = ObjectProperty(None)
    currentTime1 = ObjectProperty(None)
    currentTime2 = ObjectProperty(None)
    currentTime3 = ObjectProperty(None)
    currentTime4 = ObjectProperty(None)
    currentTime5 = ObjectProperty(None)
    currentTime6 = ObjectProperty(None)
    currentTemp = ObjectProperty(None)
    currentTemp1 = ObjectProperty(None)
    currentTemp2 = ObjectProperty(None)
    currentTemp3 = ObjectProperty(None)
    currentTemp4 = ObjectProperty(None)
    currentTemp5 = ObjectProperty(None)
    currentTemp6 = ObjectProperty(None)
    feelsLike = ObjectProperty(None)
    feelsLike1 = ObjectProperty(None)
    feelsLike2 = ObjectProperty(None)
    feelsLike3 = ObjectProperty(None)
    feelsLike4 = ObjectProperty(None)
    feelsLike5 = ObjectProperty(None)
    feelsLike6 = ObjectProperty(None)
    pop = ObjectProperty(None)
    pop1 = ObjectProperty(None)
    pop2 = ObjectProperty(None)
    pop3 = ObjectProperty(None)
    pop4 = ObjectProperty(None)
    pop5 = ObjectProperty(None)
    pop6 = ObjectProperty(None)
    pop7 = ObjectProperty(None)
    
    def on_pre_enter(self):
        ''' on_pre_enter is a keyword function in kivy
        arguments:
        -- self
         return:
        -- N/A
        '''
        self.updateVar()
    def updateVar(self):
        ''' updateVar() will update the local variables from information form the main window and get new information for the window
        arguments:
        -- self
         return:
        -- N/A
        '''
        # update current variables with information from the main window
        self.cityName = self.manager.get_screen('mainW').cityName
        self.lat = self.manager.get_screen('mainW').lat
        self.lon = self.manager.get_screen('mainW').lon
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, api_key) # url to make request
        response = requests.get(url) # send a request and get response
        data = json.loads(response.text) # convert json to plain text
        self.currentTime =  datetime.datetime.fromtimestamp(data["hourly"][0]["dt"]).strftime("%H") # get the current hour
        # increase the hour by 1 and assign it to the respective variables
        self.currentTime1 = int(self.currentTime) + 1 if int(self.currentTime) + 1 < 24 else int(self.currentTime) + 1 - 24
        self.currentTime2 = int(self.currentTime) + 2 if int(self.currentTime) + 2 < 24 else int(self.currentTime) + 2 - 24
        self.currentTime3 = int(self.currentTime) + 3 if int(self.currentTime) + 3 < 24 else int(self.currentTime) + 3 - 24
        self.currentTime4 = int(self.currentTime) + 4 if int(self.currentTime) + 4 < 24 else int(self.currentTime) + 4 - 24
        self.currentTime5 = int(self.currentTime) + 5 if int(self.currentTime) + 5 < 24 else int(self.currentTime) + 5 - 24
        self.currentTime6 = int(self.currentTime) + 6 if int(self.currentTime) + 6 < 24 else int(self.currentTime) + 6 - 24
        # get the different temperatures for the different hours and assign it to their respective variables
        self.currentTemp = data["hourly"][0]["temp"]
        self.currentTemp1 = data["hourly"][1]["temp"]
        self.currentTemp2 = data["hourly"][2]["temp"]
        self.currentTemp3 = data["hourly"][3]["temp"]
        self.currentTemp4 = data["hourly"][4]["temp"]
        self.currentTemp5 = data["hourly"][5]["temp"]
        self.currentTemp6 = data["hourly"][6]["temp"]
        # get the different feels like temperatures for the different hours and assign it to their respective variables
        self.feelsLike = data["hourly"][0]["feels_like"]
        self.feelsLike1 = data["hourly"][1]["feels_like"]
        self.feelsLike2 = data["hourly"][2]["feels_like"]
        self.feelsLike3 = data["hourly"][3]["feels_like"]
        self.feelsLike4 = data["hourly"][4]["feels_like"]
        self.feelsLike5 = data["hourly"][5]["feels_like"]
        self.feelsLike6 = data["hourly"][6]["feels_like"]
        # get the different probability of precipitation for the different hours and assign it to their respective variables
        # we also convert them to percentages and round it to two decimal places
        self.pop = round(data["hourly"][0]["pop"] * 100 , 2)
        self.pop1 = round(data["hourly"][1]["pop"] * 100, 2)
        self.pop2 = round(data["hourly"][2]["pop"] * 100, 2)
        self.pop3 = round(data["hourly"][3]["pop"] * 100, 2)
        self.pop4 = round(data["hourly"][4]["pop"] * 100, 2)
        self.pop5 = round(data["hourly"][5]["pop"] * 100, 2)
        self.pop6 = round(data["hourly"][6]["pop"] * 100, 2)

    pass




builder = Builder.load_file("my.kv") # load our kivy file


class MyApp(App):
    def build(self):
        ''' build() is a function that builds our app
        arguments:
        -- self
         return:
        -- builder, which is our kivy file
        '''
        self.title = "Weather App" # change our window title
        return builder 
if __name__ == "__main__":
    MyApp().run() # run our app
 

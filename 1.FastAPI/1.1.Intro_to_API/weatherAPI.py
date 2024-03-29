import json
import requests

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('weather.ui')
        self.ui.setWindowTitle('Weather App')
        self.ui.show()
        self.ui.button.clicked.connect(self.show)

    def show(self):
        city = self.ui.city_field.text()
        response = requests.get('https://goweather.herokuapp.com/weather/' + city)
        print(response.status_code)
        weather = json.loads(response.text)
        
        if response.status_code == 503: # failure
            QLabel('The source site is down right now. \nPlease try again a few minutes later.', self.ui.error_box).show()
        elif response.status_code == 404:
            QLabel('Please enter a city.', self.ui.error_box).show()
        elif weather['temperature'] == '':
            QLabel('Could not find the city.', self.ui.error_box).show()

        else: # success
            QLabel(weather['temperature'], self.ui.temp_box).show()
            description = weather['description']
            QLabel(description, self.ui.description_box).show()
            QLabel('wind: ' + weather['wind'], self.ui.wind_box).show()

            icon = QLabel(self.ui.today_icon)
            QLabel('Forecast for the next 3 days:', self.ui.forcast_box).show()

            if description == 'Partly cloudy':
                icon.setStyleSheet("image : url(assets/partly.png);") 
            
            if description == 'Clear' or description == 'Sunny':
                icon.setStyleSheet("image : url(assets/sunny.png);") 

            if description == 'Rainy' or description == 'Light rain shower' or description == 'Light rain':
                icon.setStyleSheet("image : url(assets/rainy.png);") 

            if description == 'Snowy' or description == 'Patchy snow nearby':
                icon.setStyleSheet("image : url(assets/snowy.png);") 
            
            icon.resize(128,128)
            icon.show()
            
            forecast = weather['forecast']
            QLabel('Day 1', self.ui.day1_icon).show()
            QLabel('Day 2', self.ui.day2_icon).show()
            QLabel('Day 3', self.ui.day3_icon).show()
            QLabel(forecast[0]['temperature'], self.ui.day1_temp).show()
            QLabel(forecast[0]['wind'], self.ui.day1_wind).show()
            QLabel(forecast[1]['temperature'], self.ui.day2_temp).show()
            QLabel(forecast[1]['wind'], self.ui.day2_wind).show()
            QLabel(forecast[2]['temperature'], self.ui.day3_temp).show()
            QLabel(forecast[2]['wind'], self.ui.day3_wind).show()


app = QApplication([])
window = Window()
app.exec()
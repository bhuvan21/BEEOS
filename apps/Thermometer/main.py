import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager

from helperbee import helper

APP_NAME = "Thermometer"
FIRST = False

Builder.load_file(helper.get_app_path() + APP_NAME + "/thermometer.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

class TemperatureScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        self.info = self.children[0].children[1]
        self.temp = self.children[0].children[2].children[0]
        
        self.update_temperature(None)
        Clock.schedule_interval(self.update_temperature, 0.5)

    def update_temperature(self, dt):
        temperature = helper.sensors.get_temperature()
        self.temp.text = "{}°C".format(temperature)
        self.info = "TODO"

class TemperatureScreenManager(ScreenManager):
    def on_enter(self):
        global FIRST
        if not FIRST:
            self.get_screen("Main").entered()
            FIRST = True

controller = TemperatureScreenManager()
controller.add_widget(TemperatureScreen(name="Main"))

def get_app():
    return controller

def get_icon():
    return "newicon.png"

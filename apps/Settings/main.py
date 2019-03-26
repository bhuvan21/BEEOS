import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

import helperbee

APP_NAME = "Settings"


Builder.load_file(helperbee.HelperBEE.get_app_path() + APP_NAME + "/settings.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

SUBSETTINGS_CATEGORIES = ["Wifi", "Bluetooth", "Sound"]


class SplashScreen(Screen):
    def entered(self):
        self.parent.transition = FadeTransition()
        self.parent.get_screen("Main").entered()
        self.parent.current = "Main"

class SubSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        box = self.children[0]
        for category in SUBSETTINGS_CATEGORIES:
            button = Button(on_press=self.goto_subsetting)
            button.size_hint = (None, None)
            button.size = (480, 40)
            button.text = category
            box.add_widget(button)
    
    def goto_subsetting(self, instance):
        print(instance.text)


class SettingsScreenManager(ScreenManager):
    def on_enter(self):
        self.get_screen("Splash").entered()


controller = SettingsScreenManager()
controller.add_widget(SplashScreen(name="Splash"))
controller.add_widget(SubSettingsScreen(name="Main"))

def get_app():
    return controller

def get_icon():
    return "testicon.png"

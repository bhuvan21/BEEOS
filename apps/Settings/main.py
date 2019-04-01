import os
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from Renderer import Renderer

from helperbee import helper
from device_info import set_password, set_home_image, set_lock_image


APP_NAME = "Settings"


Builder.load_file(helper.get_app_path() + APP_NAME + "/settings.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

SUBSETTINGS_CATEGORIES = ["Wifi", "Security", "Wallpaper", "Update Resources"]


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
        box.add_widget(Renderer())
        for category in SUBSETTINGS_CATEGORIES:
            button = Button(on_press=self.goto_subsetting)
            button.size_hint = (None, None)
            button.size = (480, 40)
            button.text = category
            box.add_widget(button)
    
    def goto_subsetting(self, instance):
        self.parent.transition = FadeTransition()
        self.parent.get_screen(instance.text).entered()
        self.parent.current = instance.text

class WifiScreen(Screen):
    def entered(self):
        self.scroll = self.children[0].children[0]
        self.connected_to = self.children[0].children[1]
        self.connected_to.text = self.connected_to.text.split(":")[0] + ": " + helper.wifi.get_current_ssid()
        
        for network in helper.wifi.get_all_ssids():
            button = Button(on_press=self.connect_to_ssid)
            button.text = network
            self.scroll.children[0].add_widget(button)
        
    def connect_to_ssid(self, instance):
        #TODO
        pass

class SecurityScreen(Screen):
    def entered(self):
        self.keyboard = Window.request_keyboard(
            self.keyboard_close, self)
        
        self.button = self.children[0].children[2].children[0]
        self.button.on_press = self.change_password
        self.input = self.children[0].children[2].children[1]
        self.warning = self.children[0].children[1]
    
    def keyboard_close(self):
        self.keyboard = None

    def change_password(self):
        password = self.input.text
        if len(password) != 6:
            self.warning.text = "Your password must be 6 chars long"
            return
        else:
            for c in password:
                if c not in "1234567890":
                    self.warning.text = "Your password must only use numbers"
                    return

            self.warning.text = "Password changed!"
            set_password(password)

class WallpaperScreen(Screen):
    def entered(self):
        self.lock_button = self.children[0].children[0].children[0]
        self.lock_button.on_press = self.change_lock
        self.home_button = self.children[0].children[0].children[1]
        self.home_button.on_press = self.change_home
        self.warning = self.children[0].children[0]
        self.file_chooser = self.children[0].children[2]
        self.file_chooser.filters = "*.png"
        self.file_chooser.rootpath = os.getcwd()
    
    def change_lock(self):
        set_lock_image(self.file_chooser.selection[0])
        self.warning.text = "Lock screen wallpaper set!"
    
    def change_home(self):
        set_home_image(self.file_chooser.selection[0])
        self.warning.text = "Home screen wallpaper set!"

class UpdateResourcesScreen(Screen):
    def entered(self):
        self.refresh_button = self.children[0].children[1]
        self.refresh_button.on_press = self.refresh
        self.warning = self.children[0].children[0]
    
    def refresh(self):
        mail = helper.email.checkMail()
        if mail[1] != None:
            fp = helper.save_attachment(mail[1])
            

class SettingsScreenManager(ScreenManager):
    def on_enter(self):
        self.get_screen("Splash").entered()


controller = SettingsScreenManager()
controller.add_widget(SplashScreen(name="Splash"))
controller.add_widget(SubSettingsScreen(name="Main"))
controller.add_widget(WifiScreen(name="Wifi"))
controller.add_widget(SecurityScreen(name="Security"))
controller.add_widget(WallpaperScreen(name="Wallpaper"))
controller.add_widget(UpdateResourcesScreen(name="Update Resources"))

def get_app():
    return controller

def get_icon():
    return "settings.png"

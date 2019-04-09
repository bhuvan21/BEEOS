import os
import bs4
import queue
import ebooklib
import threading
from ebooklib import epub

import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from Renderer import Renderer

from helperbee import helper
from device_info import set_password, set_home_image, set_lock_image


APP_NAME = "Settings"


Builder.load_file(helper.get_app_path() + APP_NAME + "/settings.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

SUBSETTINGS_CATEGORIES = ["Wifi", "Security", "Wallpaper", "Update Resources", "Brightness"]
BOOK_EXTENSIONS = ["epub"]
MUSIC_EXTENSIONS = ["mp3"]

FIRST = False

class SplashScreen(Screen):
    def entered(self):
        self.BACK_SCREEN = "Splash"
        self.parent.transition = FadeTransition()
        self.parent.get_screen("Main").entered()
        self.parent.current = "Main"

class SubSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BACK_SCREEN = "Main"
    
    def entered(self):
        box = self.children[0].children[0]
        #box.add_widget(Renderer())
        for category in SUBSETTINGS_CATEGORIES:
            button = Button(on_press=self.goto_subsetting)
            button.size_hint = (None, None)
            button.size = (480, 40)
            button.text = category
            box.add_widget(button)
        box.add_widget(Label())
    
    def goto_subsetting(self, instance):
        self.parent.transition = FadeTransition()
        self.parent.get_screen(instance.text).entered()
        self.parent.current = instance.text

class WifiScreen(Screen):
    def entered(self):
        self.BACK_SCREEN = "Main"
        self.keyboard = Window.request_keyboard(
            self.keyboard_close, self)

        self.scroll = self.children[0].children[1]
        self.input = self.children[0].children[2]
        self.connected_to = self.children[0].children[3]
        self.connected_to.text = self.connected_to.text.split(":")[0] + ": " + helper.wifi.get_current_ssid()
        
        
        self.button_ids = []

        for network in helper.wifi.get_all_ssids():
            button = Button(on_press=self.connect_to_ssid)
            button.text = network
            self.scroll.children[0].add_widget(button)
        
        Clock.schedule_interval(self.update_connection_display, 2)

    def keyboard_close(self):
        self.keyboard = None

    def connect_to_ssid(self, instance):
        helper.wifi.mobile_connect(instance.text, self.input.text)
    
    def update_connection_display(self, dt):
        ssids = helper.wifi.get_all_ssids()
        current = helper.wifi.get_current_ssid()
        
        self.scroll.children[0].children = []

        for network in ssids:
            button = Button(on_press=self.connect_to_ssid)
            button.text = network
            self.scroll.children[0].add_widget(button)
        
        self.connected_to.text = self.connected_to.text.split(":")[0] + ": " + helper.wifi.get_current_ssid()
    
    def leaving(self):
        print("stopping")
        Clock.unschedule(self.update_connection_display)
        self.keyboard_close()


class SecurityScreen(Screen):
    def entered(self):
        self.BACK_SCREEN = "Main"
        self.keyboard = Window.request_keyboard(
            self.keyboard_close, self)
        
        self.button = self.children[0].children[2].children[0].children[0]
        self.button.on_press = self.change_password
        self.input = self.children[0].children[2].children[0].children[1]
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
    
    def leaving(self):
        self.keyboard_close()

class WallpaperScreen(Screen):
    def entered(self):
        self.BACK_SCREEN = "Main"
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
        self.BACK_SCREEN = "Main"
        self.refresh_button = self.children[0].children[1]
        self.refresh_button.on_press = self.refresh
        self.warning = self.children[0].children[0]
    
    def refresh(self):
        mail = helper.email.checkMail()
        if mail[1] != None:
            filename = helper.email.get_attachment_filename(mail[1])
            extension = filename.split(".")[-1]
            if extension in BOOK_EXTENSIONS:
                directory = "/books/"
            elif extension in MUSIC_EXTENSIONS:
                directory = "/music/"
            else:
                directory = "/other/"
            fp = helper.email.save_attachment(mail[1], download_folder="/" + "/".join(os.getcwd().split("/")[1:-1]) + directory)
            if directory == "/books/":
                self.parent.transition = FadeTransition()
                self.parent.get_screen("ProcessBook").filepath = fp
                self.parent.get_screen("ProcessBook").entered()
                self.parent.current = "ProcessBook"


class ProcessBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filepath = ""

    def entered(self):
        self.BACK_SCREEN = "Update Resources"
        self.thread = threading.Thread(target=self.format_book)
        self.thread.setDaemon(True)
        self.queue = queue.Queue()
        self.thread.start()
        self.update_progress(1)
        Clock.schedule_interval(self.update_progress, .1)
    
    def format_book(self):

        self.info = self.children[0].children[1].children[0]
        self.progress = self.children[0].children[2].children[0]
        
        self.queue.put("0:100:Reading EPUB")
        pub = epub.read_epub(self.filepath)
        self.queue.put("100:100:Reading EPUB")
        docs = [d for d in pub.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
        self.queue.put("0:{}:Extracting relevant HTML".format(len(docs)))
        html_text = ""
        for i, d in enumerate(docs):
            html_text += d.get_body_content().decode()
            self.queue.put("{}:{}:Extracting relevant HTML".format(i, len(docs)))

        whole_text = ""
        self.queue.put("0:100:Making the Soup - might take a while")
        strainer = bs4.SoupStrainer("p")
        self.queue.put("20:100:Making the Soup - might take a while")
        soup = bs4.BeautifulSoup(html_text, "lxml", parse_only=strainer)
        self.queue.put("100:100:Soup made!")
        paras = [p for p in soup.find_all("p")]
        self.queue.put("0:{}:Extracting text".format(len(paras)))

        whole_text = ""
        for i, para in enumerate(paras):
            if para.text != "":
                whole_text += para.text + "\n"
            if i %100 == 0:
                self.queue.put("{}:{}:Extracting text".format(i, len(paras)))

        self.queue.put("0:100:Writing to disk...")
        path_to_save = helper.get_app_path() + "Reader/texts/{}.txt".format(self.filepath.split("/")[-1].split(".")[0])
        with open(path_to_save, "w") as f:
            f.write(whole_text)

        
        self.queue.put("100:100:All done! Feel free to leave.")

    def update_progress(self, dt):
        reading = None
        while True:
            try:
                reading = self.queue.get(block=False)
            except queue.Empty:
                break
        if reading is None:
            return
        
        self.progress.max = int(reading.split(":")[1])
        self.progress.value = int(reading.split(":")[0])
        self.info.text = reading.split(":")[2]




class BrightnessScreen(Screen):
    def entered(self):
        self.BACK_SCREEN = "Main"

        self.warning = self.children[0].children[1]
        self.set_button = self.children[0].children[2].children[0]
        self.slider = self.children[0].children[3].children[0]
        self.slider.max = 255
        self.slider.min = 0
        self.slider.step = 1

        self.set_button.on_press = self.set_brightness
    
    def set_brightness(self):
        val = self.slider.value
        self.warning.text = "Set brightness to {}/255".format(int(val))
        helper.set_display_brightness(val)


class SettingsScreenManager(ScreenManager):
    def on_enter(self):
        global FIRST
        if not FIRST:
            self.get_screen("Splash").entered()
            FIRST = True


controller = SettingsScreenManager()
controller.add_widget(SplashScreen(name="Splash"))
controller.add_widget(SubSettingsScreen(name="Main"))
controller.add_widget(WifiScreen(name="Wifi"))
controller.add_widget(SecurityScreen(name="Security"))
controller.add_widget(WallpaperScreen(name="Wallpaper"))
controller.add_widget(UpdateResourcesScreen(name="Update Resources"))
controller.add_widget(ProcessBookScreen(name="ProcessBook"))
controller.add_widget(BrightnessScreen(name="Brightness"))


def get_app():
    return controller

def get_icon():
    return "newicon.png"

import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

import helperbee

import xml.etree.ElementTree as ET
import threading
import requests
import queue

APP_NAME = "BEEStore"


Builder.load_file(helperbee.HelperBEE.get_path() + "/apps/" + APP_NAME + "/BEEStore.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.applist_queue = queue.Queue()
        self.thread = threading.Thread(None, self.get_applist)
        self.thread.setDaemon(True)
    
    def entered(self):
        self.thread.start()

        while True:
            read = None
            try:
                read = self.applist_queue.get(block=False)
            except queue.Empty:
                pass
            if read is not None:
                self.xml = read
                break

        self.parent.transition = FadeTransition()
        self.parent.get_screen("AllApps").xml = self.xml
        self.parent.get_screen("AllApps").entered()
        self.parent.current = "AllApps"

    def get_applist(self):
        xml = ET.fromstring(requests.get("https://raw.githubusercontent.com/bhuvan21/BEEStore/master/main.xml").text)
        self.applist_queue.put(xml)

class AllAppsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        n = 0
        grid = self.children[0].children[0]
        for app in self.xml:
            n += 1

            if n%2 == 0:
                grid.height = 200 + n*200

            for child in app:
                if child.tag == "iconurl":
                    iconurl = child.text
                elif child.tag == "name":
                    name = child.text

            button = Button(on_press=self.goto_detail)
            button.size_hint = (None, None)
            button.size = (200, 200)
            
            layout = BoxLayout()
            layout.pos = (button.pos[0]+70, (grid.height - button.pos[1]) - 50 - 200)
            layout.size = button.size
            layout.orientation = "vertical"
            img = AsyncImage(source=iconurl)
            img.size_hint_x = None
            img.width = 100
            
            lbl = Label(text=name, color=[1, 1, 1, 1], size_hint=(None, None), pos=(button.pos[0], button.pos[1]))
            layout.add_widget(img)
            layout.add_widget(lbl)
            button.add_widget(layout)
            
            self.children[0].children[0].add_widget(button)
    
    def goto_detail(self, instance):
        name = instance.children[0].children[0].text
        for a in self.xml:
            for child in a:
                if child.tag == "name" and child.text == name:
                    app = a
        
        self.parent.transition = FadeTransition()
        self.parent.get_screen("DetailApp").app = app
        self.parent.get_screen("DetailApp").entered()
        self.parent.current = "DetailApp"

class DetailAppScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        root = self.children[0]
        details = root.children[2]
        desc = root.children[1]
        button = root.children[0]
        icon = details.children[1]
        name = details.children[0].children[2]
        author = details.children[0].children[1]
        date = details.children[0].children[0]
        name.text = self.app.findall("name")[0].text
        author.text = self.app.findall("author")[0].text
        date.text = self.app.findall("releasedate")[0].text
        icon.source = self.app.findall("iconurl")[0].text

class BEEStoreScreenManager(ScreenManager):
    def on_enter(self):
        self.get_screen("Main").entered()



controller = BEEStoreScreenManager()
main = MainScreen(name="Main")
main.children[0].children[1].source = helperbee.HelperBEE.get_path() + "/images/UI/loading.gif"
controller.add_widget(main)
controller.add_widget(AllAppsScreen(name="AllApps"))
controller.add_widget(DetailAppScreen(name="DetailApp"))

def get_app():
    return controller

def get_icon():
    return "icon.png"

#MAKE THIS APP ACTUALLY WORK
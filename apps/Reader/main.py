import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from helperbee import helper

import xml.etree.ElementTree as ET
import threading
import requests
import queue
import subprocess

APP_NAME = "Reader"
FIRST = False


Builder.load_file(helper.get_app_path() + APP_NAME + "/reader.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


class BooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        n = 0
        grid = self.children[0].children[0]
        grid.clear_widgets()
        self.books = []
        for b in self.books:
            n += 1

            if n%2 == 0:
                grid.height = 200 + n*200

            button = Button(on_press=self.goto_read)
            button.size_hint = (None, None)
            button.size = (200, 200)
            
            layout = BoxLayout()
            layout.pos = (button.pos[0]+70, (grid.height - button.pos[1]) - 50 - 200)
            layout.size = button.size
            layout.orientation = "vertical"
            '''
            img = AsyncImage(source=iconurl)
            img.size_hint_x = None
            img.width = 100
            '''

            lbl = Label(text=name, color=[1, 1, 1, 1], size_hint=(None, None), pos=(button.pos[0], button.pos[1]))
            layout.add_widget(img)
            layout.add_widget(lbl)
            button.add_widget(layout)
            
            self.children[0].children[0].add_widget(button)
    
    def goto_read(self, instance):
        #TODO

class ReadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def entered(self):
        pass
    
    def leaving(self):
        pass
        


class BEEStoreScreenManager(ScreenManager):
    def on_enter(self):
        if not FIRST:
            self.get_screen("Splash").entered()
            FIRST = True



controller = BEEStoreScreenManager()
main = BooksScreen(name="Splash")
#main.children[0].children[1].source = helper.get_bee_path() + "/images/UI/loading.gif"
controller.add_widget(main)
controller.add_widget(ReadScreen(name="Read"))

def get_app():
    return controller

def get_icon():
    return "icon.png"
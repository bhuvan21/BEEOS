import os
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from MusicBEE import player
from helperbee import helper

APP_NAME = "Music"
FIRST = False

Builder.load_file(helper.get_app_path() + APP_NAME + "/music.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


class ChoicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def entered(self):
        self.grid = self.children[0].children[1].children[0].children[0]
        self.playlist = self.children[0].children[2].children[0]
        self.pause_button = self.children[0].children[0].children[0]
        self.pause_button.on_press = self.toggle_pause
        self.song_name = self.children[0].children[0].children[1]
        self.song_name.text = "Not Playing"
        self.paused = True
        self.pause_button.text = ">"

        song_filenames = os.listdir(helper.get_resources_path() + "/music/")
        for song in song_filenames:
            b = Button(on_press=self.play_song)
            b.text = ".".join(song.split(".")[:-1])
            self.grid.add_widget(b)
        self.grid.add_widget(Label())
    
    def play_song(self, instance):
        filename = instance.text + ".mp3"
        player.play_song(filename)
        print("playing", filename)
        self.song_name.text = instance.text
    
    def toggle_pause(self):
        if self.song_name.text != "Not Playing":
            if self.paused:
                self.pause_button.text = ">"
                self.paused = False
            else:
                self.pause_button.text = "||"
                self.paused = True
            player.pause()



class MusicScreenManager(ScreenManager):
    def on_enter(self):
        global FIRST
        if not FIRST:
            self.get_screen("Main").entered()
            FIRST = True

controller = MusicScreenManager()
controller.add_widget(ChoicesScreen(name="Main"))

def get_app():
    return controller

def get_icon():
    return "icon.png"

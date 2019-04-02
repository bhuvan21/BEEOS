import os
os.environ['KIVY_IMAGE'] = 'sdl2,pil'

import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.carousel import Carousel
from kivy.graphics import Line, Ellipse
from kivy.uix.screenmanager import Screen, ScreenManager, RiseInTransition

import queue
import datetime
import threading
import importlib.util
from copy import deepcopy


import device_info
from helperbee import helper


Builder.load_file("beeos.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

class PINLockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cancel_button = Button(background_color=[0, 0, 0, 0],
                               size_hint=[None, None],
                               pos=[340, 30],
                               size=[100, 30],
                               text="Cancel"
                               )
        self.add_widget(self.cancel_button)

        self.children[1].bind(on_press=self.PINCallback)
        for button in self.children[2].children:
            button.bind(on_press=self.PINCallback)

        self.switch_to_home = print
        self.dots = []
        self.password = ""

        self.draw_empty_dots()
    
    def draw_empty_dots(self):
        for dot in self.dots:
            self.canvas.remove(dot)
        self.dots = []
        with self.canvas:
            for i in range(6):
                x = 103+(54.8*i)
                self.dots.append(Line(circle=(x, 650, 10)))
    
    def shake_screen(self):
        anim = Animation(x=50, duration=0.05)
        for i in range(3):
            anim += (Animation(x=-50, duration=0.1) + Animation(x=50, duration=0.1))
        anim += Animation(x=0, duration=0.05)
        anim.start(self)

    def PINCallback(self, instance):
        button_number = instance.background_down.split("/")[-1].split(".")[0][0]
        if len(self.password) < 6:
            self.password += button_number

            dot = self.dots[len(self.password)-1]
            self.canvas.remove(dot)
            position = (103+((len(self.password)-1)*54.8)-10, 650-10)
            
            with self.canvas:
                self.dots[len(self.password)-1] = Ellipse(pos=position, size=(20, 20))
        
        if len(self.password) == 6:
            if self.password == device_info.get_password():
                self.switch_to_home()
            else:
                self.draw_empty_dots()
                self.password = ""
                self.shake_screen()
    
        
        
class RestingLockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_datetime, 1)

    def update_datetime(self, dt):
        self.children[0].children[2].text = datetime.datetime.now().strftime("%H:%M")
        self.children[0].children[1].text = datetime.datetime.now().strftime("%A %-d %B")

class LockCarousel(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        screen1 = PINLockScreen(name="PINLockScreen")
        screen1.cancel_button.bind(on_press=self.load_next)
        self.add_widget(screen1)
        self.add_widget(RestingLockScreen(name="RestingLockScreen"))

class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = Image(source=device_info.get_lock_image())
        self.add_widget(self.bg)
        self.add_widget(LockCarousel())
    
    def ready(self):
        self.bg.source = device_info.get_lock_image()
        
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = Image(source=device_info.get_home_image())
        self.add_widget(self.bg)
        self.names = [app for app in os.listdir(os.getcwd()+"/apps/") if app[0] != "."]
        self.paths = [os.getcwd() + "/apps/" + app for app in self.names]
        self.apps = []
        
            
    def ready(self, parent):
        Clock.schedule_interval(self.check_buttons, 0.1)
        self.bg.source = device_info.get_home_image()
        for i in range(len(self.names)-1, -1, -1):
            name = self.names[i]
            path = self.paths[i]

            app = {"name": name, "path": path}
            
            spec = importlib.util.spec_from_file_location(name, path + "/main.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            app["module"] = module
            app["sm"] = module.get_app()
            app["icon"] = path + "/" + module.get_icon()
            self.apps.append(app)
            
            screen = Screen(name=name)
            screen.add_widget(app["sm"])
            screen.background_color = [0, 0, 0, 1]
            try:
                screen.on_enter = app["sm"].on_enter
            except AttributeError:
                pass
            parent.add_widget(screen)
        print(self.apps)
        
        self.realparent = parent

        x = 42.5
        y = 600
        
        for app in self.apps:
            if x > 400:
                x = 42.5
                y -= 145

            button = Button(background_color=[0, 0, 0, 0],
                        size_hint=[None, None],
                        pos=[x, y],
                        text=app["name"],
                        color=[0, 0, 0, 0])
            img = Image(source=app["icon"], pos=(x-240+50, y-400+50))
            app["button"] = [button, img]
            button.bind(on_press=self.openapp)
            self.add_widget(button)
            self.add_widget(img)

            x += 147.5
            
    def openapp(self, instance):
        print(instance.text)
        self.realparent.current = instance.text
        self.current_app = instance.text

        

    def check_buttons(self, dt):
        if helper.sensors.get_home_button():
            self.realparent.current = "Home"
        elif helper.sensors.get_back_button():
            #self.realparent.current = self.realparent.previous()
            current = self.realparent.current
            app_names = [a["name"] for a in self.apps]
            if current in app_names:
                sm = self.realparent.get_screen(self.realparent.current).children[0]
                sm.current = sm.previous()
            else:
                self.realparent.current = "Home"



controller = ScreenManager()

def home_screen():
    controller.transition = RiseInTransition()
    controller.current = "Home"

lock_screen = LockScreen(name="Lock")
lock_screen.children[0].children[0].children[0].switch_to_home = home_screen
controller.add_widget(lock_screen)
controller.add_widget(HomeScreen(name="Home"))
controller.get_screen("Home").ready(controller)

'''
input_queue = queue.Queue()
input_thread = threading.Thread(None, get_presses)
input_thread.setDaemon(True)
input_thread.start()

def get_presses():
    #TODO add to queue if button's pressed


def input_manager():
    #TODO check input_queue and make relevant actions

Clock.schedule_interval(input_manager, 0.1)
'''

class BEEOSApp(App):
    def build(self):
        return controller

if __name__ == '__main__':
    app = BEEOSApp()
    app.run()
    
import os
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from helperbee import helper
from EPUBEE import EPUBEE


APP_NAME = "Reader"
FIRST = False


Builder.load_file(helper.get_app_path() + APP_NAME + "/reader.kv")
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


class BooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BACK_SCREEN = "Splash"
        if "covers" not in os.listdir(helper.get_app_path() + APP_NAME + "/"):
            os.mkdir(helper.get_app_path() + APP_NAME + "/covers")
        if "texts" not in os.listdir(helper.get_app_path() + APP_NAME + "/"):
            os.mkdir(helper.get_app_path() + APP_NAME + "/texts")
    
    def entered(self):
        grid = self.children[0].children[0]
        grid.clear_widgets()
        
        self.books = []
        self.book_filepaths = [helper.get_resources_path() + "/books/" + b for b in os.listdir(helper.get_resources_path() + "/books/")]
        self.titles = []
        if self.book_filepaths == []:
            grid.add_widget(Label(text="No books found :("))
        
        n = 0
        for b in self.book_filepaths:
            n += 1
            if n%2 == 0:
                grid.height = 200 + n*200
        
        n = 0
        for b in self.book_filepaths:
            n += 1

            button = Button(on_press=self.goto_read)
            button.size_hint = (None, None)
            button.size = (200, 200)
            self.children[0].children[0].add_widget(button)

            layout = BoxLayout()
            button.add_widget(layout)
            x = ((1-(n%2))*240) + 70
            y = grid.height - ((((n-1)/2) - (((n-1)/2)%1)) * 240) - 250
            layout.pos = (x, y)
            layout.size = button.size
            layout.orientation = "vertical"

            self.book_filename = b.split("/")[-1].split(".")[0]
            book = EPUBEE(b)
            cover = book.get_cover()
            
            if cover != "":
                cover_path = helper.get_app_path() + APP_NAME + "/covers/" + self.book_filename + ".jpeg"
                cover.save(cover_path)
                self.books.append(book)

                img = Image(source=cover_path)
                img.size_hint_x = None
                img.width = 100
                img.height = 100
            
            if len(book.title) > 18:
                text = book.title[:15] + "..."
            else:
                text = book.title
            self.titles.append(text)
            
            lbl = Label(text=text, color=[.5, .5, .5, 1], size_hint=(None, None), pos=(button.pos[0], button.pos[1]))
            if cover != "":
                layout.add_widget(img)
                print("adding")

            layout.add_widget(lbl)
            
            
            
    
    def goto_read(self, instance):
        print(self.books, instance.children[0].children[0].text, self.book_filename)
        self.book_filepaths[self.titles.index(instance.children[0].children[0].text)]
        self.parent.get_screen("Read").book = self.books[self.titles.index(instance.children[0].children[0].text)]
        epub_filename = self.book_filepaths[self.titles.index(instance.children[0].children[0].text)]
        self.parent.get_screen("Read").book_filename = epub_filename.split("/")[-1].split(".")[0]
        self.parent.get_screen("Read").entered()
        self.parent.current = "Read"

class ReadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book = None
        self.book_filename = None
        self.BACK_SCREEN = "Splash"
    
    def entered(self):
        self.page = 1
        self.book_label = self.children[0].children[1].children[0].children[0]
        self.scroll = self.children[0].children[1].children[0]
        with open(helper.get_app_path() + APP_NAME + "/texts/" + self.book_filename + ".txt") as f:
            text = f.read()
        self.pages = [text[i:i+5000] for i in range(0, len(text), 5000)]
        self.book_label.text = self.pages[0]
        self.progress_label = self.children[0].children[0].children[2]
        self.progress_label.text = "{}/{}".format(self.page, len(self.pages))
        self.previous_page = self.children[0].children[0].children[1]
        self.previous_page.on_press = self.show_previous_page
        self.next_page = self.children[0].children[0].children[0]
        self.next_page.on_press = self.show_next_page

    
    def show_next_page(self):
        if self.page != len(self.pages):
            self.page += 1
            self.book_label.text = self.pages[self.page-1]
            self.progress_label.text = "{}/{}".format(self.page, len(self.pages))
            self.scroll.scroll_y = 1

    def show_previous_page(self):
        if self.page != 1:
            self.page -= 1
            self.book_label.text = self.pages[self.page-1]
            self.progress_label.text = "{}/{}".format(self.page, len(self.pages))
            self.scroll.scroll_y = 0
    
        


class ReaderScreenManager(ScreenManager):
    def on_enter(self):
        global FIRST
        if not FIRST:
            self.get_screen("Splash").entered()
            FIRST = True



controller = ReaderScreenManager()
main = BooksScreen(name="Splash")
controller.add_widget(main)
controller.add_widget(ReadScreen(name="Read"))

def get_app():
    return controller

def get_icon():
    return "icon.png"

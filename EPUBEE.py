import io
import re
import PIL
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import bs4

class EPUBEE():
    def __init__(self, filename):
        self.filename = filename
        self.epub = epub.read_epub(filename)
        self.title = self.epub.get_metadata("DC", "title")[0][0]
        self.author = self.epub.get_metadata("DC", "creator")[0][0]
        self.documents = [d for d in self.epub.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
        
    def get_cover(self):    
        self.images = [d for d in self.epub.get_items_of_type(ebooklib.ITEM_IMAGE)]
        try:
            cover = self.images[0]
        except IndexError:
            print(self.title, self.filename)
            return ""
        self.cover = PIL.Image.open(io.BytesIO(cover.get_content()))
        return self.cover

    def get_whole_text(self):
        self.html_text = ""
        print("Going through {} documents".format(len(self.documents)))
        for d in self.documents:
            self.html_text += d.get_body_content().decode()
        self.whole_text = ""
        print("Making the Soup")
        strainer = bs4.SoupStrainer("p")
        soup = BeautifulSoup(self.html_text, "lxml", parse_only=strainer)
        print("Soup made!")
        n = 0
        for para in soup.find_all("p"):
            if para.text != "":
                self.whole_text += para.text + "\n"
            n += 1
            if n %100 == 0:
                print(n)
        return self.whole_text
    
    def get_pages(self):
        text = self.get_whole_text()
        return [text[i:i+5000] for i in range(0, len(text), 5000)]

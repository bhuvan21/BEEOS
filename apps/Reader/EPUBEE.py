import io
import Image
import ebooklib

from ebooklib import epub



class EPUBEE():
    def __init__(self, filename):
        self.epub = epub.read_epub(filename)
        self.title = self.epub.get_metadata("DC", "title")[0][0]
        self.author = self.epub.get_metadata("DC", "author")[0][0]
        self.documents = [d for d in self.epub.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
        
    def get_cover(self):    
        self.images = [d for d in self.epub.get_items_of_type(ebooklib.ITEM_IMAGE)]
        cover = self.images[0]
        self.cover = Image.open(io.BytesIO(cover.get_content()))
        return self.cover

    def get_whole_text(self):
        self.wholetext = ""
        for d in self.documents:
            self.wholetext += d.get_body_content()
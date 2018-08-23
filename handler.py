"""Creates a ContentHandler for the SAX parser to handle the wiki dump"""
from xml.sax.handler import ContentHandler
from processor import process_text, process_title

class WikiHandler(ContentHandler):
    """Class to handle the wiki dump through SAX parser"""

    def __init__(self):
        self.ran_flag = 1
        self.id = []
        self.id_tmp = ""
        self.id_flag = 0
        self.title = []
        self.title_tmp = ""
        self.title_flag = 0
        self.external_links = []
        self.references = []
        self.body = []
        self.infobox = []
        self.categories = []
        self.text_tmp = ""
        self.text_flag = 0

    def startDocument(self):
        print("Starting document parsing")

    def endDocument(self):
        print("Finished parsing document")

    def startElement(self, name, attrs):
        if name == "revision" or name == "contributor":
            self.ran_flag = 0
        if name == "id" and self.ran_flag == 1:
            self.id_flag = 1
        if name == "title":
            self.title_flag = 1
        elif name == "text":
            self.text_flag = 1

    def endElement(self, name):
        if name == "revision" or name == "contributor":
            self.ran_flag = 1
        if name == "id" and self.ran_flag == 1:
            self.id_flag = 0
            self.id.append(self.id_tmp)
            self.id_tmp = ""
        elif name == "title":
            self.title_flag = 0
            self.title.append(process_title(self.title_tmp.encode('utf-8')))
            self.title_tmp = ""
        elif name == "text":
            self.text_flag = 0
            external_links, references, body, infobox, categories = process_text(
                self.text_tmp.encode('utf-8'))
            self.external_links.append(external_links)
            self.references.append(references)
            self.body.append(body)
            self.infobox.append(infobox)
            self.categories.append(categories)
            self.text_tmp = ""

    def characters(self, content):
        if self.id_flag == 1 and self.ran_flag == 1:
            self.id_tmp += content
        if self.title_flag == 1:
            self.title_tmp += content
        if self.text_flag == 1:
            self.text_tmp += content

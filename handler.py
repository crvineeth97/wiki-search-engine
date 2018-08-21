"""Creates a ContentHandler for the SAX parser to handle the wiki dump"""
from xml.sax.handler import ContentHandler

class WikiHandler(ContentHandler):
    """Class to handle the wiki dump through SAX parser"""
    title = ""

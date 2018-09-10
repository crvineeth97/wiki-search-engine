"""Creates a ContentHandler for the SAX parser to handle the wiki dump"""
import io
from os import mkdir, path
from collections import defaultdict
from xml.sax.handler import ContentHandler
from processor import process_text, process_title
import config


class WikiHandler(ContentHandler):
    """Class to handle the wiki dump through SAX parser"""

    def __init__(self):
        self.docs_length = 0
        self.title_tmp = ""
        self.title_flag = 0
        self.text_tmp = ""
        self.text_flag = 0
        self.fields = ["b", "c", "e", "i", "r", "t"]
        self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def dump_index(self):
        if not path.exists(config.TEMP_OUT_DIR):
            mkdir(config.TEMP_OUT_DIR)
        out_file = config.TEMP_OUT_DIR + \
            str(self.docs_length / config.MAX_DOCS_IN_MEMORY)
        words = sorted(self.index.keys())
        with io.open(out_file, "w", encoding="utf-8") as f:
            for word in words:
                line = word + '|'
                docs = sorted(self.index[word])
                for doc_id in docs:
                    line += str(doc_id) + '|'
                    for field in self.fields:
                        line += str(self.index[word][doc_id][field]) + '|'
                line = line[:-1] + '\n'
                f.write(unicode(line))
        self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def startDocument(self):
        print "Starting document parsing"

    def endDocument(self):
        print "Finished parsing document"

    def startElement(self, name, attrs):
        if name == "title":
            self.title_flag = 1
        elif name == "text":
            self.text_flag = 1

    def endElement(self, name):
        if name == "page":
            self.docs_length += 1
            if self.docs_length % config.MAX_DOCS_IN_MEMORY == 0:
                self.dump_index()
        if name == "title":
            self.title_flag = 0
            title = process_title(self.title_tmp.encode('utf-8'))
            for word in title:
                self.index[word][self.docs_length]["t"] += 1
            self.title_tmp = ""
        elif name == "text":
            self.text_flag = 0
            fields = process_text(self.text_tmp.encode('utf-8'))
            # print fields
            for field, val in fields.iteritems():
                for word in val:
                    self.index[word][self.docs_length][field] += 1
            self.text_tmp = ""

    def characters(self, content):
        if self.title_flag == 1:
            self.title_tmp += content
        if self.text_flag == 1:
            self.text_tmp += content

"""Wikipedia Search Engine

This file takes as input a path to the wiki dump
and the name of an output file to which the inverted indices are written.
The wiki dump is parsed using a SAX XML Parser
Usage: python main.py <path-to-wiki-dump> <inverted-index-out-file>
"""
import sys
from xml.sax import make_parser
from handler import WikiHandler
from inverted_index import create_inverted_index
from merger import merge

def main():
    """Main function which is called first"""
    if len(sys.argv) < 3:
        print "Usage: python indexer.py <path-to-wiki-dump> <inverted-index-out-file>"
        return 1
    handler = WikiHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    dump = open(sys.argv[1], "r")
    parser.parse(dump)
    merge(handler.temp_files_length, sys.argv[2], handler.docs_length)

if __name__ == "__main__":
    main()

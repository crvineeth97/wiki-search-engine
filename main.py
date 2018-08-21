"""Wikipedia Search Engine

This file is the main file of the project. It takes as input a path to the wiki dump
and the name of an output file to which the inverted indices are written.
The wiki dump is parsed using a SAX XML Parser
Usage: python3 main.py <path-to-wiki-dump> <inverted-index-out-file>
"""
import sys
from xml.sax import make_parser

def main():
    """Main function which is called first"""
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <path-to-wiki-dump> <inverted-index-out-file>")
    # Need to write up a handler
    handler = 1
    parser = make_parser()
    parser.setContentHandler(handler)
    dump = open(sys.argv[1], "r")
    parser.parse(dump)
    outfile = str(sys.argv[2])
    with open(outfile, "w") as f:
        f.write("\n")

if __name__ == "__main__":
    main()

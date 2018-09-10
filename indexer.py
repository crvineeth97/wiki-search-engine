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

def main():
    """Main function which is called first"""
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <path-to-wiki-dump> <inverted-index-out-file>")
        return 1
    # Need to write up a handler
    handler = WikiHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    dump = open(sys.argv[1], "r")
    parser.parse(dump)
    # inverted_indices = create_inverted_index(handler)
    # outfile = str(sys.argv[2])
    # with open(outfile, "w") as f:
    #     for i in sorted(inverted_indices.keys()):
    #         f.write(i)
    #         f.write(" ")
    #         f.write(inverted_indices[i])
    #         f.write("\n")

if __name__ == "__main__":
    main()

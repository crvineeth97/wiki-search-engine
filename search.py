import sys
from collections import defaultdict
from operator import itemgetter
from datetime import datetime
from linecache import getline
from os import path
from processor import process_title
import config

def binary_search(file, word):
    with open(file, "r") as fin:
        left, right = 0, path.getsize(file) - 1
        key = None
        while key != word and left <= right:
            mid = (left + right) / 2
            fin.seek(mid)
            fin.readline()
            line = fin.readline().split("|")
            key = line[0]
            if word > key:
                left = mid + 1
            else:
                right = mid - 1
        if key != word:
            return None
        return line[1:]

def search(query, index_file):
    result = []
    for word in query:
        res = defaultdict(float)
        line = binary_search(index_file, word)
        if line is None:
            print "Word + \"" + word + "\" not found. Continuing..."
        else:
            for doc in line:
                tf_idf = float(doc.split("z")[1])
                for field in config.FIELDS:
                    doc_id = doc.split(field)[0]
                    try:
                        int(doc_id)
                        break
                    except ValueError:
                        continue
                res[int(doc_id)] += tf_idf
            result.append(res)
    if len(result) > 1:
        final = result[0].viewkeys() & result[1].viewkeys()
    elif len(result) == 1:
        final = result[0].viewkeys()
    else:
        print "No documents related to query found"
        return
    for i in range(2, len(result)):
        final = final & result[i].viewkeys()
    res = defaultdict(float)
    for key in final:
        for i in range(len(result)):
            res[key] += result[i][key]
    for (key, val) in sorted(res.items(), key=itemgetter(1), reverse=True)[:10]:
        title = getline(config.TITLE_FILE, key + 1)
        print title,



def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <inverted-index-file>")
        return 1
    print "Welcome to Wiki Search Engine\nTo search for a query, type the query after the prompt\
        \nThe top 10 relevant documents will be presented\nTo exit the prompt, use Ctrl+c"
    index_file = sys.argv[1]
    while True:
        query = raw_input("\nQuery >> ")
        start_time = datetime.now()
        search(process_title(query.encode("utf-8")), index_file)
        end_time = datetime.now()
        print "\n" + str((end_time - start_time).total_seconds()) + " seconds"

if __name__ == "__main__":
    main()

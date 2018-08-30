from collections import defaultdict

def create_inverted_index(handler):
    doc_length = len(handler.id)
    inverted_index = defaultdict(str)
    for i in range(doc_length):
        title = defaultdict(int)
        external_links = defaultdict(int)
        references = defaultdict(int)
        body = defaultdict(int)
        infobox = defaultdict(int)
        categories = defaultdict(int)
        for word in handler.title[i]:
            title[word] += 1
        for word in handler.external_links[i]:
            external_links[word] += 1
        for word in handler.references[i]:
            references[word] += 1
        for word in handler.body[i]:
            body[word] += 1
        for word in handler.infobox[i]:
            infobox[word] += 1
        for word in handler.categories[i]:
            categories[word] += 1
        vocabulary = list(set(title.keys()+body.keys()+infobox.keys() +
                              categories.keys()+external_links.keys()+references.keys()))
        for word in vocabulary:
            temp = ""
            temp += str(handler.id[i]) + " "
            if title[word]:
                temp += "t" + str(title[word]) + " "
            if body[word]:
                temp += "b"+str(body[word])+" "
            if infobox[word]:
                temp += "i"+str(infobox[word])+" "
            if categories[word]:
                temp += "c"+str(categories[word])+" "
            if external_links[word]:
                temp += "e"+str(external_links[word])+" "
            if references[word]:
                temp += "r"+str(references[word])
            if inverted_index[word]:
                inverted_index[word] += "|" + temp
            else:
                inverted_index[word] = temp
    return inverted_index

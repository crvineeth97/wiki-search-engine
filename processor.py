"""Text Processing
"""
import re
from collections import defaultdict
from Stemmer import Stemmer

STOP_WORDS = defaultdict(int)
FP = open("stop_words.txt", "r")
for l in FP:
    l = l.strip()
    l = l.lower()
    STOP_WORDS[l] = 1
FP.close()

STEMMER = Stemmer("english")
TAGS = ["<sup>", "#REDIRECT", "format=", "dts", "dmy", "colspan", "</sup>", "<big>", "</big>",
        "<small>", "</small>", "</tr>", "<br>", "<br />", "<center>", "</center", "</abbr>",
        "<abbr", "<code>", "</code>", "<div>", "</div>", "<imagemap>", "</imagemap>",
        "<gallery>", "</gallery>"]

NOT_BODY = ["==See also==", "== See also ==", "== References ==", "==References and sources==",
            "==References==", "== Bibliography ==", "==External links==", "== External links ==",
            "{{Infobox", "[[Category"]

def stem(sentence):
    """Stems the sentence"""
    return([STEMMER.stemWord(key) for key in sentence])


def remove_stop_words(sentence):
    """Removes stop words from a sentence"""
    return([w for w in sentence if STOP_WORDS[w] != 1 and w != " "])


def tokenize(sentence):
    """Splits the sentence into tokens"""
    words = re.findall("[\w]+|\d+", sentence)
    for key in range(0, len(words)):
        if words[key] == "00":
            words[key] = "0"
    return([key.lower() for key in words])


def process_title(title):
    """Processes the title of a Wiki page"""
    data = tokenize(title)
    data = remove_stop_words(data)
    data = stem(data)
    return data


def get_external_links(text):
    """Find external links in a text"""
    data = text.split("==External links==")
    if len(data) <= 1:
        data = text.split("== External links ==")
    links = []
    if len(data) > 1:
        lines = data[1].split("\n")
        for line in lines:
            if ("* [" in line) or ("*[" in line):
                link = line.split(" ")
                words = [word for word in link if "http" not in word]
                links.append(' '.join(words))
        links = tokenize(' '.join(links))
        links = remove_stop_words(links)
        links = stem(links)
    return links


def get_references(text):
    """Find references in a Wiki page"""
    data = text.split("== References ==")
    references = []
    temp = ""
    if len(data) > 1:
        hlp = data[1][0:data[1].find('==')]
        if '*' not in hlp:
            return references
        lines = hlp.split("\n")
        for line in lines:
            if line == "" or line[0] != '*':
                continue
            if "title =" in line:
                words = re.findall('le =(.+?)\|', line)
                temp = (' '.join(words))
            elif "\'\'" in line:
                words = re.findall('\'\'(.+?)\'\'', line)
                temp = (' '.join(words))
            elif "\"" in line:
                words = re.findall('\"(.+?)\"', line)
                temp = (' '.join(words))
            words = temp.split(" ")
            words = [word for word in words if "http" not in word]
            references.append(' '.join(words))
        references = tokenize(' '.join(references))
        references = remove_stop_words(references)
        references = stem(references)
    return references


def get_infobox(text):
    """Get infobox"""
    data = text.split("\n")
    infobox = []
    for line in data:
        i = 0
        if("{{Infobox" in line):
            bracket_count = 0
            temp = line.split("{{Infobox")[1:]
            infobox.append(' '.join(temp))
            while i < len(data)-1:
                if "{{" in line:
                    bracket_count += line.count("{{")
                if "}}" in line:
                    bracket_count -= line.count("}}")
                if bracket_count <= 0:
                    break
                i += 1
                temp = re.sub("{{Infobox", "", line)
                temp = temp.split("|")
                words = []
                for word in temp:
                    tk = word.split('=')
                    if(len(tk) > 1):
                        words.append(tk[1])
                temp = ' '.join(words)
                words = temp.split(" ")
                word1 = [word for word in words if "http" not in word]
                infobox.append(' '.join(word1))
    infobox = tokenize(' '.join(infobox))
    infobox = remove_stop_words(infobox)
    infobox = stem(infobox)
    return infobox


def get_body(text):
    """Get Body"""
    data = text.split("\n")
    body = []
    ref_flag = 0
    for line in data:
        flag = 1
        for key in NOT_BODY:
            if key in line:
                flag = 0
            break
        if flag == 0:
            continue
        if "<ref" in line and "</ref>" in line:
            store = line.split("<ref")
            for ref in store:
                if "</ref>" in ref:
                    tok = ref.split("</ref>")
                    if len(tok) > 1:
                        body.append(tok[1])
                else:
                    body.append(ref)
        else:
            if "<ref" in line:
                ref_flag = 1
                tem = line.find("<ref")
                body.append(line[0:tem])
            if ref_flag == 0:
                if "|" in line and "=" in line:
                    tem2 = line.find("=")
                    line = line[tem2:]
                body.append(line)
            if "</ref>" in line:
                ref_flag = 0
                tem = line.find("</ref>")
                body.append(line[tem:])

    body = ' '.join(body)
    body = re.sub("<ref.*?/>", " ", body)
    body = body.split(" ")
    body = [word for word in body if "http" not in word]
    body = tokenize(' '.join(body))
    body = remove_stop_words(body)
    body = stem(body)
    return body


def get_categories(text):
    """Get Categories"""
    data = text.split("\n")
    categories = []
    for line in data:
        if "[[Category" in line:
            words = re.findall('\[\[Category:(.+?)\]\]', line)
            categories.append(' '.join(words))
    categories = tokenize(' '.join(categories))
    categories = remove_stop_words(categories)
    categories = stem(categories)
    return categories


def process_text(text):
    """Process the text of a Wiki page"""
    text = re.sub("_", "", text)
    text = re.sub(",", "", text)
    text = re.sub("<ref.*?/ref>", " ", text)
    text = re.sub("#([0-9a-fA-F]{6})", "", text)
    text = re.sub("style=.*?;\"", " ", text)
    text = re.sub("style=.*?\"", " ", text)
    text = re.sub("style=.*?;", " ", text)
    text = re.sub("width=.*?%\"", " ", text)
    text = re.sub("width=.*?\"", " ", text)
    text = re.sub("border=.*?\"", " ", text)
    text = re.sub("<!--.*?-->", " ", text)
    text = re.sub("File:.*?px\|", " ", text)
    text = re.sub("File:.*?upright\|", " ", text)
    text = re.sub("File:.*?right\|", " ", text)
    text = re.sub("File:.*?upleft\|", " ", text)
    text = re.sub("File:.*?left\|", " ", text)
    text = re.sub("File:.*?thumb\|", " ", text)
    text = re.sub("File:.*?png\||File:.*?PNG\|", " ", text)
    text = re.sub("File:.*?jpg\||File:.*?JPG\|", " ", text)
    text = re.sub("Image:.*?px\|", " ", text)
    text = re.sub("Image:.*?right\|", " ", text)
    text = re.sub("Image:.*?upright\|", " ", text)
    text = re.sub("Image:.*?upleft\|", " ", text)
    text = re.sub("Image:.*?left\|", " ", text)
    text = re.sub("Image:.*?thumb\|", " ", text)
    text = re.sub("Image:.*?png\||File:.*?PNG\|", " ", text)
    text = re.sub("Image:.*?jpg\||File:.*?JPG\|", " ", text)
    for tag in TAGS:
        text = re.sub(tag, " ", text)
    external_links = get_external_links(text)
    references = get_references(text)
    body = get_body(text)
    infobox = get_infobox(text)
    categories = get_categories(text)
    return (external_links, references, body, infobox, categories)

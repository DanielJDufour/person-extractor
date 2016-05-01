from nltk.chunk import _MULTICLASS_NE_CHUNKER
from nltk.data import load
from nltk.tag.perceptron import PerceptronTagger
from nltk import ne_chunk, word_tokenize
from os import listdir
from os.path import dirname, realpath
from re import findall, finditer, MULTILINE, UNICODE
from re import compile as re_compile
flags = MULTILINE|UNICODE


directory_of_this_file = dirname(realpath(__file__))


# load patterns
directory_of_patterns = directory_of_this_file + "/prep/patterns"
language_pattern = {}
for filename in listdir(directory_of_patterns):
    language = filename.split(".")[0]
    with open(directory_of_patterns + "/" + language + ".txt") as f:
        pattern_as_string = (f.read().decode("utf-8").strip())
        #print "p"
        #print pattern_as_string
        pattern = re_compile(pattern_as_string, flags=flags)
        language_pattern[language] = pattern

global tagger
tagger = None

global chunker
chunker = None

def loadTaggerIfNecessary():
    global tagger
    if tagger is None:
        tagger = PerceptronTagger()

def loadChunkerIfNecessary():
    global chunker
    if chunker is None:
        chunker = load(_MULTICLASS_NE_CHUNKER)

def flatten(lst):
    result = []
    for element in lst:
        if hasattr(element, '__iter__'):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result

def extract_people_quickly(text, language=None):

    if isinstance(text, str):
        text = text.decode("utf-8")

    people = set()
    if language:
        for mo in finditer(pattern, text):
            people.add(mo.group("person"))
    else:
        for pattern in language_pattern.values():
            print "pattern is"
            print pattern 
            for mo in finditer(pattern, text):
                people.add(mo.group("person"))

    return list(people)


def extract_person_quickly(text, language=None):
    return (extract_people_quickly(text, language=language) or [None])[0]

def extract_people_slowly(text, language=None):
    global tagger
    loadTaggerIfNecessary()
    global chunker
    loadChunkerIfNecessary()

    if isinstance(text, str):
        text = text.decode("utf-8")

    people = []
    for tree in chunker.parse(tagger.tag(word_tokenize(text))).subtrees():
        if tree.label() == "PERSON":
            people.append(" ".join([leaf[0] for leaf in tree.leaves()]))

    people = findall("(?:[A-Z][a-z]+ )?(?:" + "|".join(people) + ")(?: [A-Z][a-z]+)?", text)

    return people

def extract_person_slowly(text):
    return extract_people(text)[0]

def extract_people(text, language=None, speed="slowly"):
    if speed == "slowly":
        return extract_people_slowly(text, language)
    else:
        return extract_people_quickly(text, language)

def extract_person(text, language=None, speed="slowly"):
    return (extract_people(text, language, speed) or [None]) [0]

epq=extract_people_quickly
eps=extract_people_slowly

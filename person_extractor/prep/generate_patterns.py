# -*- coding: utf-8 -*-
from os.path import dirname, realpath
from os import listdir
import re, pickle
directory_of_this_file = dirname(realpath(__file__))
directory_of_keywords = directory_of_this_file + "/keywords/"
directory_of_patterns = directory_of_this_file + "/patterns/"

# load keywords from files into dictionary
# d[language][before/after/etc]
d = {}
for language in listdir(directory_of_keywords):
    d[language] = {}
    directory_of_language = directory_of_keywords + language + "/"
    for filename in listdir(directory_of_language):
        category = filename.split(".")[0]
        path_to_keywords_file = directory_of_language + filename
        with open(path_to_keywords_file) as f:
            keywords = f.read().decode("utf-8").splitlines()
            # sort keywords by length, because we want to match the longest ones first
        keywords = sorted(keywords, key=lambda x: -1*len(x))
        pattern = u"(?:" + u"|".join(keywords) + u")"
        d[language][category] = pattern

print "d is", d

language_person_pattern = {}

####
#### ENGLISH
####

d_en = d['English']
upper = u"[^\W\d_b-z:\u0621-\u06ff]"
lower = u"(?:[^\W\d_A-Z:\u0621-\u06ff]|')"
pattern = u"([A-Z][a-z]{3,15} ){0,5}" + d_en['before'] + " " + "(?P<person>[A-Z][a-z]{2,15}( [A-Z][a-z]{2,15}){0,2})"
language_person_pattern['English'] = pattern

# write all patterns to their respective files
for language, pattern in language_person_pattern.iteritems():
    with open(directory_of_patterns + "/" + language + ".txt", "wb") as f:
        f.write(pattern.encode("utf-8"))


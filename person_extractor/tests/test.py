#-*- coding: utf-8 -*-
import unittest
from person_extractor import *

class TestMethods(unittest.TestCase):

    def test1(self):
        text = "The US must ramp up its support for Tunisia and press for a political settlement in neighboring Libya if the fledgling democracy is to succeed, employers federation president and Nobel Peace Prize winner Ouided Bouchamaoui told Al-Monitor."
        people = extract_people(text)
        print "extracted people is", people
        self.assertTrue("Ouided Bouchamaoui" in people)

    def test2(self):
        text = "Akram Hesso, a graduate of Aleppo University’s law school, holds the post of prime minister of Jazeera canton. From Amuda, he spoke to Al-Monitor about the difficulties and problems his people are facing and the sacrifices they made to preserve the safety of the Kurdish regions."
        people = extract_people(text)
        print "extracted people is", people
        self.assertTrue("Akram Hesso" in people)

    def test3(self):
        text = """4.0:$2">Royal Canadian Mounted Police Chief Superintendent John Smith said the arr"""
        person = extract_person_quickly(text)
        self.assertEqual("John Smith", person)

    def test4(self):
        text = "But Commons Leader Chris Grayling"
        person = extract_person_quickly(text)
        self.assertEqual("Chris Grayling", person)

    def test5(self):
        text = "Foreign Ministry Spokesperson Ahmed Abu Zeid"
        person = extract_person_quickly(text)
        self.assertEqual("Ahmed Abu Zeid", person)
 
if __name__ == '__main__':
    unittest.main()

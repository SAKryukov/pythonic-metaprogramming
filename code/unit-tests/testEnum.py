import unittest
from code.core.enumerations import *
import json

class TestEnumBase(unittest.TestCase):
    @classmethod
    def dummy(cls, One = 1, Two = 2, Three = 3, Four = 4):
        pass
# class TestEnumBase

class TestEnum(TestEnumBase):

    @enumeration
    class ParsingSample:
        One = 1
        Two = 2
        Three = 3
        DifficultCase = TestEnumBase.dummy(
            One = 10
        )
        MoreDifficultCase = TestEnumBase.dummy( \
        Two = 11)
        EvenMoreDifficultCase = TestEnumBase.dummy( \

        Three = 13)
        Last = Enum.Auto
    # class ParsingSample

    def testParsing(self):
        enum = self.ParsingSample
        count = len(enum)
        self.assertEqual(count, 7)
    # testParsing

    def testJson(self):
        enum = self.ParsingSample
        count = len(enum)
        dictionary = enum.dictionary()
        jsonString = json.dumps(dictionary)
        self.assertEqual(jsonString,
           '{"One": 1, "Two": 2, "Three": 3, "DifficultCase": null, "MoreDifficultCase": null, "EvenMoreDifficultCase": null, "Last": 4}')
    # testJson

    def testConversions(self):
        enum = self.ParsingSample
        length = len(enum)
        sameLength = enum.length()
        firstMember = enum[0]
        secondMember = enum("Two") # not a constructor!
        self.assertEqual(firstMember, enum.One)
        self.assertEqual(secondMember, enum.Two)
        self.assertEquals(length, 7)
        self.assertEquals(length, sameLength)
    # testConversions
    
# class TestEnum

if __name__ == '__main__':
    unittest.main()
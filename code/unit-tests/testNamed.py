import unittest
from code.core.named import NamedDictionary

class TestNamedBase(unittest.TestCase):
    namesWithBlank = ("my name", "good") 
    namesWithNoId = ("123", "good") 
    namesWithKeyword = ("class", "good")
    namesWithBuiltinFunctions  = ("type", "good")
# class TestNamedBase

class TestNamed(TestNamedBase):

    class DefinitionSetBase:
        first = "Hello!"
    # class DefinitionSetBase

    class DefinitionSet(DefinitionSetBase):
        second = NamedDictionary.FromStrings("first", "second", "third")
        third = 3
    # class DefinitionSet

    definitions = NamedDictionary.FromStrings(
        "Great", "Excellent", "Good",
        ("Satisfactory", "Poor", ["Bad", "Failing"]))
    dictionarySet = NamedDictionary.FromDictionary({"One": 1, "Two": 2, "Tree": [1, 2, 3]})

    definitions = NamedDictionary.Merge(definitions, dictionarySet, DefinitionSet)

    def testNameValidity(self):
        def tryNames(nameset):
            try:
                NamedDictionary.FromStrings(nameset)
            except Exception:
                return
            self.fail("Exception should be thrown on invalid name")
        # tryNames            
        tryNames(self.namesWithBlank)
        tryNames(self.namesWithNoId)
        tryNames(self.namesWithKeyword)
        # but!
        result = NamedDictionary.FromStrings(self.namesWithBuiltinFunctions)
        self.assertEqual(result.type, self.namesWithBuiltinFunctions[0])
    # testConversions

    def testMatch(self):
        self.assertEqual(self.definitions.first, "Hello!")
        self.assertEqual(self.definitions.Good, "Good")
        self.assertEqual(self.definitions.second.first, "first")
        self.assertEqual(self.definitions.Tree[0], 1)
    # testMatch

# class TestNamed

if __name__ == '__main__':
    unittest.main()
from code.core.enumerations import Enum
from code.core.named import NamedDictionary 
from code.commandLine.commandLineParser import CommandLineParser 

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

print (self.definitions.first)
print (self.definitions.Good)
print (self.definitions.second.first)
print (self.definitions.Tree[0])

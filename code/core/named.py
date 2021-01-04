''' 
NamedDictionary

Dynamically emitted dictionary-like objects
used to access elements by Python identifiers, not by string keys.
They are emitted out of classes with class attributes, sets of strings and dictionaries,
and can be merged together.
Invalid or duplicate identifiers throw exceptions.

Copyright (C) 2018 by Sergey A Kryukov

http://www.SAKryukov.org
https://www.codeproject.com/Members/SAKryukov

'''

import ast

class NamedDictionary:
    
    class DefinitionSet:
        messageDuplicateKeyError = "Identifier is already used"
        identifierValidator = "{} = None"
    # class DefinitionSet

    @classmethod
    def FromStrings(cls, *members):
        result = type(str(), (), {})
        def fromContainer(container):
            for member in container:
                if isinstance(member, tuple) or isinstance(member, list):
                    fromContainer(member)
                else:
                    cls.checkUpIdentifier(result, member)
                    setattr(result, member, member)
        fromContainer(members)
        return result
    # FromStrings

    @classmethod
    def FromDictionary(cls, dictionary):
        result = type(str(), (), {})
        for key, value in dictionary.items():
            cls.checkUpIdentifier(result, key)
            setattr(result, key, value)
        return result
    # FromDictionary

    # @classmethod
    # def FromClass(cls, definitionSetClass):
    #     return definitionSetClass

    @classmethod
    def Merge(cls, *namedDictionaries):
        result = type(str(), (), {})
        for dictionary in namedDictionaries:
            members = dir(dictionary)
            for index in range(len(members)):
                name = members[index]
                if name in cls.BuiltinAttributeSet:
                    continue
                if hasattr(result, name):
                    raise cls.DuplicateKeyError(cls, name)
                value = getattr(dictionary, name)
                setattr(result, name, value)    
        return result
    # Merge

    @classmethod
    def isValidVariableName(cls, name):
        try:
            ast.parse(cls.DefinitionSet.identifierValidator.format(name))
            return True
        except Exception:
            return False
    # isValidVariable

    @classmethod
    def checkUpIdentifier(cls, result, id):
        if not isinstance(id, str):
            raise cls.NonStringObject(id)
        if not cls.isValidVariableName(id):
            raise cls.InvalidIdentifier(id)
        if hasattr(result, id):
            raise cls.DuplicateKeyError(id)
    # checkUpIdentifier

    class NonStringObject(TypeError):
        def __init__(self, key):
            TypeError.__init__(self, dict(object=key, type=type(key)))

    class InvalidIdentifier(KeyError):
        def __init__(self, name):
            KeyError.__init__(self, dict(identifier=name))

    class DuplicateKeyError(KeyError):
        def __init__(self, cls, name):
            KeyError.__init__(self,
                cls.DefinitionSet.messageDuplicateKeyError,
                dict(identifier=name))

    BuiltinAttributeSet = frozenset(dir(
        type(str(), (), {})
    ))  
        
# class NamedDictionary

''' 
Enumeration classes

Enumeration classes are dynamically emitted dictionary-like classes
uses to access enumeration members by Python identifiers or by unique ordinal number.
They are different from Python 3 Enum types.
Emitted enumeration members have three attributes:
name, index in the order of creation, and value.
Value may or may not be int; these values are never required to be distinct
Optionally, for None values int values can be auto-generated,
0-based or based on declared int values.

Copyright (C) 2018 by Sergey A Kryukov

http://www.SAKryukov.org
https://www.codeproject.com/Members/SAKryukov

'''

import inspect
import re
from collections import OrderedDict

class DefinitionSet:
    enumeratorName = "all"
    dictionaryConverterName = "dictionary"
    parseLineRegex = r"\w+"
    inaccessibleNameAttributeName = '..'
    inaccessibleIndexAttributeName = '.'
    inaccessibleNamePrefix = inaccessibleIndexAttributeName
    continuationMode = "\\"
# class DefinitionSet

class Enum:
    
    # assign to class attribute to get auto-numerated EnumerationMember.value
    # (for always auto-numerated indices, use EnumerationMember.index instead)
    class Auto: 
        pass

    @classmethod
    def Definition(cls, enumDecl):
        regex = re.compile(DefinitionSet.parseLineRegex)
        def getAttrFromMetaclass(attr):
            return lambda cls: getattr(type(cls), attr)
        def makeInaccessibleAttributeName(name):
            return DefinitionSet.inaccessibleNamePrefix + name
        bases = list(enumDecl.__bases__)
        if not cls.EnumerationType in bases:
            # to prevent exception "a new-style class can't have only classic bases"
            # also, it is used by IsInstanceOfEnumerationType:
            bases.insert(0, cls.EnumerationType)
        result = type(enumDecl.__name__, tuple(bases), {})
        enumMetaclass = type(str(), (type,), {})
        result = enumMetaclass(result.__name__, result.__bases__, {})
        # local outer-scope objects for recursive metadata collection: 
        class indices: index = currentIntegerValue = 0
        members = []
        # recursive metadata collection:
        def collectDeclarations(cls, enumDecl, members, indices):
            for base in enumDecl.__bases__:
                collectDeclarations(cls, base, members, indices)
            try:
                lines = inspect.getsourcelines(enumDecl)[0]
            except TypeError: # for Python 3, prevent parsing built-in types
                return
            firstPos = None
            continuationMode = False
            for line in lines:
                if continuationMode:
                    strip = line.strip()
                    if len(strip) < 1:
                        continue 
                    if not strip.endswith(DefinitionSet.continuationMode):
                        continuationMode = False
                    continue        
                if line.strip().endswith(DefinitionSet.continuationMode):
                    continuationMode = True
                match = regex.search(line)
                if not match:
                    continue
                slice = match.regs[0]
                namepos = slice[0]
                if not firstPos == None:
                    if firstPos != namepos:
                        continue
                name = match.string[namepos:slice[1]]
                if name and hasattr(enumDecl, name):
                    value = getattr(enumDecl, name)
                    isNull = value == cls.Auto
                    isInt = isinstance(value, int)
                    if isNull:
                        value = indices.currentIntegerValue
                        indices.currentIntegerValue = indices.currentIntegerValue + 1
                    elif isInt:
                        indices.currentIntegerValue = value + 1
                    enumerationMember = cls.EnumerationMember(indices.index, name, value, result)
                    members.append(enumerationMember)
                    inaccessibleName = makeInaccessibleAttributeName(name)
                    setattr(enumMetaclass, name, property(getAttrFromMetaclass(inaccessibleName)))
                    setattr(enumMetaclass, inaccessibleName, enumerationMember)
                    indices.index = indices.index + 1
                    if firstPos == None:
                        firstPos = namepos
                # if name is the name of valid member
            # loop
        # collectDeclarations
        collectDeclarations(cls, enumDecl, members, indices)
        @classmethod
        def iterator(cls, inReverse = False):
            container = reversed(members) if inReverse else members
            for element in container:
                yield element
        setattr(result, DefinitionSet.enumeratorName, iterator)
        @classmethod
        def toOrderedDictionary(cls):
            dictionary = OrderedDict()
            for member in cls.all():
                dictionary[member.name] = member.value
            return dictionary
        setattr(result, DefinitionSet.dictionaryConverterName, toOrderedDictionary)
        @classmethod
        def length(cls):
            return len(members) 
        result.length = length
        enumMetaclass.__len__ = length
        @classmethod
        def getItem(cls, index):
            return members[index]
        enumMetaclass.__getitem__ = getItem
        @classmethod
        def conversionOperator(cls, name):
            for member in members:
                if member.name == name:
                    return member
            return None
        # assigning conversionOperator a real challenge :-)
        # call it "pseudo-constructor":
        enumMetaclass.__call__ = conversionOperator
        result.__init__ = None
        return result 
    # Definition

    class EnumerationType(object):
        pass

    @classmethod
    def IsMemberOfEnumeration(cls, enumeration, member):
        if not cls.IsInstanceOfEnumerationType(enumeration):
            return False
        if not isinstance(member, cls.EnumerationMember):
            return False
        return member.__enumeration__ == enumeration 

    @classmethod
    def IsInstanceOfEnumerationType(cls, obj):
        return issubclass(type(obj), type(cls.EnumerationType))

    class EnumerationMember(object):
        def __init__(self, index, name, value, enumerationClass = None):
            setattr(self, DefinitionSet.inaccessibleIndexAttributeName, index)
            setattr(self, DefinitionSet.inaccessibleNameAttributeName, name)
            self.value = value
            # new member used to tagging enumeration members with their classes
            # (those returned by CreateEnum)
            # used for IsMemberOfEnumeration test:
            self.__enumeration__ = enumerationClass
        def __str__(self):
            return self.name
        def __int__(self):
            return self.index
        def __index__(self):
            return self.index
        @property
        def name(self):
            return getattr(self, DefinitionSet.inaccessibleNameAttributeName)
        @property
        def index(self):
            return getattr(self, DefinitionSet.inaccessibleIndexAttributeName)
    # class EnumerationMember

# class Enum

# use as decorator:
#    @enumeration
#    someClass
enumeration = Enum.Definition
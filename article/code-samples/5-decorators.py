import sys
from library.enumerations import Enum
#import enum

@Enum.Definition
class Test:
    pass

def normalDecorator(cls):
    cls.addition = "addition"
    return cls

class Attribute:
    @classmethod
    def Decorator(cls, target):
        target.more = "more"
        return target

class Nested:

    @normalDecorator
    class Options:
        pass

    @Attribute.Decorator
    class Features:
        pass

    print ("good! " + str(sys.version))
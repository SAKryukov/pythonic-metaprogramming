def getter(self):
    return 13

metaclass = type(str(), (type,), {})
cls = metaclass(str(), (), {})
metaclass.val = property(getter)

v = cls.val

print "done"
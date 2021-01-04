class MyMetaclass(type):
    pass

MyClass = MyMetaclass(str("MyClass"), (), {})

aMetaclass = type(MyClass)
myInstance = MyClass()
MyClass.another = "another"
myInstance.instanceAttribute = "instanceAttribute"

# make instances of MyClass callable:
def callableImpl(instance):
    print(instance.instanceAttribute)
    print ("this is callable")
MyClass.__call__ = callableImpl
myInstance()

# print (MyMetaclass)
# same as
# print (aMetaclass)

def iterator(cls):
    container = [1, 2, 3, 4]
    for element in container:
        yield element

MyClass.__iter__ = iterator

for a in myInstance:
    print(a)

MyMetaclass.__call__ = None
newInstance = MyClass()
print("works!")
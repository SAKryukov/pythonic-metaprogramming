from code.core.enumerations import Enum

class MonochromeColor: # inheritance from object will be added by Enum.CreateEnum:
    Black = 100

class WarmColor(MonochromeColor):
    Red = Enum.Auto
    Orange\
    = Enum.Auto # could be challenging for parser
    Yellow = Enum.Auto

class GreenColor:
    Green = 200 # boundary between warm and cool

class CoolColor:
    Blue = Enum.Auto
    Indigo = Enum.Auto
    Violet = dict(opacity = 0.9, wavelength = 400) # any value
    
@Enum.Definition
class Color(WarmColor, GreenColor, CoolColor): # multiple inheritance
    White = Enum.Auto

for color in Color.all():
    print (color.name, color.index, color.value)
for color in Color.all(True): # in reverse
    print (color.name, color.index, color.value)

print(Color.Blue) # called str(Color.Blue)
arr = [0] * len(Color)
arr[int(Color.Yellow)] = str(Color.Yellow)
arr[Color.Blue.index] = Color.Blue.name
print("Arrays or tuples can be indexed with enumeration .index:", arr)
index = 4
print("Access enumeration member by index", int(Color[index]), Color[index].name)

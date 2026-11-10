


# for item in folder.iterdir():
#     print(item)

from collections import defaultdict
from typing import Protocol
import asyncio 


async def get_number():
    return 8

async def main():
    a = get_number()
    print(a)

    b = await get_number()
    print(b)

asyncio.run(main())



class CanSpeak(Protocol):
    def speak(self) -> str:
        return "Speaks Hello World"

class Dog:
    def speak(self) -> str:
        return "woof"

class Robot:
    def speak(self) -> str:
        return "beep"

class Rock:
    def speak(self) -> str:
        return "hello" 

def make_noise(thing: CanSpeak) -> None:
    print(thing.speak())
dog = Dog()
make_noise(Dog())
make_noise(Robot())
make_noise(Rock())

normal = {}
# normal[4].add("ada")
# print(normal)

notebook = defaultdict(set)
notebook[5].add("Ada")
notebook[5].add("tunde") 
notebook[7].add("bola") 
notebook[7].add("bola") 
print(notebook)

rooms = set()
rooms.add(2)
rooms.add(3)
rooms.add(1)
print(len(rooms))
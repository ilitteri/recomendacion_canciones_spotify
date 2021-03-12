from typing import Any

class Queue:
    '''Estructura de cola'''
    def __init__(self):
        self.__data = []
        self.__count = 0
        
    def enqueue(self, data: Any):
        self.__data.append(data)
        self.__count += 1

    def dequeue(self):
        self.__count -= 1
        data = self.__data.pop(0)
        return data

    def is_empty(self):
        return self.__count == 0
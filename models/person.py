#!/usr/bin/env python3

class Person:
    def __init__(self, name, surname):
        self.__name = name
        self.__surname = surname

    def __str__(self):
        return self.get_name()+":"+self.get_surname()

    def get_name(self): return self.__name
    def get_surname(self): return self.__surname

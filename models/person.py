#!/usr/bin/env python3

class Person:
    def __init__(self, name, surname, gender):
        self.__name = name
        self.__surname = surname
        self.__gender = gender

    def __str__(self):
        return self.get_name()+":"+self.get_surname()+":"+self.get_gender()

    def get_name(self): return self.__name
    def get_surname(self): return self.__surname
    def get_gender(self): return self.__gender

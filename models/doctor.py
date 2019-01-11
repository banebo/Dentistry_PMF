#!/usr/bin/env python3

import os
from models.person import Person

class Doctor(Person):

    def __init__(self, id, name, surname, gender):
        super().__init__(name, surname, gender)
        self.__id = id

    def __str__(self):
        return self.get_id()+":"+super().__str__()+":doctor"

    def get_id(self): return self.__id

def dr_menu(info):
    while True:
        os.system("clear")
        printDrMenu(info)
        choice = input("\n>> ")
        while choice.lower() not in ('1','2','3','4','5','6','7','x'):
            print("\n[-] Bad option "+choice)
            printDrMenu(info)
            choice = input("\n>> ")

        if choice == '1':
            print("Search appointment")
        elif choice == 'x':
            exit(0)

        else: print("fuck you")
        

def printDrMenu(info):
    print("\nLoged-in as dr. %s %s (%s)" % \
        (info['name'],info['surname'],info['id']))

    print("\n\t[1] Search appointments")
    print("\t[2] Modify appointment details")
    print("\t[3] View all appointments")
    print("\t[4] Search patient")
    print("\t[5] View salary")
    print("\t[6] Change password")
    print("\t[x] Logout and exit")

       

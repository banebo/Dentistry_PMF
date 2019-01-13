#!/usr/bin/env python3

import os
import hashlib
from models.person import Person

class Doctor(Person):

    def __init__(self, id, name, surname):
        super().__init__(name, surname)
        self.__id = id

    def __str__(self):
        return self.get_id()+":"+super().__str__()+":doctor"

    def get_id(self): return self.__id

    def __equals__(self, other):
        return (self.__class__ == other.__class__) and \
                (self.get_id() == other.get_id()) and \
                (self.get_name() == other.get_name()) and \
                (self.get_surname() == other.get_surname())

    def hashCode(self):
        info = self.get_id() + self.get_name() + self.get_surname()
        return hashlib.md5(info.encode("utf-8")).hexdigest()

def dr_menu(info):
    while True:
        os.system("clear")
        printDrMenu(info)
        choice = input("\n>> ")
        while choice.lower() not in ('1','2','3','4','5','6','7','x'):
            print("\n[-] Bad option "+ choice if(choice) else " ")
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

def get_doctor(hash):
    doctors = get_doctors()
    for dr in doctors:
        if hash == dr.hashCode():
            return dr
    return None

def get_doctors():
    if not os.path.isfile("database/empList.txt"): 
        return None

    doctors = []
    file = open("database/empList.txt", "r")
    for line in file:
        line.strip("\n")
        info = line.split(':')
        if info[-1].strip() == "doctor": 
            doctors.append(Doctor(info[0].strip(), \
                info[1].strip(), info[2].strip()))

    file.close()
    return doctors

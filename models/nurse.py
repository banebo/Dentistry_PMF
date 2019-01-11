#!/usr/bin/env python3

import os
import models.patient as patient
from models.person import Person


class Nurse(Person):
    def __init__(self, id, name, surname, gender, speciality=""):
        super().__init__(name, surname, gender)
        self.__type = empType.NURSE
        self.__id = id

    def __str__(self):
        return \
        self.get_id()+":"+super().__str__()+":nurse"

    def get_id(self): return self.__id
    def get_type(self): return self.__type


def nurse_menu(info):
    while True:
        os.system("clear")
        printNurseMenu(info)
        choice = input("\n>> ")
        while choice.lower() not in ('1','2','3','4','5','6','x'):
            print("\n[-] Bad option "+choice)
            printDrMenu(info)
            choice = input("\n>> ")

        if choice == '1':
            pass
        elif choice == '2':
            patient.new_patient()

        elif choice == '3':
            pass
        elif choice == '3': pass

        elif choice == '4': 
            patient.search_patient()

        elif choice == '5': pass
        elif choice == '6': pass
        elif choice == 'x':
            exit(0)
  

def printNurseMenu(info):
    print("\nLoged-in as dr. %s %s (%s)" % \
        (info['name'],info['surname'],info['id']))

    print("\n\t[1] Make appointment")
    print("\t[2] New patient")
    print("\t[3] Search appointment")
    print("\t[4] Search patient")
    print("\t[5] View salary")
    print("\t[6] Change password")
    print("\t[x] Logout and exit")


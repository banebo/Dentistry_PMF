#!/usr/bin/env python3

import os
from models import patient
from models.person import Person
from models import appointment
from models import admin

class Nurse(Person):
    def __init__(self, id, name, surname):
        super().__init__(name, surname,)
        self.__id = id

    def __str__(self):
        return \
        self.get_id()+":"+super().__str__()+":nurse"

    def get_id(self): return self.__id

def nurse_menu(info):
    while True:
        #os.system("clear")
        printNurseMenu(info)
        choice = input("\n>> ")
        while choice.lower() not in ('1','2','3','4','5','6','x'):
            print("\n[-] Bad option "+choice)
            printNurseMenu(info)
            choice = input("\n>> ")

        if choice == '1':   appointment.make_appointment()
        elif choice == '2': patient.new_patient()
        elif choice == '3': appointment.search_appointment()
        elif choice == '4': patient.search_patient()
        elif choice == '5' : appointment.print_all_appointments()
        elif choice == '6': admin.change_password()
        elif choice == 'x': exit(0)

def printNurseMenu(info):
    print("\nLoged-in as %s %s (%s)" % \
        (info['name'],info['surname'],info['id']))

    print("\n\t[1] Make appointment")
    print("\t[2] New patient")
    print("\t[3] Search appointment")
    print("\t[4] Search patient")
    print("\t[5] View schedule")
    print("\t[6] Change password")
    print("\t[x] Logout and exit")

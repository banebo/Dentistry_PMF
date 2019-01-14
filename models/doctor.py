#!/usr/bin/env python3

import os
import hashlib
import datetime
from models.person import Person
from models import patient
from models import appointment
from models import admin

class Doctor(Person):

    def __init__(self, id, name, surname):
        super().__init__(name, surname)
        self.__id = id

    def __str__(self):
        return self.get_id()+":"+super().__str__()+":doctor"

    def get_id(self): return self.__id

    def __equals__(self, other):
        if not other:
            return False

        return (self.__class__ == other.__class__) and \
                (self.get_id() == other.get_id()) and \
                (self.get_name() == other.get_name()) and \
                (self.get_surname() == other.get_surname())

    def __hash__(self):
        info = self.get_id() + self.get_name() + self.get_surname()
        return hashlib.md5(info.encode("utf-8")).hexdigest()

def dr_menu(info):
    while True:
        os.system("clear")
        printDrMenu(info)
        choice = input("\n>> ")
        while choice.lower() not in ('1','2','3','4','5','6','x'):
            print("\n[-] Bad option "+ choice if(choice) else " ")
            printDrMenu(info)
            choice = input("\n>> ")

        if choice == '1': appointment.search_appointment()
        elif choice == '2': appointment.modify_appointment_details()
        elif choice == '3': appointment.print_all_appointments()
        elif choice == '4': patient.search_patient()
        elif choice == '5': print_salary(info)
        elif choice == '6': admin.change_password(info)
        elif choice == 'x': exit(0)

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
        if hash == dr.__hash__():
            return dr
    return None

def get_doctors():
    if not os.path.isfile("database/empList.txt"): 
        return None

    doctors = []
    file = open("database/empList.txt", "r")
    for line in file:
        info = line.strip(" \n").split(':')
        if info[-1].strip() == "doctor": 
            doctors.append(Doctor(info[0].strip(), \
                info[1].strip(), info[2].strip()))

    file.close()
    return doctors

def search_doctors(name, surname, id=None):
    doctors = get_doctors()

    if len(doctors) == 0:
        print("\n[-] No doctors in database")
        return None

    doctor_list = []
    name = name.strip().lower()
    surname = surname.strip().lower()

    for dr in doctors:
        drname = dr.get_name().lower()
        drsurname = dr.get_surname().lower()
        if not surname:
            if name == drname:
                doctor_list.append(dr)
        elif not name:
            if surname == drsurname:
                doctor_list.append(dr)
        else:
            if (surname==drsurname) and (name==drname):
                doctor_list.append(dr)

    return doctor_list

def get_salary(info):
    doctor_obj = search_doctors(info['name'], info['surname'], id=info['id'])[0]
    appointments = appointment.get_appointments_dr_patient(doctor_obj, None, either=True)
    if not appointments:
        return 0

    now = datetime.datetime.now()
    salary = 0
    for appoint in appointments:
        if (appoint.get_time().month == now.month) and \
        (now > appoint.get_time()):
            salary += appoint.get_price() * 0.4 # nesto mora i ordinaciji da ostane

    return salary
    
def print_salary(info):
    salary = get_salary(info)
    if salary == 0:
        print("[-] You have done no work this month")
    else:
        print("\n[+] This months salary is: %.2d" % salary)
    input("\n\nPress Enter to continue...")
    return

def find_doctor():
    drName = input("[?] Enter doctor's name: ")
    drSurname = input("[?] Enter doctor's surname: ")
    dr_search = search_doctors(drName, drSurname)

    while len(dr_search) == 0:
        print("\n[-] Doctor not found")
        drName = input("[?] Enter doctor's name: ")
        drSurname = input("[?] Enter doctor's surname: ")
        dr_search = search_doctors(drName, drSurname)
        
    if len(dr_search) > 1:
        doctor = appointment.choose(type='doctors', list=dr_search)
    else:
        doctor = dr_search[0]

    return doctor

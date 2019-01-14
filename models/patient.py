#!/usr/bin/env python3

import os
import hashlib
from models.person import Person

class Patient(Person):
    def __init__(self, name, surname, contactInfo, alergies, illness):
        super().__init__(name, surname)
        self.__alergies = alergies
        self.__illness = illness
        self.__contactInfo = contactInfo

    def __str__(self):
        return super().__str__()+":"+self.get_alergies()+":"+self.get_illness()

    def get_alergies(self): return self.__alergies
    def get_illness(self): return self.__illness
    def get_contactInfo(self): return self.__contactInfo

    def __equals__(self, other):
        return (self.__class__ == other.__class__) and \
                (self.get_name() == other.get_name()) and \
                (self.get_surname() == other.get_surname()) and \
                (self.get_contactInfo() == other.get_contactInfo()) and \
                (self.get_alergies() == other.get_alergies()) and \
                (self.get_illness() == other.get_illness())

    def hashCode(self):
        info = self.get_name()+self.get_surname()+self.get_contactInfo()
        return hashlib.md5(info.encode('utf-8')).hexdigest()

def search_patient():
    os.system("clear")
    print("\n\tSEARCH PATIENT\n")

    name = input("[?] Enter name: ").strip().lower()
    surname = input("[?] Enter surname: ").strip().lower()

    if not(name or surname):
        return

    patients = get_patients()
    foundPatients = []

    for p in patients:
        pname = p.get_name().lower().strip()
        psurname = p.get_surname().lower().strip()
        if not name:
            if surname == psurname:
                foundPatients.append(p)
        elif not surname:
            if name == pname:
                foundPatients.append(p)
        else:
            if (name == pname) and (surname == psurname):
                foundPatients.append(p)

    if len(foundPatients) == 0:
        print("[-] Patient {:s} {:s} not found".format(name.title(),surname.title()))
        input("\n\nPress Enter to continue...")
        return

    print("\n[*] Found {:d} patients mathing {:s} {:s}".format( \
        len(foundPatients), name.title(), surname.title()))

    for patient in foundPatients:
        print("\n\t{:12}  {:>s}".format("Name:", patient.get_name()))
        print("\t{:12}  {:>s}".format("Surname:", patient.get_surname()))
        print("\t{:12}  {:>s}".format("Contact:", patient.get_contactInfo()))
        print("\t{:12}  {:>s}".format("Alergies:", patient.get_alergies()))
        print("\t{:12}  {:>s}".format("Illnesses:", patient.get_illness()))

    input("\n\nPress Enter to continue...")
    print()
    return

def new_patient():
    os.system("clear")
    print("\n\tNEW PATIENT\n")

    name = input("[?] Patient name: ").strip().title()
    while not name:
        name = input("[?] Enter a valid patient name: ").strip().title()
        
    surname = input("[?] Patient surname: ").strip().title()
    while not surname:
        surname = input("[?] Enter a valid patient surname: ").strip().title()

    contactInfo = input("[?] Patient contact [email or phone]: ").strip()
    while not contactInfo.strip():
        contactInfo = input("[?] Please enter contact info [email or phone]: ").strip()

    alergies = input("[?] Patient alergies: ").strip()
    if not alergies:
        alergies = "None"

    illness = input("[?] Patient illnesses: ").strip()
    if not illenss:
        illness = "None"

    info = name+":"+surname+":"+contactInfo+":"+alergies+":"+illness
    file = open("database/patients.txt", "a")
    file.write(info+"\n")
    file.close()

    print("\t[+] Done")
    input("\nPress Enter to continue...")
    return

def get_patient(hash):
    patients = get_patients()

    for p in patients:
        if p.hashCode() == hash:
            return p

    return None

def search_patients(name, surname):
    patients = get_patients()

    if len(patients) == 0:
        print("[-] No patients in database")
        return None

    patient_list = []
    name = name.strip().lower()
    surname = surname.strip().lower()

    for p in patients:
        pname = p.get_name().lower()
        psurname = p.get_surname().lower()
        if not surname:
            if name == pname:
                patient_list.append(p)
        elif not name:
            if surname == psurname:
                patient_list.append(p)
        else:
            if (surname==psurname) and (name==pname):
                patient_list.append(p)

    return patient_list
                
def get_patients():
    if not os.path.isfile("database/patients.txt"):
        return None

    patients = []
    file = open("database/patients.txt", "r")
    for line in file:
        info = line.strip(" \n").split(':')
        patients.append(Patient(info[0], info[1], info[2], info[3], info[4]))

    file.close()
    return patients

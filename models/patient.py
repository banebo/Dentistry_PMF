#!/usr/bin/env python3

import os
from models.person import Person

class Patient(Person):
    def __init__(self, name, surname, gender, contactInfo, \
        alergies, illness):
        super().__init__(name, surname, gender)
        self.__alergies = alergies
        self.__illness = illness
        self.__contactInfo = contactInfo

    def __str__(self):
        return super().__str__()+ \
            ":"+self.get_alergies()+":"+self.get_illness()

    def get_alergies(self): return self.__alergies
    def get_illness(self): return self.__illness
    def get_contactInfo(self): return self.__contactInfo


def search_patient():
    os.system("clear")
    print("\n\tSEARCH PATIENT\n")

    name = input("[?] Enter name: ")
    surname = input("[?] Enter surname: ")

    if not(name and surname):
        choice = input("[-] Please enter valid info. Retry [y/n]: ").strip()
        if choice == "y":
            search_patient()

    if not os.path.isfile("database/patients.txt"):
        print("[-] Patients file missing. Aborting...\n")
        return

    foundPatients = []
    file = open("database/patients.txt", "r")
    for line in file:
        info = line.split(":")
        if len(info) != 6:
            continue

        if (info[0] == name) and (info[1] == surname):
            foundPatients.append(Patient(info[0], info[1], info[2], info[3],\
            info[4], info[5].strip("\n")))

    file.close()

    if len(foundPatients) == 0:
        print("[-] Patient %s %s not found." % (name, surname))
        return

    print("\n[*] Found %d patients matching %s %s" %(len(foundPatients), \
    name, surname))

    for patient in foundPatients:
        print("\n\tName: " + patient.get_name())
        print("\tSurname: " + patient.get_surname())
        print("\tContact: " + patient.get_contactInfo())
        print("\tGender: " + patient.get_gender())
        print("\tAlergies: " + patient.get_alergies())
        print("\tIllnesses: " + patient.get_illness())

    input("\n\nPress Enter to continue...")
    print()
    return

def new_patient():
    os.system("clear")
    print("\n\tNEW PATIENT\n")

    name = input("[?] Patient name: ").strip()
    surname = input("[?] Patient surname: ").strip()
    gender = input("[?] Patient gender: ").strip()
    contactInfo = input("[?] Patient contact [email or phone]: ").strip()
    while not contactInfo.strip():
        contactInfo = input("[?] Please enter contact info [email or phone]: ").strip()
    alergies = input("[?] Patient alergies: ").strip()
    illness = input("[?] Patient illnesses: ").strip()

    if not(name and surname and gender and contactInfo):
        choice = input("[-] Failed to create patient, information missing. Retry[y/n]: ")
        if choice.lower() == "y":
            new_patient()
        return

    info = name+":"+surname+":"+gender+":"+contactInfo+":"+alergies+":"+illness
    file = open("database/patients.txt", "a")
    file.write(info+"\n")
    file.close()

    print("\t[+] Done")
    input("\nPress Enter to continue...")
    return



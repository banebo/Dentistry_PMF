#!/usr/bin/env python3

import os
import datetime
import models
import models.doctor as doctor
from models import patient

class Appointment:
    def __init__(self, time, patient_id, doctor_id, intervention, description):
        self.__patient = patient_id
        if not self.__patient:
            print("[-] Patient is missing")
            return

        self.__doctor = doctor_id
        if not self.__doctor:
            print("[-] Doctor is missing")
            return
            
        self.__time = datetime.datetime.strptime(str(time), "%Y-%m-%d %H-%M")
        self.__description = description
        self.__intervention = intervention

    def __str__(self):
        date = self.get_time()
        date = "{:%Y-%m-%d %H-%M}".format(date)

        return date+":"+str(self.get_patientID()) + ":" + \
            str(self.get_doctorID())+":"+self.get_intervention()+ \
            ":"+self.get_description()

    def get_price(self):
        if not os.path.isfile("database/interventions.txt"):
            return 0

        file = open("database/interventions.txt", "r")
        for line in file:
            info = line.split(':')
            if info[0] == self.get_intervention():
                return int(info[1].strip())

        file.close()
        return 0

    def get_intervention(self): return self.__intervention
    def get_time(self): return self.__time
    def get_doctorID(self): return self.__doctor
    def get_patientID(self): return self.__patient

    def get_patient(self): 
        for p in models.patient.get_patients():
            if p.hashCode() == int(self.get_patientID()):
                return p
        return None
 
    def get_doctor(self): 
        for dr in doctor.get_doctors():
            if dr.hashCode() == int(self.get_doctorID()):
                return dr
        return None

    def get_description(self): return self.__description
    def get_intervention(self): return self.__intervention

def make_appointment():
    os.system("clear")
    print("\n\tNEW APPOINTMENT")

    intervention = choose_intervention()
    intervention = intervention.split(":")[0]

    doctor = choose(type="doctors")
    if not doctor:
        print("\n[-] Can't make an appointment, no doctors")
        input("\n\nPress Enter to continue...")
        return

    print()
    date = choose_date(doctor)
    date = "{:%Y-%m-%d %H-%M}".format(date)

    patient = find_patient()
    
    desc = input("\n[?] Enter appointment description: ")

    appointment = Appointment(date, patient.hashCode(), doctor.hashCode(),\
        intervention, desc)

    file = open("database/appointments.txt", "a")
    file.write(appointment.__str__())
    file.write("\n")
    file.close()

    print("\t[+] Done")
    input("\n\nPress Enter to continue...")
    return

def choose_intervention():
    interventions = getInterventions()
    printInterventions(interventions)
    choice = input("\t>> ")

    if not canStr2Int(choice):
        choice = -1
    else:
        choice = int(choice)

    while choice < 0 or choice > len(interventions):
        print("\n[-] Please enter a valid number")
        printInterventions(interventions)
        choice = input("\t>> ")

        if not canStr2Int(choice):
            choice = -1
        else:
            choice = int(choice)

    return interventions[choice-1]
    
def getInterventions():
    if not os.path.isfile("database/interventions.txt"):
        return

    information = []
    file = open("database/interventions.txt","r")
    for line in file:
        if len(line.split(":")) == 2:
            information.append(line.strip("\n"))

    file.close()

    return information

def printInterventions(list):
    print("\n[?] Choose an intervention: ")

    if not list:
        print("\t[-] No interventions!")
        return

    for i in range(len(list)):
        inter = list[i].split(":")
        if not len(inter) == 2:
            continue
        print("\t[{:d}] {:.<30} {:5}".format(i+1,inter[0], inter[1]))

    print()
    return
        
def choose_date(doctor):
    ok = True
    date = input("[?] Enter appointment date [DD.MM.YYYY]: ").strip(" .")
    time = input("[?] Enter appointment time [00/24 . 00/60]: ").strip()
    date += " " + time

    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H.%M")
    except ValueError as e:
        ok = False
    if isinstance(date, datetime.datetime):
        if date < datetime.datetime.now():
            ok = False
    if ok: 
        if bad_time(doctor, date):
            ok = False

    while not ok:
        ok = True
        print("\n[-] Invalid date or time!")
        date = input("[?] Enter appointment date [DD.MM.YYYY]: ").strip(" .")
        time = input("[?] Enter appointment time [00/24 . 00/60]: ").strip()
        date+=" "+time

        try: 
            date = datetime.datetime.strptime(date, "%d.%m.%Y %H.%M")
        except ValueError as e:
            ok = False
        if isinstance(date, datetime.datetime):
            if date < datetime.datetime.now():
                ok = False
        if ok: 
            if bad_time(doctor, date):
                ok = False
        
    return date

def bad_time(doctor, time):
    if not os.path.isfile("database/appointments.txt"):
        return False

    if (time.hour < 7) or (time.hour >= 20):
        return True

    file = open("database/appointments.txt", "r")
    for line in file:
        info = line.split(":")
        appoint_date = datetime.datetime.strptime(info[0], "%Y-%m-%d %H-%M")

        if (models.doctor.get_doctor(info[2]).__equals__(doctor)) and \
        (appoint_date == time):
            return True

    file.close()
    return False

def print_choices(list):
    if len(list) == 0:
        print("[-] Nothing to show")
     
    print("\n[?] Choose: ")
    for i in range(len(list)):
        if isinstance(list[i], doctor.Doctor):
            print("\t[%d] dr. %s %s" % (i+1, list[i].get_name(), list[i].get_surname()))
        else:
            print("\t[%d] %s %s" % (i+1, list[i].get_name(), list[i].get_surname()))

def choose(type=None, list=None):
    if type == "doctors":
        list = doctor.get_doctors()

    if len(list) == 0:
        return None

    print_choices(list)
    choice = input("\n\t>> ")

    if not canStr2Int(choice):
        choice = -1
    else:
        choice = int(choice)

    while choice < 0 or choice > len(list):
        print("\n[-] Please enter a valid number")
        print_choices(list)
        choice = input("\n\t>> ")

        if not canStr2Int(choice):
            choice = -1
        else:
            choice = int(choice)

    return list[choice-1]

def find_patient():
    patientName = input("[?] Enter patient name: ").strip()
    patientSurname = input("[?] Enter patient surname: ").strip()
    patient_search = models.patient.search_patients(patientName, patientSurname)

    while len(patient_search) == 0:
        print("\n[-] Patient not found")
        patientName = input("[?] Enter patient name: ")
        patientSurname = input("[?] Enter patient surname: ")
        patient_search = models.patient.search_patients(patientName, patientSurname)
        
    if len(patient_search) > 1:
        patient = choose(list=patient_search)
    else:
        patient = patient_search[0]
        print("\t[*] One patient found: "+patient.get_name()+" "+ \
            patient.get_surname())

    return patient

def canStr2Int(c):
    try:
        c = int(c)

    except ValueError as e:
        return False

    return True

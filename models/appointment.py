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
            return None

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

    def __equals__(self, obj):
        if not obj: 
            return False

        return (self.__class__ == obj.__class__) and \
                (self.get_time() == obj.get_time()) and \
                (self.get_patientID() == obj.get_patientID()) and \
                (self.get_doctorID() == obj.get_doctorID()) and \
                (self.get_intervention() == obj.get_intervention()) and \
                (self.get_description() == obj.get_description())


    def tableRepr(self):
        date = self.get_time()
        date = "{:d}.{:d}.{:d} at {:d}:{:d}".format( \
            date.day, date.month, date.year, date.hour, date.minute)
        if self.get_doctor():
            doctor = "dr."+self.get_doctor().get_surname()+" "+ \
                self.get_doctor().get_name()
        else:
            doctor = "DoctorNotFound"

        if self.get_patient():
            patient = self.get_patient().get_name()+" "+ \
                self.get_patient().get_surname()
        else:
            patient = "PatientNotFound"

        return "{:^19}|{:^30}|{:^27}|{:^25}|\t{:70}|".format( \
            date, doctor, patient, self.get_intervention(),
            self.get_description()) 

                
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
            if p.hashCode() == self.get_patientID():
                return p
        return None
 
    def get_doctor(self): 
        for dr in doctor.get_doctors():
            if dr.hashCode() == self.get_doctorID():
                return dr
        return None

    def get_description(self): return self.__description
    def get_intervention(self): return self.__intervention

    def set_description(self, newDesc): self.__description = newDesc


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
        return
     
    print("\n[?] Choose: ")
    for i in range(len(list)):
        if isinstance(list[i], doctor.Doctor):
            print("\t[%d] dr. %s %s" % (i+1, list[i].get_name(), list[i].get_surname()))
        else:
            print("\t[%d] %s %s" % (i+1, list[i].get_name(), list[i].get_surname()))

    return

def print_appoint_choices(list):
    if len(list)==0:
        print("[-] Nothing to show")
        return

    print("{:^3} ||".format("No.") +  get_appointmentHeader())
    for i in range(len(list)):
        row = "{:^3} ||".format(i+1) + list[i].tableRepr()
        print(row)

    return

def get_appointmentHeader():
    header = "{:^19}|{:^30}|{:^27}|{:^25}|\t{:^70}|\n".format( \
        "Date and time", "Doctor","Patient","Intervention","Description")

    n = len(header)
    for i in range(n):
        header += "-"

    return header

def choose(type=None, list=None):
    if (type == "doctors") and (not list):
        list = doctor.get_doctors()

    if len(list) == 0:
        return None

    if type == "appointments": print_appoint_choices(list)
    else: print_choices(list)

    choice = input("\n\t>> ")

    if not canStr2Int(choice):
        choice = -1
    else:
        choice = int(choice)

    while choice < 0 or choice > len(list):
        print("\n[-] Please enter a valid number")

        if type == "appointments": print_appoint_choices(list)
        else: print_choices(list)

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

def find_doctor():
    drName = input("[?] Enter doctor's name: ")
    drSurname = input("[?] Enter doctor's surname: ")
    dr_search = models.doctor.search_doctors(drName, drSurname)

    while len(dr_search) == 0:
        print("\n[-] Doctor not found")
        drName = input("[?] Enter doctor's name: ")
        drSurname = input("[?] Enter doctor's surname: ")
        dr_search = models.doctor.search_doctors(drName, drSurname)
        
    if len(dr_search) > 1:
        doctor = choose(type='doctors', list=dr_search)
    else:
        doctor = dr_search[0]

    return doctor

def get_appointments():
    if not os.path.isfile("database/appointments.txt"):
        print("\n\n[-] Database file is missing!\n")
        exit(1)

    appoints = []
    file = open("database/appointments.txt")
    for line in file:
        info = line.strip(" \n").split(':')
        if len(info) != 5: continue

        appoints.append(Appointment(info[0].strip(), info[1].strip(), \
            info[2].strip(), info[3].strip(), info[4].strip()))

    file.close()
    return appoints

def get_appointments_dr_patient(doctor_obj, patient_obj, either=False):
    appointments = get_appointments()
    if not appointments:
        return None

    appoint_list = []

    for appointment in appointments:
        if either:
            if (not doctor_obj) and patient_obj:
                if appointment.get_patient().__equals__(patient_obj):
                    appoint_list.append(appointment)

            if (not patient_obj) and doctor_obj:
                if appointment.get_doctor().__equals__(doctor_obj):
                    appoint_list.append(appointment)

        if (appointment.get_doctor().__equals__(doctor_obj)) and \
        (appointment.get_patient().__equals__(patient_obj)):
            appoint_list.append(appointment)

    return appoint_list

def search_appointment():
    os.system("clear")
    print("\n\tSEARCH APPOINTMENT\n")

    patient_obj = find_patient()
    doctor_obj = find_doctor()
    appointments = get_appointments_dr_patient(doctor_obj, patient_obj)
    if not appointments:
        print("\n[-] No appointments found")
        input("\n\nPress Enter to continue...")
        return
    if len(appointments) > 1:
        print("\n")
        appointment = choose(type="appointments",list=appointments)
    else:
        appointment = appointments[0]

    print("\n\n")
    print("[*] Appointment details:\n")
    print(get_appointmentHeader())
    print(appointment.tableRepr())

    input("\n\nPress Enter to continue...")

    return

def canStr2Int(c):
    try:
        c = int(c)

    except ValueError as e:
        return False

    return True

def print_all_appointments():
    if not os.path.isfile("database/appointments.txt"):
        print("[-] No appointments.txt file")
        return

    appointments = get_appointments()
    if len(appointments) == 0:
        print("[-] No appointments")
        return

    appointments.sort(key=lambda x: x.get_time())
            
    print("\n"+get_appointmentHeader())
    now = datetime.datetime.now()
    for a in appointments:
        if not a: continue
        if a.get_time() > now:
            print(a.tableRepr())


    input("\n\nPress Enter to continue...")
    return

def get_indexOf(obj, list):
    for i in range(len(list)):
        if obj.__equals__(list[i]):
            return i
    return None

def modify_appointment_details():
    os.system("clear")
    print("\n\tMODIFY APPOINTMENT DETAILS\n")

    doctor_obj = find_doctor()
    patient_obj = find_patient()
    appointments = get_appointments_dr_patient(doctor_obj, patient_obj, either=True)
    if not appointments:
        print("[-] No appointments found!")
        input("\n\nPress Enter to continue...")
        return

    if len(appointments) > 1:
        print("\n")
        appointment_obj = choose(type="appointments",list=appointments)
    else:
        appointment_obj = appointments[0]

    index = get_indexOf(appointment_obj, appointments)

    newDets = input("[?] Enter new details: ")
    appointment_obj.set_description(newDets)
    appointments[index] = appointment_obj

    file = open("database/appointments.txt", "w")
    for appoint in appointments:
        file.write(str(appoint) + "\n")

    file.close()
    print("\n\t[+] Done.")
    input("\n\nPress Enter to continue...")
    return

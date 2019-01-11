#!/usr/bin/env python3

import getpass
import os
import crypt
import models.patient as patient
import models.nurse as nurse
import models.doctor as doctor
import models.functions as func
import models.admin as admin

def loginPage():
    os.system("clear")
    print("\n\tLOGIN")
    while True:
            username = str(input("\n[?] Enter username: "))
            password = getpass.getpass("[?] Enter password: ")

            if not login(username, password):
                print("[-] Login failed!\n")
                return None
            else:
                return getInfo(username)

    
def login(username, password):

    if not username.strip() or not password.strip():
        return False

    if not os.path.isfile("database/login.txt"):
        print("[-] Login file is missing, can't login.")
        exit(1)

    file = open("database/login.txt", "r")
    c = 0
    for line in file:
        c += 1
        info = line.strip("\n").split(":")
        if len(info) != 2:
            continue

        if info[0] == username:
            if crypt.crypt(password, info[1]) == info[1]:
                return True

    file.close()
    return False

def getInfo(username):
    if not username.strip():
        return None

    if not os.path.isfile("database/empList.txt"):
        print("[-] Cant fetch data, file missing!")
        return

    if username == "admin":
        return {'id':'admin'}

    file = open("database/empList.txt", "r")
    for line in file:
        if line.split(":")[0] == username:
            info = line.split(":")
            if len(info) == 5:
                return {'id': info[0], 'name':info[1], 'surname':info[2], \
                'gender':info[3], 'empType':info[4].strip("\n")}

    file.close()
    return None


def main():
    os.system("clear")

    print("\t WELCOME TO DENTISTRY\n\n")

    while True:
        info = loginPage()
        if info == None: continue

        if info['id'] == "admin":
            admin.admin_menu(info)
        if info['empType'] == "doctor":
            doctor.dr_menu(info)
        elif info['empType'] == "nurse":
            nurse.nurse_menu(info)
        else:
            print("[-] Something went wrong")
            exit(1)

    exit(0)

if __name__ == "__main__":
    while True:
        try:
            main()

        except KeyboardInterrupt as e:
            choice = input("\n[!] Are you sure you want to exit [y/n]? ")
            if choice.lower() == "y":
                print("\n\n[*] Exiting...")
                exit(0)

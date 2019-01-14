#!/usr/bin/env python3

import os
import getpass
import crypt
from models.person import Person

class Admin(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return super().__str__() + ":admin"

def admin_menu(info):
    while True:                                                                 
        os.system("clear")                                                      
        printAdminMenu(info)                                                       
        choice = input("\n>> ")                                                 
        while choice.lower() not in ('1','x'):          
            print("\n[-] Bad option "+choice)                                   
            printAdminMenu(info)                                                   
            choice = input("\n>> ")                                             
                                                                                 
        if choice == '1': registerPage()
        elif choice == 'x': exit(0)                                                             

def printAdminMenu(info):
    print("\nLogged in as " + info['id'])

    print("\n\t[1] Register employee")
    print("\t[x] Exit")

def registerPage():
    #os.system("clear")
    print("\nREGISTER\n")

    name = str(input("[?] Name: ")).strip().title()
    while not name:
        name = str(input("[?] Enter a valid name: ")).strip().title()
        
    surname = str(input("[?] Surname: ")).strip().title()
    while not surname:
        surname = str(input("[?] Enter a valid surname: ")).strip().title()

    username = str(input("[?] Username: ")).strip()
    while (not username) or username_exists(username):
        username = str(input("[?] Invalid username, enter another one: ")).strip()

    pass1 = getpass.getpass("[?] Enter password: ")
    pass2 = getpass.getpass("[?] Re-enter password: ")

    while (not pass1.strip()) or pass1 != pass2:
        pass1 = getpass.getpass("[?] Invalid password, enter password: ")
        pass2 = getpass.getpass("[?] Re-enter password: ")

    empType = str(input("[?] Enter employee type [doctor/nurse]: ")).strip()
    while empType.lower() not in ('doctor', 'nurse'):
        empType = input("[?] Enter employee type [doctor/nurse]: ").strip()

    info = username+":"+name+":"+surname+":"+empType+"\n"
    file = open("database/empList.txt", "a")
    file.write(info)
    file.close()

    file = open("database/login.txt", "a")
    info=username+":"+crypt.crypt(pass1,crypt.mksalt(crypt.METHOD_SHA512))+"\n"
    file.write(info)
    file.close()

    print("\n[+] Done")
    input("\n\nPress Enter to continue...")

    return

def username_exists(username):
    if not os.path.isfile("database/empList.txt"):
        return False

    file = open("database/empList.txt", "r")
    for line in file:
        if line.split(":")[0].strip() == username:
            file.close()
            return True

    return False

def change_password(info):
    #os.system("clear")
    print("\n\tPASSWORD CHANGE\n")
    file = open("database/login.txt")
    list = []
    for line in file:
        loginfo = line.strip(" \n").split(':')
        list.append({'username':loginfo[0], 'password':loginfo[1]})
    file.close()
    
    current_password = ""
    for usr in list:
        if usr['username'] == info['id']:
            current_password = usr['password']
            break

    password = getpass.getpass("[?] Enter current password: ")
    while current_password != crypt.crypt(password, current_password):
        print("\n[-] Invalid password!")
        password = getpass.getpass("[?] Enter current password: ")
        
    password1 = getpass.getpass("[?] Enter new password: ")
    password2 = getpass.getpass("[?] Re-enter new password: ")

    while password1 != password2:
        password1 = getpass.getpass("[?] Enter new password: ")
        password2 = getpass.getpass("[?] Re-enter new password: ")

    for usr in list:
        if usr['username'] == info['id']:
            usr['password']=crypt.crypt(password1, crypt.mksalt(crypt.METHOD_SHA512))

    file = open("database/login.txt", "w")
    for usr in list:
        file.write(usr['username']+":"+usr['password']+"\n")
    file.close()

    print("\n[+] Done")
    input("\n\nPress Enter to continue...")

    return

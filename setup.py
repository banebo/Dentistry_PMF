#!/usr/bin/env python3

import crypt
import getpass
import os

def main():
    username = input("[?] Enter admin username: ")
    while checkUsername(username):
        username = input("[?] Username taken, enter admin username: ")
        
    pass1 = getpass.getpass("[?] Enter password: ")
    while not pass1:
        pass1 = getpass.getpass("[?] Enter password: ")

    pass2 = getpass.getpass("[?] Re-enter password: ")
    if pass1 != pass2:
        print("[-] Passwords do not match, aborting...")

    hashed = crypt.crypt(pass1, crypt.mksalt(crypt.METHOD_SHA512))
    file = open("database/login.txt", "a")
    file.write(username+":"+hashed+"\n")
    file.close()

    print("[+] Done")


def checkUsername(username):
    if not os.path.isfile("database/login.txt"):
        return False

    file = open("database/login.txt", "r")
    for line in file:
        if line.split(':')[0] == username:
            return True

    file.close()
    return False


if __name__=="__main__":
    main()

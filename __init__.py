from _ast import keyword

__author__ = 'admin'
__name__ = '__main__'

import Encrypt as en
import Decrypt as de


def main():
    choice = input("Pleae select one of the following options:\n1) Encrypt\n2)Decrypt")
    if str(choice) == '1':
        inputFile = input("Type in the full path of the file you wish to encrypt:\n")
        key = input("Please type in key. Must be a minimum of 16 characters.")[:16]
        encrypt = en.Encrypt()
        encrypt.encrypt(inputFile,key)

    elif str(choice) == '2':
        inputFile = input("Type in the full path of the file you wish to encrypt:\n")
        key = input("Please type in the key to decrypt the chosen file.\n")
        decrypt = de.Decrypt()
        decrypt.decrypt(inputFile, key)



if __name__ == "__main__":
    main()

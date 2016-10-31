from _ast import keyword

__author__ = 'admin'
__name__ = '__main__'

import Encrypt as nc


def main():

    inputFile = input("Type in the full path of the file you wish to encrypt/n")
    new = nc.NewCrypto()
    key = input("Please type in key. Must be a minimum of 16 characters.")[:16]

    state = new.encrypt(inputFile, key)
    print(state)


if __name__ == "__main__":
    main()

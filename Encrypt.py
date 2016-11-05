__author__ = 'admin'
import io as io
import numpy as np
import binascii
import Utility as u
import os as os
import KeyExp as KE

class Encrypt():
    INPUT_BLOCK_SIZE = 128
    KEY_SIZE = 256
    Nb = INPUT_BLOCK_SIZE / 32
    Nk = KEY_SIZE / 32

    def encrypt(self, inputfile, key):
        output = []

        keyschedule = KE.keyExpansion(key)
        iv = np.array(np.random.random_integers(0, 1, self.INPUT_BLOCK_SIZE)).reshape(16,8)  # randomly generate bits of equal size to block size
        priorstate = iv
        with io.open(inputfile,mode='rb') as f:
                byte = []
                try:
                    for i in range(0,16):
                        byte.append(f.read(1))
                    while byte[15]:
                        state = self.decodeandBlockChain(byte,priorstate)
                        output.append(self.round(state,keyschedule))
                        try:
                            byte = []
                            for i in range(0,16):
                                byte.append(f.read(1))
                            priorstate = np.asarray(state).reshape(16,8)
                        except Exception as e:
                            print("Error: {1}".format(e))
                        finally:
                            f.close()
                except Exception as e:
                    print("Error: {1}".format(e))
                finally:
                    f.close()

        path = input("Please select file path for encrypted file:\n")
        while os.path.exists(path):
            path = input("Sorry, this file already exists, please choose a unique file path:\n")
        with io.open(path,mode='ab') as f:
           for i in iv:
                   f.write(bytearray(int(u.bitArrayToBytes(i),16)))
           for i in output:
               for x in i:
                   f.write(bytearray(int(x,16)))

    def decodeandBlockChain(self, byteArray, priorstate):
        block = []
        state = []
        for i in range(0,16):
            block.append(binascii.hexlify(byteArray[i]).decode())
            block[i] = u.bitArrayToBytes(u.byteXOR(u.bytesToBits(block[i]),priorstate[i]))
            if (i+1) % 4 == 0:
                state.append([block[i-3],block[i-2],block[i-1],block[i]])
        return state

    def round(self,state, keyschedule):
            for i in range(0,len(state)):
                for x in range(len(state[i])):
                    newthing = hex(u.SBOX[int(state[i][x],16)])
                    state[i][x] = newthing
            state = self.shiftRows(state)
            state = self.mixColumns(state)
            state = np.asarray(state).reshape(16,8)
            finalstate = []
            for i in range(0, len(state)):
                    temp = u.byteXOR(state[i],u.bytesToBits(keyschedule[i]))
                    finalstate.append(u.bitArrayToBytes(temp))
            return finalstate

    def shiftRows(self, state):
        for i in range(0, 4):
            tempstate = []
            othertempstate = []
            if i > 0:
                n = 0
                for x in range(0, i):
                    tempstate.append(state[i][x])
                for x in range(i, 4):
                    othertempstate.append(state[i][x])
                for n in range(0, len(othertempstate)):
                    state[i][n] = othertempstate[n]
                for y in range(n + 1, 4):
                    state[i][y] = tempstate[y - len(othertempstate)]
        return state

    def mixColumns(self, state):
        for i in range(0, 4):
            for n in range(0, 4):
                tempbits = u.bytesToBits(state[n][i])
                if i == 0:
                    if n == 0:
                        tempbits = self.timesTwo(tempbits)
                    elif n == 1:
                        tempbits = self.timesThree(tempbits)
                if i == 1:
                    if n == 1:
                        tempbits = self.timesTwo(tempbits)
                    elif n == 2:
                        tempbits = self.timesThree(tempbits)
                if i == 2:
                    if n == 2:
                        tempbits = self.timesTwo(tempbits)
                    if n == 3:
                        tempbits = self.timesThree(tempbits)
                if i == 3:
                    if n == 0:
                        tempbits = self.timesThree(tempbits)
                    if n == 3:
                        tempbits = self.timesTwo(tempbits)
                state[n][i] = tempbits
        return state

    def timesThree(self, byte):
        return u.bytesToBits(u.THREEXTABLE[int(str(byte).replace('[', '').replace(']','').replace(',', '').replace(' ', ''),2)])

    def timesTwo(self, bits):
        for i in range(0,7):
            if bits[0] == 1:
                bits[i] = bits[i + 1]
                bits[7] = 0
                bits = u.byteXOR(bits, [0,0,0,1,1,0,1,1])
            else:
                bits[i] = bits[i + 1]
                bits[7] = 0
        return bits

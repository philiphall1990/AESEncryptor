import Utility as u
import KeyExp as KE
import io
import binascii
import numpy as np
class Decrypt():

    def decrypt(self,inputFile, key):                                               # Do decrypt logic on each block.
        output = []
        keyschedule = KE.keyExpansion(key)                                          # Do Key Expansion to derive full key schedule from key.
        with io.open(inputFile, mode='rb') as f:                                    # Open file to be decrypted.
            self.byte = []                                                          # Instantiate variables.
            self.block = []
            self.state = []
            self.priorstate = []
            self.decodeandBlockChain(f)                                             # Decode file to hex, and retrieve IV or prior state.
            while self.byte[31]:                                                    # While byte has 32 elements (a single state) (Maybe should be while state is 32 elements?)
                self.byte = []  
                self.block = []
                decryptedstate = self.round(self.state, keyschedule)                # The (semi) decrypted state is the product of a single round.
                for i in range(0, 16):                                              
                    decryptedstate[i] = u.bitArrayToBytes(                          # For each element the (final) decrypted state is the XOR of the state element and the prior state element at the same position.
                        u.byteXOR(u.bytesToBits(decryptedstate[i]), 
                                  u.bytesToBits(self.priorstate[i])))
                output.append(decryptedstate)                                       # Append the final output with this state as decrypted.
                self.priorstate = decryptedstate
                self.state = []
                self.decodeandBlockChain(f)

        return output



    def decodeandBlockChain(self,f):
        try:
            for i in range(0, 32):
                try:
                    self.byte.append(f.read(1))
                except:
                    print("Reached File End")
                if len(self.byte) < i + 1:
                    self.block.append('0x00')
                else:
                    self.block.append(binascii.hexlify(self.byte[i]).decode())
                if i < 16 and len(self.priorstate) < 16:
                    self.priorstate.append(self.block[i])

                if i >= 16 and (i + 1) % 4 == 0:
                    self.state.append([self.block[i - 3], self.block[i - 2], self.block[i - 1], self.block[i]])
        except Exception as e:
            print("Error: {1}".format(e))



    def round(self, state, keyschedule):
        for i in range(0,4):
            for x in range(0,4):
                state[i][x] = hex(u.INVSBOX[int(state[i][x],16)])
        state = self.invShiftRows(state)
        state = self.invMixColumns(state)

        state = np.asarray(state).reshape(16, 8)
        finalstate = []
        for i in range(0, len(state)):
            temp = u.byteXOR(state[i],u.bytesToBits(keyschedule[i]))
            finalstate.append(u.bitArrayToBytes(temp))
        return finalstate

    def invShiftRows(self,state):
        for i in range(0, 4):
            tempstate = []
            othertempstate = []
            if i > 0:
                n = 0
                for x in range(0,4-i):
                     tempstate.append(state[i][x])
                for x in range(4-i,4):
                    othertempstate.append(state[i][x])
                for n in range(0,len(othertempstate)):
                    state[i][n] = othertempstate[n]
                for y in range(n+1,4):
                    state[i][y] = tempstate[y-len(othertempstate)]
        return state


    def invMixColumns(self, state):
        for i in range(0,4):
            for n in range(0,4):
                tempbits = int(str(state[n][i]), 16)
                if i == 0:
                    if n == 0:
                        tempbits= u.TIMES14[int(tempbits)]
                    elif n == 1:
                        tempbits= u.TIMES11[int(tempbits)]
                    elif n == 2:
                        tempbits = u.TIMES13[int(tempbits)]
                    elif n ==3:
                        tempbits = u.TIMES9[int(tempbits)]
                if i == 1:
                    if n == 0:
                        tempbits= u.TIMES9[int(tempbits)]
                    elif n == 1:
                        tempbits= u.TIMES14[int(tempbits)]
                    elif n == 2:
                        tempbits = u.TIMES11[int(tempbits)]
                    elif n ==3:
                        tempbits = u.TIMES13[int(tempbits)]
                if i == 2:
                    if n == 0:
                        tempbits= u.TIMES13[int(tempbits)]
                    elif n == 1:
                        tempbits= u.TIMES9[int(tempbits)]
                    elif n == 2:
                        tempbits = u.TIMES14[int(tempbits)]
                    elif n ==3:
                        tempbits = u.TIMES11[int(tempbits)]
                if i == 3:
                    if n == 0:
                        tempbits= u.TIMES11[int(tempbits)]
                    elif n == 1:
                        tempbits= u.TIMES13[int(tempbits)]
                    elif n == 2:
                        tempbits = u.TIMES9[int(tempbits)]
                    elif n ==3:
                        tempbits = u.TIMES14[int(tempbits)]
                state[n][i] =  u.bytesToBits(hex(tempbits))
        return state

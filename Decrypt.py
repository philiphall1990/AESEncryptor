import Utility as u
import KeyExp as KE
import io
class Decrypt():

    def decrypt(self,inputFile, key):
        key = KE.keyExpansion(key)
        state = inputFile
        for i in range(0,4):
            for x in range(0,4):
                state[i][x] = u.INVSBOX[int(state[i][x],16)]
        with io.open(inputFile, mode='rb') as f:
            byte = []
            try:
                for i in range(0,16):
                    byte.append(f.read(1))
                while byte[15]:

                    try:
                      for i in range(0,16):
                          byte.append(f.read(1))
                    except Exception as e:
                        print("Error: {1}".format(e))
                    finally:
                        f.close()
            except Exception as e:
                print("Error: {1}".format(e))
            finally:
                f.close()

        state = self.invShiftRows(state)
        state = self.invMixColumns(state)
        return state


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
                tempbits = u.bytesToBits(state[n][i])
                if i == 0:
                    if n == 0:
                        tempbits= u.TIMES14[int(tempbits,16)]
                    elif n == 1:
                        tempbits= u.TIMES11[int(tempbits,16)]
                    elif n == 2:
                        tempbits = u.TIMES13[int(tempbits,16)]
                    elif n ==3:
                        tempbits = u.TIMES9[int(tempbits,16)]
                if i == 1:
                    if n == 0:
                        tempbits= u.TIMES9[int(tempbits,16)]
                    elif n == 1:
                        tempbits= u.TIMES14[int(tempbits,16)]
                    elif n == 2:
                        tempbits = u.TIMES11[int(tempbits,16)]
                    elif n ==3:
                        tempbits = u.TIMES13[int(tempbits,16)]
                if i == 2:
                    if n == 0:
                        tempbits= u.TIMES13[int(tempbits,16)]
                    elif n == 1:
                        tempbits= u.TIMES9[int(tempbits,16)]
                    elif n == 2:
                        tempbits = u.TIMES14[int(tempbits,16)]
                    elif n ==3:
                        tempbits = u.TIMES11[int(tempbits,16)]
                if i == 3:
                    if n == 0:
                        tempbits= u.TIMES11[int(tempbits,16)]
                    elif n == 1:
                        tempbits= u.TIMES13[int(tempbits,16)]
                    elif n == 2:
                        tempbits = u.TIMES9[int(tempbits,16)]
                    elif n ==3:
                        tempbits = u.TIMES14[int(tempbits,16)]
                state[n][i] =  tempbits
        return state

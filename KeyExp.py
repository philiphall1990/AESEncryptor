import Utility as u

def keyExpansion(key):
        word = []
        bytes = bytearray(key, encoding='ascii')
        key = []
        for i in bytes:
            key.append(bin(int(i)))
        for i in key:
            word.append('0x00')
        rconCounter = 0
        for x in range(12, 44, 4):
            holder = word[x:x + 4]
            if (x + 4) % 16 == 0:
                holder = []
                for i in __subWord(__rotWord([word[x], word[x + 1], word[x + 2], word[x + 3]])):
                    holder.append(i)
                holder[0] = u.bitArrayToBytes(u.byteXOR(u.bytesToBits(holder[0]), u.bytesToBits(u.RCON[rconCounter])))
                rconCounter += 1
            for i in range(0, 4):
                word.append(u.bitArrayToBytes(u.byteXOR(u.bytesToBits(holder[i]), u.bytesToBits(word[i + (x - 12)]))))
        return word

def __rotWord(word):
        temp = word[0]
        for i in range(1, 4):
            word[i - 1] = word[i]
        word[3] = temp
        return word

def __subWord(word):
        array = []
        for byte in word:
            index = int(byte.replace('0x', ''), 16)
            array.append(hex(u.SBOX[index]))
        return array

#trivium stream cipher
#80 bit key
#Initialization phase
#warm-up phase
#encryption phase
#structure
#3 LFSR : A,B,C (288 total bits)
#Si = (A92 XOR A65) XOR (B83 XOR B68) XOR (C110 XOR C65)
#A0 = (C110 XOR C65) XOR (C108 AND C109) XOR A68
#B0 = (A92 XOR A65) XOR (A90 AND A91) XOR B77
#C0 = (B83 XOR B68) XOR (B81 AND B82) XOR C86

#Initialization:
#80 bit IV loaded in A0-A79
#80 bit key loaded in B0-B79
#all other register bits to 0

#warm up:
#cipher clocked 4*288 = 1152
#No generated cipher output

#encryption:
#generates up to 2^64 bits of keystream

from collections import deque
import re

def str_to_bin(string):
    s = ' '.join(format(x, '08b') for x in bytearray(string,'utf-8'))
    print(s)
    s = re.sub(r'\s+','',s)
    return s

class Trivium:
    A = deque([format(0,'b')]*93)
    B = deque([format(0,'b')]*84)
    C = deque([format(0,'b')]*112)


    def Initialization(self,key,IV):
        key_bin = str_to_bin(key)
        IV_bin = str_to_bin(IV)



        if self.check_len(key_bin,IV_bin) == 0:
            return 0

        for i in range(0,len(key_bin)):
            self.B[i] = key_bin[i]

        for j in range(0,len(IV_bin)):
            self.A[j] = IV_bin[j]

        print(self.A)
        print(self.B)

        return 1

    def Warm_up(self):
        for i in range(0,1152):
            self.step()


    def Encryption(self,length,sol_register):
        for i in range(0,length):
            sol_register[i] = self.step()

    def step(self):
        sa = self.xor(self.A[92],self.A[65])
        sb = self.xor(self.B[83],self.B[68])
        sc = self.xor(self.C[110],self.C[65])
        s = self.xor(sa,self.xor(sb,sc))
        a00 = self.A[68]
        a01 = self.and_(self.C[108],self.C[109])
        a0 = self.xor(sc,self.xor(a00,a01))
        b00 = self.B[77]
        b01 = self.and_(self.A[90],self.A[91])
        b0 = self.xor(sa,self.xor(b00,b01))
        c00 = self.C[86]
        c01 = self.and_(self.B[81],self.B[82])
        c0 = self.xor(sb,self.xor(c00,c01))
        self.shift_left(self.A,a0)
        self.shift_left(self.B,b0)
        self.shift_left(self.C,c0)
        return s

    def shift_left(self,register,value):
        register.rotate(1)
        register[0] = value


    def check_len(self,key,IV):
        if len(key) > 80 or len(IV) > 80:
            return 0
        return 1

    def xor(self,str1,str2):
        if str1 == str2:
            return '0'
        else:
            return '1'

    def and_(self,str1,str2):
        if str1 != '0' and str2 != '0':
            return '1'
        else:
            return '0'

if __name__ == "__main__":
    trivium = Trivium()
    s = [0]*80
    trivium.Initialization('1234567890','1234567890')
    trivium.Warm_up()
    trivium.Encryption(80,s)
    print(s)

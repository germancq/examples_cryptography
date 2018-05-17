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
from bitstring import BitArray
import re

def str_to_bin(string):
    s = ' '.join(format(x, '08b') for x in bytearray(string,'utf-8'))
    s = re.sub(r'\s+','',s)
    return s

class Trivium:
    A = deque([0]*93)
    B = deque([0]*84)
    C = deque([0]*111)


    def Initialization(self,key,IV):

        #hex to bits
        key_ = BitArray(hex=key)
        IV_ = BitArray(hex=IV)



        self.check_len(key_.bin,IV_.bin)


        for i in range(0,len(key_.bin)):
            self.B[i] = int(key_.bin[i])

        for j in range(0,len(IV_.bin)):
            self.A[j] = int(IV_.bin[j])

        return 1

    def Warm_up(self):
        for i in range(0,1152):
            self.step()


    def Encryption(self,length):
        for i in range(0,length):
            yield self.step()

    def step(self):
        sa = self.A[92] ^ self.A[65]
        sb = self.B[83] ^ self.B[68]
        sc = self.C[110] ^ self.C[65]
        s = sa ^ sb ^ sc
        a00 = self.A[68]
        a01 = self.C[108] & self.C[109]
        a0 = sc ^ a00 ^ a01
        b00 = self.B[77]
        b01 = self.A[90] & self.A[91]
        b0 = sa ^ b00 ^ b01
        c00 = self.C[86]
        c01 = self.B[81] & self.B[82]
        c0 = sb ^ c00 ^ c01
        self.shift_right(self.A,a0)
        self.shift_right(self.B,b0)
        self.shift_right(self.C,c0)
        return s

    def shift_right(self,register,value):
        register.rotate(1)
        register[0] = int(value)


    def check_len(self,key,IV):
        if len(key) > 80 or len(IV) > 80:
            raise ValueError('values for key an IV must not exceed 80 bits')



if __name__ == "__main__":
    key = "01020304050607080900"#HEX
    IV = "01020304050607080900"#HEX


    trivium = Trivium()
    trivium.Initialization(key,IV)
    trivium.Warm_up()
    s = trivium.Encryption(80)
    print (BitArray(s).hex)

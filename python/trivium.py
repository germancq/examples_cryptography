'''
 * @Author: German Cano Quiveu, germancq@gmail.com 
 * @Date: 2019-09-21 22:20:30 
 * @Last Modified by:   German Cano Quiveu, germancq@gmail.com 
 * @Last Modified time: 2019-09-21 22:20:30 
''' 
#trivium stream cipher
#80 bit key
#Initialization phase
#warm-up phase
#encryption phase
#structure
#3 LFSR : A,B,C (288 total bits)
#Si = Aout XOR Bout XOR Cout
#A0 = Cout XOR A68 XOR (C108 AND C109)
#B0 = Aout XOR B77 XOR (A90 AND A91)
#C0 = Bout XOR C86 XOR (B81 AND B82)
#Aout = A92  XOR A65
#Bout = B83  XOR B68
#Cout = C110  XOR C65

#Initialization:
#80 bit Key loaded in A0-A79 (K1,....,K80,0,0,0..,0)
#80 bit IV loaded in B0-B79
#last 3 bits of register C is set to 1
#all other register bits to 0

#warm up:
#cipher clocked 4*288 = 1152
#No generated cipher output

#encryption:
#generates up to 2^64 bits of keystream

from collections import deque
from bitstring import BitArray


class Trivium:
    A = deque([0]*93)
    B = deque([0]*84)
    C = deque([0]*111)


    def Initialization(self,key,IV):

        #hex to bits
        key_ = BitArray(hex=key)
        IV_ = BitArray(hex=IV)
        print(key_.hex)
        key_.byteswap()
        print(key_.hex)
        IV_.byteswap()


        self.check_len(key_.bin,IV_.bin)


        for i in range(0,len(IV_.bin)):
            self.B[i] = int(IV_.bin[i])

        for j in range(0,len(key_.bin)):
            self.A[j] = int(key_.bin[j])
            
        self.C[108] = 1
        self.C[109] = 1
        self.C[110] = 1    

        return 1

    def Warm_up(self):
        for i in range(0,1152):
            self.step()


    def gen_keystream(self,length):
        keystream = []
        for i in range(0,length):
            keystream.append(self.step())
        return keystream    

    def step(self):
        Aout = self.A[92] ^ self.A[65] 
        Bout = self.B[83] ^ self.B[68]
        Cout = self.C[110] ^ self.C[65] 
        s = Aout ^ Bout ^ Cout

        A0 = Cout ^ self.A[68] ^ (self.C[108] & self.C[109])
        B0 = Aout ^ self.B[77] ^ (self.A[90] & self.A[91])
        C0 = Bout ^ self.C[86] ^ (self.B[81] & self.B[82])
        
        self.shift_right(self.A,A0)
        self.shift_right(self.B,B0)
        self.shift_right(self.C,C0)
        return s

    def shift_right(self,register,value):
        register.rotate(1)
        register[0] = int(value)


    def check_len(self,key,IV):
        if len(key) > 80 or len(IV) > 80:
            raise ValueError('values for key an IV must not exceed 80 bits')


def trivium_impl(key,iv,n):
    key = hex(key)#HEX
    IV = hex(iv)#HEX
    trivium = Trivium()
    trivium.Initialization(key,IV)
    trivium.Warm_up()
    s = trivium.gen_keystream(n)
    hex_keystream = '0b' + ''.join(str(i) for i in s[::-1])
    hex_keystream = BitArray(hex_keystream)
    print (hex_keystream.hex)
    hex_keystream.byteswap()
    print (hex_keystream.hex)
    return hex_keystream.hex


if __name__ == "__main__":
    trivium_impl(0x8000000,0x0,128)



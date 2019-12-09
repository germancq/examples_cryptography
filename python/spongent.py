# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spongent.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/12/02 13:14:32 by germancq          #+#    #+#              #
#    Updated: 2019/12/02 13:14:47 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import LFSR
import math

S_box = [0xE,0xD,0xB,0x0,0x2,0x1,0x4,0xF,0x7,0xA,0x8,0x5,0x9,0xC,0x3,0x6]

class Spongent:

    def __init__(self,n,c,r,R) :
        self.n = n
        self.c = c
        self.r = r
        self.R = R
        self.b = r + c
        self.state = 0
        self.initialize_lCounter()
        

    def generate_hash(self,message):
        self.initialization_phase(message)
        self.absorbing_phase()
        self.squeezing_phase()
        return self.result


    def initialization_phase(self,message):
        #padding message with 1 
        message = message << 1
        message = message | 0x1
        #fill with zeros until r multiple
        n = message.bit_length() % self.r
        message = message << n
        #cut into blocks of r bits
        self.m = []
        self.mask = 0xFFFF
        if(self.n <= 160):
            self.mask = 0xFF
            
        for i in range(0,(message.bit_length()/self.r)):
            self.m.append(((message >> (self.r * i)) & mask)) 
        


    def absorbing_phase(self):
        for i in range(0,len(self.m)):
            self.state = self.state ^ self.m[i]
            self.permutation()
        


    def squeezing_phase(self):
        self.result = 0
        for i in range(0, self.n/self.r):
           self.result = ((self.state & self.mask)<<(i*self.r)) | result     
           self.permutation()


    def initialize_lCounter(self):
        size = math.ceil(math.log2(self.R))
        
        initial_state_options = {
            88: 0x5,
            128: 0x7A,
            160: 0x45,
            224: 0x01,
            256: 0x9E
        }

        feedback_coefficients_options = {
            88: 0x61,
            128: 0xC1,
            160: 0xC1,
            224: 0xC1,
            256: 0x11D
        }

        self.initial_lCounter_state = initial_state_options.get(self.n,0x0)
        feedback_coefficients = feedback_coefficients_options.get(self.n,0x0)

        self.lCounter = LFSR.LFSR(size,self.initial_lCounter_state,feedback_coefficients)


    def permutation(self):
        self.lCounter.set_state(self.initial_lCounter_state)
        for i in range (0,self.R):
            reverse_counter = reverse_bits(self.lCounter.get_state())
            self.state = self.state ^ reverse_counter ^ self.lCounter.get_state()
            self.lCounter.step()
            self.sBoxLayer()
            self.pLayer()
     
    
    def reverse_bits(self,data):
        result = 0
        for i in range (0,data.bit_length()):
           result = (((data>>(data.bit_length-i-1)) & 0x1))<<i | result
                    
    def sBoxLayer(self):
        new_state = 0
        for i in range(0,self.b/4):
            index = (self.state >> 4*i) & 0xF    
            new_state = (S_box[index]<<4*i) | new_state
        
        self.state = new_state   
        
    def pLayer(self):
        new_state = 0
        for i in range (0,b): 
            bit_pos = i * (self.b/4)
            if(i == b-1):
                bit_pos = i
            value_bit = (self.state >> i) & 0x1
            new_state = (value_bit << bit_pos) | new_state
            
        self.state = new_state
                
                    


if __name__ == "__main__":
    print()    
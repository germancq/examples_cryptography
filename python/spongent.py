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
        self.initialize_lCounter()
        

    def initialization_phase(self):
        print()


    def absorbing_phase(self):
        print()


    def squeezing_phase(self):
        print()    

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




if __name__ == "__main__":
    print()    
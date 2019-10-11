# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hirose_present.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/11 10:39:41 by germancq          #+#    #+#              #
#    Updated: 2019/10/11 12:31:42 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import present
import math



class HirosePresent :
    
    def __init__(self,c):
        self.c = c 
        self.present_right = present.Present(0x00000000000000000000)
        self.present_left  = present.Present(0x00000000000000000000)

    def generate_hash(self,plaintext) :
        #key in Present is 80 bits
        # the key iterates is the concatenation of right present with 16 bits of plaintext

        hr_prev = 0x0000000000000000
        hl_prev = 0x0000000000000000
        
        print(math.log2(plaintext))
        i = math.ceil(math.log2(plaintext)/16)
        print(i)
        
        while i > 0 :
            print("+++++++++++++++++++++++++++++++++++")
            print(i)
            i = i - 1
            print(hex(plaintext))
            m_i = plaintext & 0xFFFF
            plaintext = plaintext >> 16
            key_i = (hr_prev << 16) | m_i
            print(hex(m_i))
            print(hex(key_i))
            print(hex(hl_prev))
            print(hex(hr_prev))

            self.present_right.refresh_key(key_i)
            self.present_left.refresh_key(key_i)

            plaintext_right = self.c ^ hl_prev
            hr_i = self.present_right.encrypt(plaintext_right)
            hr_prev = hr_i ^ plaintext_right

            plaintext_left = hl_prev
            hl_i = self.present_left.encrypt(plaintext_left)
            hl_prev = hl_i ^ plaintext_left
            print("++++++++++++++++++++++++++++++++++++")


        print("////////////////////////////////")
        print(hex(hl_prev))
        print(hex(hr_prev))
        return ((hl_prev<<64) | hr_prev)
      



if __name__ == "__main__":
    hirose_present_hash_impl = HirosePresent(0x1234567812345678)
    hash_value = hirose_present_hash_impl.generate_hash(0x1234567887654321)
    print(hex(hash_value))
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    twofish.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/21 16:43:56 by germancq          #+#    #+#              #
#    Updated: 2019/10/23 18:08:09 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''
key 128 bits
'''

MDS = [[0x01,0xef,0x5b,0x5b],
       [0x5b,0xef,0xef,0x01],
       [0xef,0x5b,0x01,0xef],
       [0xef,0x01,0xef,0x5b]]

RS = [[0x01,0xa4,0x55,0x87,0x5a,0x58,0xdb,0x9e],
      [0xa4,0x56,0x82,0xf3,0x1e,0xc6,0x68,0xe5],
      [0x02,0xa1,0xfc,0xc1,0x47,0xae,0x3d,0x19],
      [0xa4,0x55,0x87,0x5a,0x58,0xdb,0x9e,0x03]]       

Sbox_q0 = [[0x8,0x1,0x7,0xD,0x6,0xF,0x3,0x2,0x0,0xB,0x5,0x9,0xE,0xC,0xA,0x4],
           [0xE,0xC,0xB,0x8,0x1,0x2,0x3,0x5,0xF,0x4,0xA,0x6,0x7,0x0,0x9,0xD],
           [0xB,0xA,0x5,0xE,0x6,0xD,0x9,0x0,0xC,0x8,0xF,0x3,0x2,0x4,0x7,0x1],
           [0xD,0x7,0xF,0x4,0x1,0x2,0x6,0xE,0x9,0xB,0x3,0x0,0x8,0x5,0xC,0xA]]   

Sbox_q1 = [[0x2,0x8,0xB,0xD,0xF,0x7,0x6,0xE,0x3,0x1,0x9,0x4,0x0,0xA,0xC,0x5],
           [0x1,0xE,0x2,0xB,0x4,0xC,0x3,0x7,0x6,0xD,0xA,0x5,0xF,0x9,0x0,0x8],
           [0x4,0xC,0x7,0x5,0x1,0x6,0x9,0xA,0x0,0xE,0xD,0x8,0x2,0xB,0x3,0xF],
           [0xB,0x9,0x5,0x1,0xC,0x3,0xD,0xE,0x6,0x4,0x7,0xF,0x2,0x0,0x8,0xA]]                 


class Twofish :
    
    def __init__(self,key):
        k = key_schedule(key)
        self.M_e = k[0]
        self.M_o = k[1]
        self.S_i = k[2]

    def encrypt(self,plaintext) :    
        plaintext_0 = plaintext & (2**32 - 1)
        plaintext_1 = (plaintext>>32) & (2**32 - 1)
        plaintext_2 = (plaintext>>64) & (2**32 - 1)
        plaintext_3 = (plaintext>>96) & (2**32 - 1)
        
        k_0 = generate_K_values(0,self.M_e,self.M_o)
        print(hex(k_0[0]))
        print(hex(k_0[1]))
        
        k_1 = generate_K_values(1,self.M_e,self.M_o)

        print(hex(k_1[0]))
        print(hex(k_1[1]))
        '''
        R_0 = plaintext_0 ^ k_0[0]
        R_1 = plaintext_1 ^ k_0[1]
        R_2 = plaintext_2 ^ k_1[0]
        R_3 = plaintext_3 ^ k_1[1]

        
        for i in range(0,15):
            #print(i)
            #print(hex(R_0))
            #print(hex(R_1))
            #print(hex(R_2))
            #print(hex(R_3))
            f = function_F(R_0,R_1,i,self.M_e,self.M_o,self.S_i)
            R_0 = ROR(f[0] ^ R_2, 1, 32)      
            R_1 = ROL(R_3,1,32) ^ f[1]  
            R_2 = R_0
            R_3 = R_1

        k_2 = generate_K_values(2,self.M_e,self.M_o)   
        k_3 = generate_K_values(3,self.M_e,self.M_o)     
        
        C_0 = R_2 ^ k_2[0]
        C_1 = R_3 ^ k_2[1]
        C_2 = R_0 ^ k_3[0]
        C_3 = R_1 ^ k_3[1]

        return (C_3 << 96) + (C_2 << 64) + (C_1 << 32) + C_0 
        '''
        return 0

def function_F(x,y,round,M_e,M_o,S_i):

    T0 = function_g(x,S_i)
    y = ROL(y,8,32)
    T1 = function_g(y,S_i)
    K_r = generate_K_values(round+8,M_e,M_o)
    F0 = (T0 + T1 + K_r[0]) & (2**32 - 1)
    F1 = (T0 + (T1<<1) + K_r[1]) & (2**32 - 1)
    return (F0,F1)



def function_g(x,S_i):
      
    return function_h(x,S_i)


def key_schedule(key):
    m_i = [[] for i in range(8)]
    M_i = []
    S_i = []
    for i in range(0,2):
        for j in range(0,8):
            m_i[i].append((key>>(8*(i+j))) & 0xFF)
        r = matrix_multiplication(RS,m_i[i])
        
        S_i.append((r[3][0]<<24) + (r[2][0]<<16) + (r[1][0]<<8) + r[0][0])
            
    for i in range(0,8) :
        M_i.append((key >> 32*i) & 0xFFFFFFFF)
    
    M_e = [M_i[0],M_i[2]]
    M_o = [M_i[1],M_i[3]]

    
    return (M_e,M_o,S_i) 


def function_h(X,L):
    #print("start function_h")
    #print(hex(X))
    #print(L)
    

    selected_boxes = [[0,1,0,1],
                      [0,0,1,1],
                      [1,0,1,0]]
    input_x = X
    y = 0
    for i in range(0,3):
        x_0 = input_x & 0xFF
        x_1 = (input_x>>8) & 0xFF
        x_2 = (input_x>>16) & 0xFF
        x_3 = (input_x>>24) & 0xFF
        
        y_0 = generate_q_output(selected_boxes[i][0],x_0)
        y_1 = generate_q_output(selected_boxes[i][1],x_1)
        y_2 = generate_q_output(selected_boxes[i][2],x_2)
        y_3 = generate_q_output(selected_boxes[i][3],x_3)
       

        y = ((y_3<<24) + (y_2<<16) + (y_1<<8) + y_0)
        #print(hex(y))
        
        if(i != 2):
            input_x = y ^ L[i]
            
        #y = y & (2**32 - 1)
    

    print(hex(y))
    z_matrix =  matrix_multiplication(MDS,[y_0,y_1,y_2,y_3]) 
    
    print(hex(z_matrix[3][0]))
    print(hex(z_matrix[2][0]))
    print(hex(z_matrix[1][0]))
    print(hex(z_matrix[0][0]))

    z_3 = z_matrix[3][0] & 0xFF
    z_2 = z_matrix[2][0] & 0xFF
    z_1 = z_matrix[1][0] & 0xFF
    z_0 = z_matrix[0][0] & 0xFF

    z = ((z_3<<24)  +  
         (z_2<<16)  + 
         (z_1<<8)  + 
         (z_0))      
 
    #print("end function_h")
    

    return z


def generate_q_output(q_i,x):
    
    t_box = Sbox_q0
    if(q_i == 1):
        t_box = Sbox_q1
    
    a0 = x>>4 & 0xf
    b0 = x & 0xf
    a1 = a0 ^ b0 
    b1 = a0 ^ ROR(b0,1,4) ^ ((a0<<3) & 0xF)
    a2 = t_box[0][a1]
    b2 = t_box[1][b1]
    a3 = a2 ^ b2
    b3 = a2 ^ ROR(b2,1,4) ^ ((a2<<3) & 0xF)
    a4 = t_box[2][a3]
    b4 = t_box[3][b3]

    
    z = (b4<<4) + a4
    
    return z & 0xFF


def generate_K_values(i,M_e,M_o):
    p = 2**24 + 2**16 + 2**8 + 2**0
    A = function_h(p<<i,M_e)
    print(hex(A))
    B = function_h((p<<i)+1,M_o)
    B = ROL(B,8,32)
    print(hex(B))
    K_0 = A+B & (2**32 - 1) #K_2i
    K_1 = (A+(B<<1)) & (2**32 - 1)
    K_1 = ROL(K_1,9,32) #K_2i+1
    return (K_0,K_1)


def matrix_multiplication(M1,M2) :
    
    rows_a = len(M1)
    rows_b = len(M2) # == colums_a
    colums_a = rows_b
    colums_b = 1
    if(type(M2[0]) is list) : 
        colums_b = len(M2[0])
    
    result = []
    

    for i in range(0,rows_a) :
        result.append([])
        for j in range(0,colums_b) :    
            result[i].append(0)
            for k in range(0,rows_b):
                a_1 = result[i][j]

                if(colums_b > 1):
                    a_3 = M2[k][j]
                else :
                    a_3 = M2[j]

                if(colums_a > 1) :
                    a_2 = M1[i][k]   
                else :
                     a_2 = M1[k]
                    
                result[i][j] = (a_1 + (a_2 * a_3))

    return result


def ROL(x,i,len_bits):
    j = len_bits - i
    return ((x<<i) | (x>>j)) & (2**len_bits - 1) 

def ROR(x,i,len_bits):
    j = len_bits - i
    return ((x>>i) | (x<<j)) & (2**len_bits - 1)     


if __name__ == "__main__":
    
    key = 0x0
    plaintext = 0x0
    cipher = Twofish(key)
    result = cipher.encrypt(plaintext)
    print(hex(result))
    
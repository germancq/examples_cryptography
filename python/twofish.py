# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    twofish.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/21 16:43:56 by germancq          #+#    #+#              #
#    Updated: 2019/10/21 18:22:58 by germancq         ###   ########.fr        #
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


def function_F(x,y,round):
    print()
    T0 = function_g(x)
    T1 = function_g(y<<8)



def function_g(x):
    print()    
    return 0


def matrix_multiplication(M1,M2) :
    result = []

    rows_a = len(M1)
    rows_b = len(M2) # == colums_a
    colums_b = len(M2[0])
    
    for i in range(0,rows_a) :
        for j in range(0,colums_b) :
            result[i][j] = 0
            for k in range(0,rows_b):
                result[i][j] = (result[i][j]) + (M1[i][k] * M2[k][j])

    return result

if __name__ == "__main__":
    print()
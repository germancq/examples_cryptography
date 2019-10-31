# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    matrix_multiplication_test.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/31 12:35:02 by germancq          #+#    #+#              #
#    Updated: 2019/10/31 15:32:00 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cocotb
from cocotb.regression import TestFactory
from cocotb.result import TestFailure, ReturnValue
from cocotb.triggers import Timer
import numpy as np
import random
import math


def setup_function(dut, a, b, p):
    dut.a = a
    dut.b = b
    dut.p = p


@cocotb.coroutine
def calculate_result(dut, expected_s):
    yield Timer(1000)
    
    
    print(hex(int(dut.a[0].value)))
    print(hex(int(dut.a[1].value)))
    print(hex(int(dut.a[2].value)))
    print(hex(int(dut.a[3].value)))
    print(hex(int(dut.a[4].value)))
    print(hex(int(dut.a[5].value)))
    print(hex(int(dut.a[6].value)))
    print(hex(int(dut.a[7].value)))
    print(hex(int(dut.a[8].value)))
    print(hex(int(dut.a[9].value)))
    print(hex(int(dut.a[10].value)))
    print(hex(int(dut.a[11].value)))
    print(hex(int(dut.a[12].value)))
    print(hex(int(dut.a[13].value)))
    print(hex(int(dut.a[14].value)))
    print(hex(int(dut.a[15].value)))
    print("----------------------------")
    print(hex(int(dut.b[0].value)))
    print(hex(int(dut.b[1].value)))
    print(hex(int(dut.b[2].value)))
    print(hex(int(dut.b[3].value)))
    print("----------------------------")  
    print(hex(int(dut.s[0].value)))
    print(hex(int(dut.s[1].value)))
    print(hex(int(dut.s[2].value)))
    print(hex(int(dut.s[3].value)))
    


    if(dut.s[0] != expected_s[0][0]) :
            raise TestFailure("""Error matrix_multiplication value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s[0].value)),hex(expected_s[0][0])))


    if(dut.s[1] != expected_s[1][0]) :
            raise TestFailure("""Error matrix_multiplication value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s[1].value)),hex(expected_s[1][0])))

    if(dut.s[2] != expected_s[2][0]) :
            raise TestFailure("""Error matrix_multiplication value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s[2].value)),hex(expected_s[2][0])))

    if(dut.s[3] != expected_s[3][0]) :
            raise TestFailure("""Error matrix_multiplication value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s[3].value)),hex(expected_s[3][0])))
    

def matrix_multiplication_GF256(M1,M2,p) :
    
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
                    a_3 = M2[k]

                if(colums_a > 1) :
                    a_2 = M1[i][k]   
                else :
                     a_2 = M1[k]
                    
                #result[i][j] = (a_1 + (a_2 * a_3))
                gf_1 = galois_multiplication(a_2,a_3,p)
                
                result[i][j] = galois_add(a_1,gf_1)

    return result


def galois_add(a,b) :
    return a ^ b    

def galois_multiplication(a,b,p):    
    #GF(256)
    t = 0
    if(type(b) is list) :
        b = b[0]
    for i in range(0,8):
        mask = 0x1<<i
        bit_b = b & mask
        b_i = 0 if bit_b == 0 else 1 
        r = b_i*(a<<i) 
        t = galois_add(t,r)
        

    t = reduced_polinomial_GF256(t,p)
       


    return t    

def reduced_polinomial_GF256(a,p):
    #grado del polinomio p
    n = math.ceil(math.log(p,2))
    n = n - 1 
    t = a
    for i in range(15,7,-1):
        mask = 0x1<<i
        bit_t = t & mask
        t_i = 0 if bit_t == 0 else 1
        if(t_i):
            m = int(i - n)
            t = galois_add(p<<m ,t)

    return t    


@cocotb.coroutine
def run_test(dut, a = 0, b= 0):

    a = [[0x01,0xef,0x5b,0x5b],
         [0x5b,0xef,0xef,0x01],
         [0xef,0x5b,0x01,0xef],
         [0xef,0x01,0xef,0x5b]]

    b0 = random.randint(0,255)
    b1 = random.randint(0,255)
    b2 = random.randint(0,255)
    b3 = random.randint(0,255)

    b = [[b0],
         [b1],
         [b2],
         [b3]]
    
    p = 0x169
    expected_s = matrix_multiplication_GF256(a,b,p)

    a = [0x01,0xef,0x5b,0x5b,
         0x5b,0xef,0xef,0x01,
         0xef,0x5b,0x01,0xef,
         0xef,0x01,0xef,0x5b]

    b = [b0,
         b1,
         b2,
         b3]     

    setup_function(dut,a,b,p)
    yield calculate_result(dut,expected_s)


n = 10
factory = TestFactory(run_test)

factory.add_option("a", np.random.randint(low=0,high=(2**8)-1,size=n))  
factory.add_option("b", np.random.randint(low=0,high=(2**8)-1,size=n))  
factory.generate_tests()
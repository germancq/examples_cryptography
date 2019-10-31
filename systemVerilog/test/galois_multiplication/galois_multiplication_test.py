# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    galois_multiplication_test.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/30 15:24:04 by germancq          #+#    #+#              #
#    Updated: 2019/10/31 15:35:51 by germancq         ###   ########.fr        #
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
    
    print(hex(int(dut.m_out[0].value)))
    print(hex(int(dut.m_out[1].value)))
    print(hex(int(dut.m_out[2].value)))
    print(hex(int(dut.m_out[3].value)))
    print(hex(int(dut.m_out[4].value)))
    print(hex(int(dut.m_out[5].value)))
    print(hex(int(dut.m_out[6].value)))
    print(hex(int(dut.m_out[7].value)))
    print(hex(int(dut.m_out[8].value)))
    print(hex(int(dut.m_out[9].value)))
    print(hex(int(dut.m_out[10].value)))
    print(hex(int(dut.m_out[11].value)))
    print(hex(int(dut.m_out[12].value)))
    print(hex(int(dut.m_out[13].value)))
    print(hex(int(dut.m_out[14].value)))
    print("/////////////////////////////")
    print(hex(int(dut.polinomial_inst.polinomials[7].value)))
    #print(hex(int(dut.polinomial_inst.s.value)))
    #print(hex(int(dut.polinomial_inst.m_out[6].value)))
    print(hex(int(dut.polinomial_inst.polinomials[6].value)))
    print(hex(int(dut.polinomial_inst.polinomials[5].value)))
    #print(hex(int(dut.polinomial_inst.m_out[5].value)))
    print(hex(int(dut.polinomial_inst.polinomials[4].value)))
    #print(hex(int(dut.polinomial_inst.m_out[4].value)))
    print(hex(int(dut.polinomial_inst.polinomials[3].value)))
    #print(hex(int(dut.polinomial_inst.m_out[3].value)))
    print(hex(int(dut.polinomial_inst.polinomials[2].value)))
    #print(hex(int(dut.polinomial_inst.m_out[2].value)))
    print(hex(int(dut.polinomial_inst.polinomials[1].value)))
    #print(hex(int(dut.polinomial_inst.m_out[1].value)))
    print(hex(int(dut.polinomial_inst.polinomials[0].value)))
    #print(hex(int(dut.polinomial_inst.m_out[0].value)))
    
    
    print(hex(int(dut.s.value)))
    
    if(dut.s != expected_s) :
            raise TestFailure("""Error multiplication value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s.value)),hex(expected_s)))

   
def galois_add(a,b) :
    return a ^ b    

def galois_multiplication(a,b,p):    
    #GF(256)
    t = 0
    
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

    
    p = 0x169
    expected_s = galois_multiplication(a,b,p)
    setup_function(dut,a,b,p)
    yield calculate_result(dut,expected_s)



n = 10
factory = TestFactory(run_test)

factory.add_option("a", np.random.randint(low=0,high=(2**8)-1,size=n))  
factory.add_option("b", np.random.randint(low=0,high=(2**8)-1,size=n))  
factory.generate_tests()
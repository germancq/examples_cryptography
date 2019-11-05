# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    twofish_stage_test.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/05 13:05:31 by germancq          #+#    #+#              #
#    Updated: 2019/11/05 13:44:44 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cocotb
import numpy as np
import time
import random
import math
from cocotb.triggers import Timer,RisingEdge, FallingEdge
from cocotb.regression import TestFactory
from cocotb.result import TestFailure, ReturnValue
from cocotb.clock import Clock

import importlib
import sys
sys.path.append('/home/germancq/gitProjects/examples_cryptography/python')
import twofish


def setup_function(dut, Me, Mo, Si, R0, R1, R2, R3, enc_dec):
    dut.i = 0
    dut.enc_dec = enc_dec
    dut.R0 = R0
    dut.R1 = R1
    dut.R2 = R2
    dut.R3 = R3
    dut.Si = Si
    dut.Me = Me    
    dut.Mo = Mo

@cocotb.coroutine
def calculate_values(dut,expected_values):
    for i in range (0,16):
        dut.i = i
        yield Timer(100)
        print("verilog-values")
    
        print(hex(int(dut.i.value)))
        print(hex(int(dut.R0.value)))
        print(hex(int(dut.R1.value)))
        print(hex(int(dut.R2.value)))
        print(hex(int(dut.R3.value)))
        print(hex(int(dut.F0.value)))
        print(hex(int(dut.F1.value)))
        print(hex(int(dut.Z0.value)))
        print(hex(int(dut.Z1.value)))
        print(hex(int(dut.Z2.value)))
        print(hex(int(dut.Z3.value)))
        print(hex(expected_values[4*i]))
        print(hex(expected_values[(4*i)+1]))
        print(hex(expected_values[(4*i)+2]))
        print(hex(expected_values[(4*i)+3]))
        print("end-verilog-values")
        if(dut.Z0 != expected_values[4*i]) :
            raise TestFailure("""Error Z0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Z0.value)),hex(expected_values[4*i])))   
        if(dut.Z1 != expected_values[(4*i)+1]) :
            raise TestFailure("""Error Z1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Z1.value)),hex(expected_values[(4*i)+1])))   
        if(dut.Z2 != expected_values[(4*i)+2]) :
            raise TestFailure("""Error Z2 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Z2.value)),hex(expected_values[(4*i)+2])))  
        if(dut.Z3 != expected_values[(4*i)+3]) :
            raise TestFailure("""Error Z3 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Z3.value)),hex(expected_values[(4*i)+3])))  

        


@cocotb.coroutine
def run_test(dut, key = 0):
    #key = random.randint(0,(2**128)-1)
    #print(hex(key))
    key = random.randint(0,(2**128)-1)
    R0 = random.randint(0,(2**32)-1)
    R1 = random.randint(0,(2**32)-1)
    R2 = random.randint(0,(2**32)-1)
    R3 = random.randint(0,(2**32)-1)
    twofish_SW = twofish.Twofish(key)
    Me = twofish_SW.M_e
    Mo = twofish_SW.M_o
    Si = twofish_SW.S_i

    expected_enc_values = []
    expected_dec_values = []

    for i in range (0,16):
       
        enc_values = twofish.enc_stage(R0,R1,R2,R3,Me,Mo,Si,i)
        expected_enc_values.append(enc_values[0])
        expected_enc_values.append(enc_values[1])
        expected_enc_values.append(enc_values[2])
        expected_enc_values.append(enc_values[3])
        dec_values = twofish.dec_stage(R0,R1,R2,R3,Me,Mo,Si,i)
        expected_dec_values.append(dec_values[0])
        expected_dec_values.append(dec_values[1])
        expected_dec_values.append(dec_values[2])
        expected_dec_values.append(dec_values[3])


    #encrypt
    print("ENCRYPT")
    enc_dec = 0
    
    

    setup_function(dut,Me,Mo,Si,R0,R1,R2,R3,enc_dec)
    yield calculate_values(dut,expected_enc_values)

    #decrypt
    print("DECRYPT")
    enc_dec = 1
    
    

    setup_function(dut,Me,Mo,Si,R0,R1,R2,R3,enc_dec)
    yield calculate_values(dut,expected_dec_values)



n = 10
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests() 
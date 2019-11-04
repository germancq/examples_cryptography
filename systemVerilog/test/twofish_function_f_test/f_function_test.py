# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    f_function_test.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/04 17:21:12 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 17:29:30 by germancq         ###   ########.fr        #
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


def setup_function(dut, Me, Mo, Si, R0, R1):
    dut.i = 0
    dut.R0 = R0
    dut.R1 = R1
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
        print(hex(int(dut.T0.value)))
        print(hex(int(dut.T1.value)))
        print(hex(int(dut.K0.value)))
        print(hex(int(dut.K1.value)))
        print(hex(int(dut.F0.value)))
        print(hex(int(dut.F1.value)))
        print(hex(expected_values[2*i]))
        print(hex(expected_values[(2*i)+1]))
        print("end-verilog-values")
        if(dut.F0 != expected_values[2*i]) :
            raise TestFailure("""Error F0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.F0.value)),hex(expected_values[2*i])))   
        if(dut.F1 != expected_values[(2*i)+1]) :
            raise TestFailure("""Error F1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.F1.value)),hex(expected_values[(2*i)+1])))   



@cocotb.coroutine
def run_test(dut, key = 0):
    #key = random.randint(0,(2**128)-1)
    #print(hex(key))
    key = random.randint(0,(2**128)-1)
    R0 = random.randint(0,(2**32)-1)
    R1 = random.randint(0,(2**32)-1)
    twofish_SW = twofish.Twofish(key)
    Me = twofish_SW.M_e
    Mo = twofish_SW.M_o
    Si = twofish_SW.S_i

    expected_values = []

    for i in range (0,16):
        f_values = twofish.function_F(R0,R1,i,Me,Mo,Si)
        expected_values.append(f_values[0])
        expected_values.append(f_values[1])

    
    

    setup_function(dut,Me,Mo,Si,R0,R1)
    yield calculate_values(dut,expected_values)
    



n = 10
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests() 
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expanded_key_words_test.py                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/04 16:26:33 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 16:44:23 by germancq         ###   ########.fr        #
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


def setup_function(dut, Me, Mo):
    dut.i = 0
    dut.Me = Me    
    dut.Mo = Mo

@cocotb.coroutine
def calculate_values(dut,expected_values):

    for i in range (0,16):
        dut.i = i
        yield Timer(100)
        print("verilog-values")
    
        print(hex(int(dut.i.value)))
        print(hex(int(dut.m.value)))
        print(hex(int(dut.h1_input.value)))
        print(hex(int(dut.A.value)))
        print(hex(int(dut.B.value)))
        print(hex(int(dut.K_0.value)))
        print(hex(int(dut.K_1.value)))
        print(hex(expected_values[2*i]))
        print(hex(expected_values[(2*i)+1]))
        print("end-verilog-values")
        if(dut.K_0 != expected_values[2*i]) :
            raise TestFailure("""Error key_0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.K_0.value)),hex(expected_values[2*i])))   
        if(dut.K_1 != expected_values[(2*i)+1]) :
            raise TestFailure("""Error key_1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.K_1.value)),hex(expected_values[(2*i)+1])))   



@cocotb.coroutine
def run_test(dut, key = 0):
    #key = random.randint(0,(2**128)-1)
    #print(hex(key))
    key = random.randint(0,(2**128)-1)
    twofish_SW = twofish.Twofish(key)
    Me = twofish_SW.M_e
    Mo = twofish_SW.M_o

    expected_values = []

    for i in range (0,16):
        k_values = twofish.generate_K_values(i,Me,Mo)
        expected_values.append(k_values[0])
        expected_values.append(k_values[1])

    setup_function(dut,Me,Mo)
    yield calculate_values(dut,expected_values)
    



n = 10
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()    
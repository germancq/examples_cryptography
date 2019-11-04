# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    function_h_test.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/04 15:33:36 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 15:57:09 by germancq         ###   ########.fr        #
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


def setup_function(dut, x, L):
    dut.X = x
    dut.L = L    

@cocotb.coroutine
def calculate_values(dut,expected_y):
    yield Timer(100)
    print("verilog-values")
    
    print(hex(int(dut.X.value)))
    print(hex(int(dut.Q0.value)))
    print(hex(int(dut.X1.value)))
    print(hex(int(dut.Q1.value)))
    print(hex(int(dut.X2.value)))
    print(hex(int(dut.Q2[0].value)))
    print(hex(int(dut.Q2[1].value)))
    print(hex(int(dut.Q2[2].value)))
    print(hex(int(dut.Q2[3].value)))
    print(hex(int(dut.y[0].value)))
    print(hex(int(dut.y[1].value)))
    print(hex(int(dut.y[2].value)))
    print(hex(int(dut.y[3].value)))
    print(hex(int(dut.Z.value)))
    
    print("end-verilog-values")
    
    if(dut.Z != expected_y) :
            raise TestFailure("""Error Z value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Z.value)),hex(expected_y)))   



@cocotb.coroutine
def run_test(dut, x = 0, L0=0, L1=0):
    #key = random.randint(0,(2**128)-1)
    #print(hex(key))
    #key = 0
    expected_y = twofish.function_h(x,[L0,L1])


    setup_function(dut,x,[L0,L1])
    yield calculate_values(dut,expected_y)
    



n = 10
factory = TestFactory(run_test)

factory.add_option("x", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.add_option("L0", np.random.randint(low=0,high=(2**8)-1,size=n))
factory.add_option("L1", np.random.randint(low=0,high=(2**8)-1,size=n))
factory.generate_tests()    
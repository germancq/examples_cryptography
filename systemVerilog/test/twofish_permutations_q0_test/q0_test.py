# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    q0_test.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/04 12:46:56 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 15:59:28 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cocotb
import numpy as np
import time
import random
from cocotb.triggers import Timer,RisingEdge, FallingEdge
from cocotb.regression import TestFactory
from cocotb.result import TestFailure, ReturnValue
from cocotb.clock import Clock

import importlib
import sys
sys.path.append('/home/germancq/gitProjects/examples_cryptography/python')
import twofish


def setup_function(dut, x):
    dut.x = x    


@cocotb.coroutine
def calculate_values(dut,expected_y):
    yield Timer(100)
    print("verilog-values")
    '''
    print(hex(int(dut.a0.value)))
    print(hex(int(dut.b0.value)))
    print(hex(int(dut.a1.value)))
    print(hex(int(dut.b1.value)))
    print(hex(int(dut.a2.value)))
    print(hex(int(dut.b2.value)))
    print(hex(int(dut.a3.value)))
    print(hex(int(dut.b3.value)))
    print(hex(int(dut.a4.value)))
    print(hex(int(dut.b4.value)))
    print(hex(int(dut.y.value)))
    '''
    print("end-verilog-values")
    
    if(dut.q0 != expected_y) :
            raise TestFailure("""Error q0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.q0.value)),hex(expected_y)))   


@cocotb.coroutine
def run_test(dut, x = 0):
    #key = random.randint(0,(2**128)-1)
    #print(hex(key))
    #key = 0
    expected_y = twofish.generate_q_output(0,x)

    setup_function(dut,x)
    yield calculate_values(dut,expected_y)
    



n = 10
factory = TestFactory(run_test)

factory.add_option("x", np.random.randint(low=0,high=(2**8)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

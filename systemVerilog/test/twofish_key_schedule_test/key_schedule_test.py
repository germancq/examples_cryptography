# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    key_schedule_test.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/03 11:49:43 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 12:18:03 by germancq         ###   ########.fr        #
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


def setup_function(dut, key):
    dut.key = key

@cocotb.coroutine
def calculate_values(dut,expected_Me,expected_Mo,expected_Si):
    yield Timer(100)
    print("verilog-values")
    print(hex(int(dut.Me[0].value)))
    print(hex(int(dut.Me[1].value)))
    print(hex(int(dut.Mo[0].value)))
    print(hex(int(dut.Mo[1].value)))
    print(hex(int(dut.m0.s[0].value)))
    print(hex(int(dut.m0.s[1].value)))
    print(hex(int(dut.m0.s[2].value)))
    print(hex(int(dut.m0.s[3].value)))
    print(hex(int(dut.m1.s[0].value)))
    print(hex(int(dut.m1.s[1].value)))
    print(hex(int(dut.m1.s[2].value)))
    print(hex(int(dut.m1.s[3].value)))
    print(hex(int(dut.Si[0].value)))
    print(hex(int(dut.Si[1].value)))

    print("end-verilog-values")
    
    if(dut.Me[0] != expected_Me[0]) :
            raise TestFailure("""Error Me_0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Me[0].value)),hex(expected_Me[0])))   
    if(dut.Me[1] != expected_Me[1]) :
        raise TestFailure("""Error Me_1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Me[1].value)),hex(expected_Me[1])))   
    if(dut.Mo[0] != expected_Mo[0]) :
        raise TestFailure("""Error Mo_0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Mo[0].value)),hex(expected_Mo[0])))   
    if(dut.Mo[1] != expected_Mo[1]) :
        raise TestFailure("""Error Mo_1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Mo[1].value)),hex(expected_Mo[1])))   
    if(dut.Si[0] != expected_Si[0]) :
        raise TestFailure("""Error Si_0 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Si[0].value)),hex(expected_Si[0])))   
    if(dut.Si[1] != expected_Si[1]) :
        raise TestFailure("""Error Si_1 value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.Si[1].value)),hex(expected_Si[1])))   


@cocotb.coroutine
def run_test(dut, key = 0):
    key = random.randint(0,(2**128)-1)
    #print(hex(key))
    #key = 0
    twofish_SW = twofish.Twofish(key)
    expected_Me = twofish_SW.M_e
    expected_Mo = twofish_SW.M_o
    expected_Si = twofish_SW.S_i
    setup_function(dut,key)
    yield calculate_values(dut,expected_Me,expected_Mo,expected_Si)
    



n = 1
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

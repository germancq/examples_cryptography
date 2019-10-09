# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    key_schedule_test.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/07 12:55:52 by germancq          #+#    #+#              #
#    Updated: 2019/10/08 13:26:01 by germancq         ###   ########.fr        #
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
import present

CLK_PERIOD = 20 # 50 MHz


#the keyword yield
#   Testbenches built using Cocotb use coroutines.
#   While the coroutine is executing the simulation is paused.
#   The coroutine uses the yield keyword
#   to pass control of execution back to
#   the simulator and simulation time can advance again.
#
#   yield return when the 'Trigger' is resolve
#
#   Coroutines may also yield a list of triggers
#   to indicate that execution should resume if any of them fires


def setup_function(dut, key):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst = 0
    dut.key = key
    dut.key_index = 0
    

@cocotb.coroutine
def rst_function_test(dut, key):
    dut.rst = 1
    
    yield n_cycles_clock(dut,10)

    
    if(dut.counter_output != 0):
        raise TestFailure("""Error rst,wrong counter_output value = {0}, expected value is {1}""".format(hex(int(dut.counter_output.value)),0))
        
    if(dut.key_register_output != key) : 
        raise TestFailure("""Error rst,wrong key_register_output value = {0}, expected value is {1}""".format(hex(int(dut.key_register_output.value)),hex(key)))
        
    if(dut.end_signal != 0):
        raise TestFailure("""Error rst,wrong end_signal value = {0}, expected value is {1}""".format(hex(int(dut.end_signal.value)),0))
             

    

    dut.rst = 0


@cocotb.coroutine
def generate_round_keys(dut) :
    dut.rst = 0
    i = 0
    while dut.end_signal.value == 0 :
        
        if(dut.current_state == 1) :
            print("**************")
            print(i)
            print(int(dut.counter_output))
            print(hex(int(dut.key_register_output.value)))
            i = i+1
            print("**************")
            
        yield n_cycles_clock(dut,1)
        

            
    if(dut.end_signal != 1):
        raise TestFailure("""Error generate_round_keys,wrong end_signal value = {0}, expected value is {1}""".format(hex(int(dut.end_signal.value)),1))
             

@cocotb.coroutine
def check_round_keys(dut,present_SW) :

    yield n_cycles_clock(dut,1)
    
    for i in range(0,32) :
        dut.key_index = i+1
        expected_key = present_SW.round_keys[i]
        print(i)
        #
        print(int(dut.key_index.value))
        print(hex(int(dut.roundkey.value)))
        print(hex(expected_key))
        
        if(dut.roundkey != expected_key) :
            raise TestFailure("""Error check_round_keys,wrong key value = {0}, expected value is {1} at iteration {2}""".format(hex(int(dut.roundkey.value)),hex(expected_key),int(dut.key_index.value)))
        
        yield n_cycles_clock(dut,1)
       


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, key = 0):
    key = random.randint(0,(2**32)-1)
    #print(hex(key))
    #key = 0
    present_SW = present.Present(key)
    setup_function(dut,key)
    
    yield rst_function_test(dut, key)
    yield generate_round_keys(dut)
    yield check_round_keys(dut,present_SW)



n = 10
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

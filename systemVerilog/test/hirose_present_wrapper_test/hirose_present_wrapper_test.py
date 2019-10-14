# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hirose_present_wrapper_test.py                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/14 11:47:12 by germancq          #+#    #+#              #
#    Updated: 2019/10/14 15:33:02 by germancq         ###   ########.fr        #
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
import hirose_present

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


def setup_function(dut, plaintext, c):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst = 0
    dut.c = c
    dut.plaintext = plaintext

    
   
    

@cocotb.coroutine
def rst_function_test(dut):
    dut.rst = 1
    
    yield n_cycles_clock(dut,10)
    
    if(dut.hash_output != 0):
        raise TestFailure("""Error rst hash_output,wrong hash value = {0}, expected value is {1}""".format(hex(int(dut.hash_output.value)),0))

    if(dut.end_signal != 0):
        raise TestFailure("""Error rst end_signal,wrong end_signal value = {0}, expected value is {1}""".format(hex(int(dut.end_signal.value)),0))
    
    dut.rst = 0




@cocotb.coroutine
def hash_test(dut,expected_value) :
    
    i = 0
    while dut.end_signal.value == 0 :
        #print(int(dut.current_state.value))
        
        if(dut.end_hash.value ):
            
            print('++++++++++++++++++++++++')
            print(i)
            print(int(dut.counter_output))
            #print(hex(int(dut.plaintext)))
            #print(hex(int(dut.c.value)))
            print(hex(int(dut.h_left_o.value)))
            print(hex(int(dut.h_right_o.value)))
            print(hex(int(dut.hash_o.value)))

            print("~~~~~~~~~~~~~~~~~~")
            print(hex(int(dut.hash_impl.key_i.value)))
            print(hex(int(dut.hash_impl.input_left.value)))
            print(hex(int(dut.hash_impl.input_right.value)))
            print(hex(int(dut.hash_impl.output_left.value)))
            print(hex(int(dut.hash_impl.output_right.value)))
            
            
            
            print('++++++++++++++++++++++++++')
            
        i = i+1
        
        yield n_cycles_clock(dut,1)
        
        
    
    #yield n_cycles_clock(dut,1)
    print(hex(int(dut.hash_output.value)))
    if(dut.hash_output != expected_value) :
            raise TestFailure("""Error hash,wrong value = {0}, expected value is {1}""".format(hex(int(dut.hash_output.value)),hex(expected_value)))
    
    
       


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, text = 0):
    
    text = random.randint(0,(2**32)-1)

    
    #text = 0xAAAAAAAAAAAAAAAA
    c    = 0x1111111111111111
    len_value = 64
    hash_SW = hirose_present.HirosePresent(c,len_value)
    expected_value = hash_SW.generate_hash(text)

    setup_function(dut,text,c)
    
    yield rst_function_test(dut)
    yield hash_test(dut,expected_value)



n = 10
factory = TestFactory(run_test)

factory.add_option("text", np.random.randint(low=0,high=(2**32)-1,size=n))
#factory.add_option("c", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

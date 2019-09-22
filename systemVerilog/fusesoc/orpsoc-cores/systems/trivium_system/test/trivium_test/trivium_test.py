# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    trivium_test.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/09/22 22:31:07 by germancq          #+#    #+#              #
#    Updated: 2019/09/23 01:57:16 by germancq         ###   ########.fr        #
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
sys.path.append('/home/germancq/criptografia/examples_cryptography/python')
import trivium

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


def setup_function(dut, key, iv):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst = 0
    dut.en = 0
    dut.key = key
    dut.iv = iv
    

@cocotb.coroutine
def rst_function_test(dut, key, iv):
    dut.rst = 1
    yield n_cycles_clock(dut,10)

    if(dut.dout_A != key):
        raise TestFailure("Error rst,wrong dout_A value = %s"
                          % hex(int(dut.dout_A.value)))
        
    if(dut.dout_B != iv):
        raise TestFailure("Error rst,wrong dout_B value = %s"
                          % hex(int(dut.dout_B.value)))
        
    if(dut.dout_C != 0x7000000000000000000000000000):
        raise TestFailure("Error rst,wrong dout_C value = %s"
                          % hex(int(dut.dout_C.value)))
        
    if(dut.counter_out != 0x0):
        raise TestFailure("Error rst,wrong counter value = %s"
                          % hex(int(dut.counter_out.value)))            

    

    dut.rst = 0


@cocotb.coroutine
def warm_up_phase_test(dut):
    dut.rst = 0
    dut.en = 0
    
    
    for i in range(0,1152) :
       
       if(dut.counter_out != i):
            raise TestFailure("Error warm_up,wrong counter value = %s"
                            % hex(int(dut.counter_out.value)))
       if(dut.warm_up_complete != 0):
            raise TestFailure("Error warm_up,wrong warm_up_complete value = %s"
                            % hex(int(dut.warm_up_complete.value)))
        
        
       yield n_cycles_clock(dut,1)
       dout_a = int(dut.dout_A.value)
    
    
          
    if(dut.warm_up_complete != 1):
            raise TestFailure("Error warm_up,wrong warm_up_complete value = %s"
                            % hex(int(dut.warm_up_complete.value)))
            
    
    
    
    yield n_cycles_clock(dut,10)
    
    if(dut.dout_A != dout_a):
        raise TestFailure("Error warm_up,wrong dout_A value = %s"
                          % hex(int(dut.dout_A.value)))


@cocotb.coroutine
def key_stream_generation_test(dut,expected_value) : 
    dut.rst = 0
    dut.en = 1
    

        

@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, key = 0 , iv = 0):
    #expected_value = trivium.trivium_impl(key,iv,128)
    #print(expected_value)
    setup_function(dut, key, iv)
    yield rst_function_test(dut, key, iv)
    yield warm_up_phase_test(dut)
    #yield key_stream_generation_test(dut, expected_value, n)
    



n = 10
factory = TestFactory(run_test)
factory.add_option("key", np.random.randint(low=0,high=(2**16)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.add_option("iv", np.random.randint(low=0,high=(2**16)-1,size=n))
factory.generate_tests()
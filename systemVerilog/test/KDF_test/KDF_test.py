# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    KDF_test.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/17 16:38:46 by germancq          #+#    #+#              #
#    Updated: 2019/10/17 17:04:18 by germancq         ###   ########.fr        #
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
import keyDerivationFunction

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


def setup_function(dut, salt, count, user_password):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst = 0
    dut.salt = salt
    dut.count = count
    dut.user_password = user_password

    
   
    

@cocotb.coroutine
def rst_function_test(dut,first_value):
    dut.rst = 1
    
    
    yield n_cycles_clock(dut,10)
    
    if(dut.key_derivated != 0):
        raise TestFailure("""Error rst hash_output,wrong hash value = {0}, expected value is {1}""".format(hex(int(dut.key_derivated.value)),0))

    if(dut.end_signal != 0):
        raise TestFailure("""Error rst end_signal,wrong end_signal value = {0}, expected value is {1}""".format(hex(int(dut.end_signal.value)),0))

    if(dut.counter_output != 0):
        raise TestFailure("""Error rst counter_output,wrong counter_output value = {0}, expected value is {1}""".format(hex(int(dut.counter_output.value)),0))

    if(dut.hash_input != first_value):
        raise TestFailure("""Error rst hash_input,wrong hash_input value = {0}, expected value is {1}""".format(hex(int(dut.hash_input.value)),hex(first_value)))
    
    dut.rst = 0




@cocotb.coroutine
def kdf_test(dut,expected_value) :
    
    i = 0
    while dut.end_signal.value == 0 :
        #print(int(dut.current_state.value))
        
        if(dut.hash_end_signal.value ):
            
            print('++++++++++++++++++++++++')
            #print(i)
            print(int(dut.counter_output))
            print(hex(int(dut.hash_input.value)))
            print(hex(int(dut.hash_output.value)))
            print(hex(int(dut.register_output.value)))
            
            
            print('++++++++++++++++++++++++++')
            
        #i = i+1
        
        yield n_cycles_clock(dut,1)
        
        
    
    print(hex(expected_value))
    if(dut.key_derivated != expected_value) :
            raise TestFailure("""Error kdf,wrong value = {0}, expected value is {1}""".format(hex(int(dut.key_derivated.value)),hex(expected_value)))
    
    
       


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, text = 0):
    
    #text = random.randint(0,(2**32)-1)

    salt = 0x123456789ABCDEF0
    count = 50
    user_password = 0xAAAA

    kdf_impl = keyDerivationFunction.KDF(count,salt,user_password)   
    expected_value = kdf_impl.generate_derivate_key()
    
    first_value = (user_password << 96) + (salt << 32) + count
    

    setup_function(dut,salt,count,user_password)
    
    yield rst_function_test(dut,first_value)
    yield kdf_test(dut,expected_value)



n = 1
factory = TestFactory(run_test)

factory.add_option("text", np.random.randint(low=0,high=(2**32)-1,size=n))
#factory.add_option("c", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

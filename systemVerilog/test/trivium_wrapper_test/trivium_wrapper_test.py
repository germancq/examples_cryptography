# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    trivium_wrapper_test.py                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/09 12:17:36 by germancq          #+#    #+#              #
#    Updated: 2019/10/09 13:06:10 by germancq         ###   ########.fr        #
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
import trivium

CLK_PERIOD = 20 # 50 MHz


def bitArray_to_int_value (bitarray):
    value = 0
    for i in range (0,len(bitarray)):
        value = value + (2**i)*bitarray[i]

    return value    


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
    dut.key = key
    dut.iv = iv
    

@cocotb.coroutine
def rst_function_test(dut, key, iv, trivium_SW):
    dut.rst = 1
    key_1 = hex(key).rstrip("L")#HEX
    IV_1 = hex(iv).rstrip("L")#HEX
    trivium_SW.rst()
    trivium_SW.Initialization(key_1,IV_1)
    yield n_cycles_clock(dut,10)


    if(dut.trivium_impl.dout_A != bitArray_to_int_value(trivium_SW.A)):
        raise TestFailure("""Error rst,wrong dout_A value = {0}, expected value is {1}""".format(hex(int(dut.trivium_impl.dout_A.value)),hex(bitArray_to_int_value(trivium_SW.A))))
        
    if(dut.trivium_impl.dout_B != bitArray_to_int_value(trivium_SW.B)):
        raise TestFailure("""Error rst,wrong dout_A value = {0}, expected value is {1}""".format(hex(int(dut.trivium_impl.dout_A.value)),hex(bitArray_to_int_value(trivium_SW.B))))
        
    if(dut.trivium_impl.dout_C != bitArray_to_int_value(trivium_SW.C)):
        raise TestFailure("""Error rst,wrong dout_A value = {0}, expected value is {1}""".format(hex(int(dut.trivium_impl.dout_A.value)),hex(bitArray_to_int_value(trivium_SW.C))))
        
    if(dut.counter_out != 0x0):
        raise TestFailure("Error rst,wrong counter value = %s"
                          % hex(int(dut.counter_out.value)))            

    

    dut.rst = 0


@cocotb.coroutine
def warm_up_phase_test(dut, trivium_SW):
    dut.rst = 0
    
    #yield n_cycles_clock(dut,1)
    
    for i in range(0,1152) :
       
       if(dut.trivium_impl.counter_out != i):
            raise TestFailure("""Error warm_up,wrong counter value = {0} at iteration {1}""".format(hex(int(dut.trivium_impl.counter_out.value)),i))
                           
       if(dut.trivium_impl.warm_up_complete != 0):
            raise TestFailure("""Error warm_up,wrong warm_up_complete value = {0} at iteration {1}""".format(hex(int(dut.trivium_impl.warm_up_complete.value)),i))
        
       if(dut.trivium_impl.dout_A != bitArray_to_int_value(trivium_SW.A)):
        raise TestFailure("""Error warm_up,wrong dout_A value = {0}, expected value is {1} at iteration {2}""".format(hex(int(dut.dout_A.value)),hex(bitArray_to_int_value(trivium_SW.A)),i))
        
       if(dut.trivium_impl.dout_B != bitArray_to_int_value(trivium_SW.B)):
            raise TestFailure("""Error warm_up,wrong dout_B value = {0}, expected value is {1} at iteration {2}""".format(hex(int(dut.trivium_impl.dout_B.value)),hex(bitArray_to_int_value(trivium_SW.B)),i))
            
       if(dut.trivium_impl.dout_C != bitArray_to_int_value(trivium_SW.C)):
            raise TestFailure("""Error warm_up,wrong dout_C value = {0}, expected value is {1} at iteration {2}""".format(hex(int(dut.trivium_impl.dout_C.value)),hex(bitArray_to_int_value(trivium_SW.C)),i)) 

       
       
       
       yield n_cycles_clock(dut,1)

       trivium_SW.step()

       
     
    if(dut.counter_out != 0x0):
        raise TestFailure("Error rst,wrong counter value = %s"
                          % hex(int(dut.counter_out.value)))      
          
    if(dut.warm_up_complete != 1):
            raise TestFailure("Error final warm_up,wrong warm_up_complete value = %s"
                            % hex(int(dut.warm_up_complete.value)))
            
    
    
    
    


@cocotb.coroutine
def key_stream_generation_test(dut,trivium_SW,expected_value) : 
    dut.rst = 0
    
    expected_output = trivium_SW.gen_keystream(64)
    print(expected_output)
    i = 0
    while (dut.end_block == 0) :
        if(dut.key_stream != expected_output[i]):
            raise TestFailure("""Error warm_up,wrong key_stream value = {0}, expected value is {1}  at iteration {2}""".format(hex(int(dut.key_stream.value)),expected_output[i],i))
        yield n_cycles_clock(dut,1)
        i = i+1

    #expected_value.byteswap()
        
    if(dut.block_o != expected_value):
            raise TestFailure("""Error output value = {0}, expected value is {1}  """.format(hex(int(dut.block_o.value)),hex(expected_value)))


        
                          
    

        

@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, key = 0 , iv = 0):
    
    expected_value = trivium.trivium_impl(key,iv,64)
    expected_value = int(expected_value,2)
    trivium_SW = trivium.Trivium()

    setup_function(dut, key, iv)
    yield rst_function_test(dut, key, iv, trivium_SW)
    yield warm_up_phase_test(dut, trivium_SW)
    yield key_stream_generation_test(dut, trivium_SW,expected_value)
    



n = 2
factory = TestFactory(run_test)
factory.add_option("key", np.random.randint(low=0,high=(2**8)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.add_option("iv", np.random.randint(low=0,high=(2**8)-1,size=n))
factory.generate_tests()
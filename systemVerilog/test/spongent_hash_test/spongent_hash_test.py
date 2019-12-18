# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spongent_hash_test.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/12/18 17:52:50 by germancq          #+#    #+#              #
#    Updated: 2019/12/18 18:42:35 by germancq         ###   ########.fr        #
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
import LFSR
import spongent

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


def setup_function(dut,msg):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.msg = msg
    dut.rst = 0


@cocotb.coroutine
def rst_function_test(dut,expected_padded_msg):
    dut.rst = 1
    yield n_cycles_clock(dut,20)
    
    if(dut.permutation_impl.rst != 1):
        raise TestFailure("""Error in reset, wrong value = {0}, expected value = {1}""".format(hex(int(dut.permutation_impl.rst.value)),hex(1))) 

    

    if(dut.padded_msg != expected_padded_msg):
        raise TestFailure("""Error in padded_msg, wrong value = {0}, expected value = {1}""".format(hex(int(dut.padded_msg.value)),hex(expected_padded_msg))) 


@cocotb.coroutine
def absorbing_test(dut,expected_state,spongent_impl):
    dut.rst = 0

    if(dut.absorbing_phase_impl.permutation_initial_state != spongent_impl.absorbing_before_p_states[0]):
        raise TestFailure("""Error in absorbing initial state, wrong value = {0}, expected value = {1}""".format(hex(int(dut.absorbing_phase_impl.permutation_initial_state.value)),hex(spongent_impl.absorbing_before_p_states[0]))) 
    
    i = 0
    print(int(dut.absorbing_phase_impl.DATA_WIDTH_PADDED))

    while (dut.end_absorbing == 0):
        if(dut.absorbing_phase_impl.end_permutation == 1):
            
            

            yield n_cycles_clock(dut,1)
            
            if(dut.absorbing_phase_impl.absorbing_state != spongent_impl.absorbing_after_p_states[i]):
                 raise TestFailure("""Error in absorbing after permutation state, wrong value = {0}, expected value = {1} at {2}""".format(hex(int(dut.absorbing_phase_impl.absorbing_state.value)),hex(spongent_impl.absorbing_after_p_states[i]),i)) 

            i = i+1    
            
        yield n_cycles_clock(dut,1)

    if(dut.absorbing_state != expected_state):
        raise TestFailure("""Error in absorbing state, wrong value = {0}, expected value = {1}""".format(hex(int(dut.absorbing_state.value)),hex(expected_state))) 


@cocotb.coroutine
def squeezing_test(dut,spongent_impl,expected_result):


    if(dut.squeezing_phase_impl.result != spongent_impl.squeezing_results[0]):
        raise TestFailure("""Error in squeezing initial state, wrong value = {0}, expected value = {1}""".format(hex(int(dut.squeezing_phase_impl.result.value)),hex(spongent_impl.squeezing_results[0]))) 

    i = 0
    
    while(dut.squeezing_phase_impl.end_squeezing == 0):
        if(dut.squeezing_phase_impl.end_permutation == 1):

            print(hex(int(dut.squeezing_phase_impl.counter_o.value)))
            yield n_cycles_clock(dut,1)
            print(hex(int(dut.squeezing_phase_impl.state.value)))
            
            
            if(dut.squeezing_phase_impl.state != spongent_impl.squeezing_states[i]):
                raise TestFailure("""Error in squeezing state, wrong value = {0}, expected value = {1} at {2}""".format(hex(int(dut.squeezing_phase_impl.state.value)),hex(spongent_impl.squeezing_states[i]),i)) 

            if(dut.squeezing_phase_impl.result != spongent_impl.squeezing_results[i]):
                raise TestFailure("""Error in squeezing result, wrong value = {0}, expected value = {1} at {2}""".format(hex(int(dut.squeezing_phase_impl.result.value)),hex(spongent_impl.squeezing_results[i]),i)) 
            
            i = i+1
        
        yield n_cycles_clock(dut,1)    


    if(dut.squeezing_phase_impl.result != expected_result):
        raise TestFailure("""Error in Hash, wrong value = {0}, expected value = {1}""".format(hex(int(dut.squeezing_phase_impl.result.value)),hex(expected_result)))

        
    

@cocotb.coroutine
def n_cycles_clock(dut,n):
    for _ in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk) 

        
@cocotb.coroutine
def run_test(dut,msg=0):
    msg = random.randint(0,(2**24)-1)
    print(hex(msg))
    spongent_impl = spongent.Spongent(256,256,16,140)
    spongent_impl.initialization_phase(msg,64)
    expected_padded_msg = spongent_impl.padded_msg
    expected_state = spongent_impl.absorbing_phase()
    expected_result = spongent_impl.squeezing_phase(expected_state)
    setup_function(dut,msg) 
    yield rst_function_test(dut,expected_padded_msg)    
    yield absorbing_test(dut,expected_state,spongent_impl)  
    yield squeezing_test(dut,spongent_impl,expected_result)

             
n = 10
factory = TestFactory(run_test)

factory.add_option("msg", np.random.randint(low=1,high=(2**8)-1,size=n))
factory.generate_tests() 
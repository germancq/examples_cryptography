# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    LFSR_test.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/12/16 13:53:55 by germancq          #+#    #+#              #
#    Updated: 2019/12/16 14:29:17 by germancq         ###   ########.fr        #
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

def setup_function(dut,initial_state,feedback_coeff):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start()) 
    dut.rst = 0
    dut.shift = 0
    dut.feedback_coeff = feedback_coeff
    dut.initial_state = initial_state


@cocotb.coroutine
def rst_function_test(dut,initial_state):
    dut.rst = 1

    yield n_cycles_clock(dut,20)
    
    if(dut.state != initial_state):
        raise TestFailure("""Error initial state in reset, wrong value = {0}, expected value = {1}""".format(hex(int(dut.state.value)),hex(initial_state)))    


@cocotb.coroutine
def shift_function_test(dut,LFSR_impl):
    dut.rst = 0
    dut.shift = 1
    
    n = 50

    while(n>0):
        
        if(dut.state != LFSR_impl.state):
            raise TestFailure("""Error state in shift, wrong value = {0}, expected value = {1} at iteration = {2}""".format(hex(int(dut.state.value)),hex(LFSR_impl.state),50-n))    

        
        yield n_cycles_clock(dut,1)
        LFSR_impl.step()

        n = n-1


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)   




@cocotb.coroutine
def run_test(dut, initial_state = 0, feedback_coeff = 0):
    setup_function(dut,initial_state,feedback_coeff)
    LFSR_impl = LFSR.LFSR(6,initial_state,feedback_coeff)
    yield rst_function_test(dut,initial_state)
    LFSR_impl.set_state(initial_state) 
    yield shift_function_test(dut,LFSR_impl)
    
    



n = 10
factory = TestFactory(run_test)

factory.add_option("initial_state", np.random.randint(low=0,high=(2**6)-1,size=n))
factory.add_option("feedback_coeff", np.random.randint(low=(2**5),high=(2**6)-1,size=n))
factory.generate_tests()  
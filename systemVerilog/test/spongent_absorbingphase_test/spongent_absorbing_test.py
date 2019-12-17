# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spongent_absorbing_test.py                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/12/17 19:19:14 by germancq          #+#    #+#              #
#    Updated: 2019/12/17 19:19:51 by germancq         ###   ########.fr        #
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
def rst_function_test(dut,msg):
    dut.rst = 1
    yield n_cycles_clock(dut,20)
    
    if(dut.permutation_impl.rst != 1):
        raise TestFailure("""Error in reset, wrong value = {0}, expected value = {1}""".format(hex(int(dut.permutation_impl.rst.value)),hex(1))) 

    print(hex(int(dut.msg)))
    print(hex(int(dut.padded_msg)))


@cocotb.coroutine
def permutation_test(dut,spongent_impl,state):
    dut.rst = 0

    yield n_cycles_clock(dut,1)

    


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for _ in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk) 

        
@cocotb.coroutine
def run_test(dut,msg=0):
    msg = random.randint(0,(2**8)-1)
    print(hex(msg))
    spongent_impl = spongent.Spongent(88,80,8,45)
    setup_function(dut,msg) 
    yield rst_function_test(dut,msg)    
    yield permutation_test(dut,spongent_impl,msg)  

             
n = 10
factory = TestFactory(run_test)

factory.add_option("msg", np.random.randint(low=1,high=(2**8)-1,size=n))
factory.generate_tests() 
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    present_test.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/01 13:00:00 by germancq          #+#    #+#              #
#    Updated: 2019/10/01 15:23:51 by germancq         ###   ########.fr        #
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


def setup_function(dut, key, plaintext):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst = 0
    dut.key = key
    dut.block_input = plaintext
    dut.enc_dec = 0
    

@cocotb.coroutine
def rst_function_test(dut):
    dut.rst = 1
    
    yield n_cycles_clock(dut,10)

    dut.rst = 0


@cocotb.coroutine
def generate_round_keys(dut) :
    dut.rst = 0
    while dut.end_key_generation.value == 0 :
        yield n_cycles_clock(dut,1)
        

            
    if(dut.end_key_generation != 1):
        raise TestFailure("""Error generate_round_keys,wrong end_signal value = {0}, expected value is {1}""".format(hex(int(dut.end_key_generation.value)),1))
             

@cocotb.coroutine
def enc_dec_test(dut,expected_enc_value,expected_dec_value) :
    
    yield n_cycles_clock(dut,1)
    print(hex(int(dut.block_output.value)))
    if(dut.block_output != expected_enc_value) :
            raise TestFailure("""Error enc_test,wrong value = {0}, expected value is {1}""".format(hex(int(dut.block_output.value)),hex(expected_enc_value)))

    dut.enc_dec = 1    

    yield n_cycles_clock(dut,1)
    print(hex(int(dut.block_output.value)))
    if(dut.block_output != expected_dec_value) :
            raise TestFailure("""Error dec_test,wrong value = {0}, expected value is {1}""".format(hex(int(dut.block_output.value)),hex(expected_dec_value)))
    
       


@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, key = 0):
    key = random.randint(0,(2**32)-1)
    text = random.randint(0,(2**32)-1)

    print(hex(key))
    print(hex(text))
    present_SW = present.Present(key)
    expected_enc_value = present_SW.encrypt(text)
    expected_dec_value = present_SW.decrypt(text)
    setup_function(dut,key,text)
    
    yield rst_function_test(dut)
    yield generate_round_keys(dut)
    yield enc_dec_test(dut,expected_enc_value,expected_dec_value)



n = 10
factory = TestFactory(run_test)

factory.add_option("key", np.random.randint(low=0,high=(2**32)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()

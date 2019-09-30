# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    shiftregister_test.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/09/22 15:55:50 by germancq          #+#    #+#              #
#    Updated: 2019/09/22 19:35:11 by germancq         ###   ########.fr        #
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

import sys

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


def setup_function(dut, din):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.din = din
    dut.load = 0
    dut.shift_left = 0
    dut.shift_right = 0
    dut.input_bit = 0
    

@cocotb.coroutine
def load_function_test(dut,din):
    dut.load = 1
    yield n_cycles_clock(dut,1)

    if(dut.dout.value.integer != din):
        raise TestFailure("Error load,wrong data value = %s, expected value is = %s"
                          % hex(int(dut.data.value))
                          % hex(din))

    

    dut.load = 0
    
@cocotb.coroutine
def shift_left_test(dut,din,n_cycles) :
     dut.shift_left = 1
     
     for i in range(n_cycles):
         random_bit = random.getrandbits(1)
         dut.input_bit = random_bit
         expected_output_bit = (din & 0x80)>>7
         
         din = ((din << 1) & 0xFF)
         din = din + random_bit
         
         
         yield n_cycles_clock(dut,1)
         
         if(dut.dout.value.integer != din):
            raise TestFailure("Error shift left,wrong data value = '{0}', expected value is = '{1}'".format(hex(int(dut.dout.value)), hex(din)))
            
         if(dut.output_bit.value.integer != expected_output_bit):
            raise TestFailure("Error shift left,wrong output bit value = '{0}', expected value is = '{1}'".format(hex(int(dut.output_bit.value)),hex(expected_output_bit)))

     
     dut.shift_left = 0   


@cocotb.coroutine
def shift_right_test(dut,din,n_cycles) :
     dut.shift_right = 1
     
     for i in range(n_cycles):
         random_bit = random.getrandbits(1)
         dut.input_bit = random_bit
         expected_output_bit = (din & 0x1)
         
         din = ((din >> 1) & 0xFF)
         din = din | (random_bit<<7)
         
         
         yield n_cycles_clock(dut,1)
         
         if(dut.dout.value.integer != din):
            raise TestFailure("Error shift left,wrong data value = '{0}', expected value is = '{1}'".format(hex(int(dut.dout.value)), hex(din)))
            
         if(dut.output_bit.value.integer != expected_output_bit):
            raise TestFailure("Error shift left,wrong output bit value = '{0}', expected value is = '{1}'".format(hex(int(dut.output_bit.value)),hex(expected_output_bit)))

     
     dut.shift_right = 0   




@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, din = 2):
    setup_function(dut, din)
    yield load_function_test(dut,din)
    yield shift_left_test(dut,din,20)
    yield load_function_test(dut,din)
    yield shift_right_test(dut,din,20)



n = 10
factory = TestFactory(run_test)
factory.add_option("din", np.random.randint(low=0,high=(2**8)-1,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()
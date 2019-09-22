 #
 # @Author: German Cano Quiveu, germancq@gmail.com 
 # @Date: 2019-09-21 22:23:48 
 # @Last Modified by:   German Cano Quiveu, germancq@gmail.com 
 # @Last Modified time: 2019-09-21 22:23:48 
 #

import cocotb
import numpy as np
import time
import linecache
from cocotb.triggers import Timer,RisingEdge, FallingEdge
from cocotb.regression import TestFactory
from cocotb.result import TestFailure, ReturnValue
from cocotb.clock import Clock

import sys

CLK_PERIOD = 20 # 50 MHz

LOOKUP_FILE = "../../rtl/systemVerilog/lookuptable_contents.mem"

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
    dut.addr = din
    

@cocotb.coroutine
def rst_function_test(dut):
    dut.rst = 1
    yield n_cycles_clock(dut,10)

    if(dut.data != 0xFFFFFFFF):
        raise TestFailure("Error rst,wrong data value = %s"
                          % hex(int(dut.data.value)))

    

    dut.rst = 0


@cocotb.coroutine
def check_lookuptable(dut, din):
    
    with open(LOOKUP_FILE) as fp:
        lines = fp.readlines()
    
    
        yield n_cycles_clock(dut,1)
        selected_line = lines[din].replace(" ","")
        print(selected_line)
    
        if(dut.data.value.integer != int(selected_line,16)):
            raise TestFailure("Error data,wrong value = %s"
                            % hex(int(dut.data.value)))
                            
    





@cocotb.coroutine
def n_cycles_clock(dut,n):
    for i in range(0,n):
        yield RisingEdge(dut.clk)
        yield FallingEdge(dut.clk)



@cocotb.coroutine
def run_test(dut, din = 2):
    setup_function(dut, din)
    yield rst_function_test(dut)
    yield check_lookuptable(dut,din)



n = 10
factory = TestFactory(run_test)
factory.add_option("din", np.random.randint(low=0,high=32,size=n)) #array de 10 int aleatorios entre 0 y 31
factory.generate_tests()
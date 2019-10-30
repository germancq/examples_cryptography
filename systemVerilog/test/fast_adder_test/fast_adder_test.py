# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    fast_adder_test.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/30 12:39:43 by germancq          #+#    #+#              #
#    Updated: 2019/10/30 12:39:51 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cocotb
from cocotb.regression import TestFactory
from cocotb.result import TestFailure, ReturnValue
from cocotb.triggers import Timer
import numpy as np
import random


def setup_function(dut, a, b):
    dut.a = a
    dut.b = b

@cocotb.coroutine
def calculate_result(dut,expected_s,expected_c):
    yield Timer(100)

    if(dut.s != expected_s) :
            raise TestFailure("""Error sum value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.s.value)),hex(expected_s)))

    if(dut.c != expected_c) :
            raise TestFailure("""Error carry value,wrong value = {0}, expected value is {1}""".format(hex(int(dut.c.value)),hex(expected_c)))    



@cocotb.coroutine
def run_test(dut, a = 0, b = 0):

    print(hex(a))
    print(hex(b))
    expected_s = (a + b) & ((2**32)-1)
    expected_c = ((a+b)>>32) & 0x01

    setup_function(dut,a,b)
    yield calculate_result(dut,expected_s,expected_c)



n = 10
factory = TestFactory(run_test)

factory.add_option("a", np.random.randint(low=0,high=(2**32)-1,size=n))  
factory.add_option("b", np.random.randint(low=0,high=(2**32)-1,size=n)) 
factory.generate_tests()

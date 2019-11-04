# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/04 17:20:31 by germancq          #+#    #+#              #
#    Updated: 2019/11/04 17:20:54 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/twofish.sv \
				  ../../rtl/galois_arithmetic.sv \
				  ../../rtl/adder.sv

TOPLEVEL= f_function
MODULE=f_function_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
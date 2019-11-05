# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/05 12:19:02 by germancq          #+#    #+#              #
#    Updated: 2019/11/05 12:19:47 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/twofish.sv \
				  ../../rtl/galois_arithmetic.sv \
				  ../../rtl/adder.sv \
				  ../../rtl/register.sv \
				  ../../rtl/counter.sv

TOPLEVEL= twofish
MODULE=twofish_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
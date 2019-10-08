# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/01 12:59:24 by germancq          #+#    #+#              #
#    Updated: 2019/10/07 12:44:07 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/present_x32.sv \
				  ../../rtl/present_misc.sv \
				  ../../rtl/register.sv \
				  ../../rtl/memory_module.sv \
				  ../../rtl/counter.sv	

TOPLEVEL=present_x32
MODULE=present_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
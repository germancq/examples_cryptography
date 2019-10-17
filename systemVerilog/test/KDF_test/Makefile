# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/17 16:30:38 by germancq          #+#    #+#              #
#    Updated: 2019/10/17 16:45:15 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/KDF.sv \
				  ../../rtl/hirose_present_wrapper.sv \
				  ../../rtl/hirose_present.sv \
				  ../../rtl/present.sv \
				  ../../rtl/present_misc.sv \
				  ../../rtl/register.sv \
				  ../../rtl/memory_module.sv \
				  ../../rtl/counter.sv	

TOPLEVEL=KDF
MODULE=KDF_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
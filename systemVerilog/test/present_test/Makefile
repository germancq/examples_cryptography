# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/07 13:59:49 by germancq          #+#    #+#              #
#    Updated: 2019/10/07 14:00:11 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/present.sv \
				  ../../rtl/present_misc.sv \
				  ../../rtl/register.sv \
				  ../../rtl/memory_module.sv \
				  ../../rtl/counter.sv	

TOPLEVEL=present
MODULE=present_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
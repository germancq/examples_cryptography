# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/09 12:16:44 by germancq          #+#    #+#              #
#    Updated: 2019/10/09 12:17:14 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/trivium_wrapper.sv \
				  ../../rtl/trivium.sv \
				  ../../rtl/shift_register.sv \
				  ../../rtl/counter.sv	

TOPLEVEL=trivium_wrapper
MODULE=trivium_wrapper_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/09/30 16:15:22 by germancq          #+#    #+#              #
#    Updated: 2019/09/30 17:14:33 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../rtl/present.sv \
				  ../../rtl/register.sv \
				  ../../rtl/memory_module.sv \
				  ../../rtl/counter.sv	

TOPLEVEL=key_schedule
MODULE=key_schedule_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml
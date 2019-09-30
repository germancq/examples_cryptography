# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/09/22 22:31:02 by germancq          #+#    #+#              #
#    Updated: 2019/09/22 22:34:50 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VERILOG_SOURCES = ../../trivium.sv \
				  ../../shift_register.sv \
				  ../../counter.sv	

TOPLEVEL=trivium
MODULE=trivium_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim


clean_results : 
	rm *.pyc
	rm *.xml

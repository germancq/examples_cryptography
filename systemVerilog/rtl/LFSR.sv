/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-12-16 13:52:27
 * @ Modified by: Your name
 * @ Modified time: 2019-12-17 13:51:03
 * @ Description:
 */

module LFSR #(
    parameter DATA_WIDTH = 6
)
(
    input clk,
    input rst,
    input shift,
    input [DATA_WIDTH:0] feedback_coeff,
    input [DATA_WIDTH-1:0] initial_state,
    output [DATA_WIDTH-1:0] state
);

    logic [DATA_WIDTH-1:0] state_reg;
    logic bit_xored;
    assign state = state_reg;

    assign bit_xored = ^(state_reg & feedback_coeff[DATA_WIDTH:1]);

    always_ff @(posedge clk) begin
        if(rst == 1) begin
            state_reg <= initial_state;
        end
        else if(shift == 1) begin
            state_reg <= {state_reg[DATA_WIDTH-2:0],bit_xored};
        end
    end

endmodule : LFSR
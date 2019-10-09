/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 15:33:22
 * @ Modified by: Your name
 * @ Modified time: 2019-10-08 13:24:37
 * @ Description:
 */

module memory_module(
    input clk,
    input r_w,
    input [ADDR-1:0] addr,
    input [DATA_WIDTH-1:0] din,
    output logic [DATA_WIDTH-1:0] dout
);

parameter ADDR = 5;
parameter DATA_WIDTH = 64;

logic [DATA_WIDTH-1:0]  memory_ [2**ADDR-1:0];


always_ff @(posedge clk) begin
    if (r_w == 1) begin
        memory_[addr] <= din;
    end
    else begin
        dout <= memory_[addr];
    end

end


endmodule : memory_module
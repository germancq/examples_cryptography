/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 15:33:22
 * @ Modified by: Your name
 * @ Modified time: 2019-10-02 12:48:06
 * @ Description:
 */

module memory_module(
    input r_w,
    input [ADDR-1:0] addr,
    input [DATA_WIDTH-1:0] din,
    output [DATA_WIDTH-1:0] dout
);

parameter ADDR = 4;
parameter DATA_WIDTH = 32;

logic [2**ADDR-1:0] [DATA_WIDTH-1:0] memory_ ;

assign dout = memory_[addr];

always_comb begin
    if (r_w == 1) begin
        memory_[addr] = din;
    end
end


endmodule : memory_module
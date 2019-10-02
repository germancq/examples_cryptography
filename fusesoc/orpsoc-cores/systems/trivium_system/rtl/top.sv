/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-01 16:23:01
 * @ Modified by: Your name
 * @ Modified time: 2019-10-01 16:28:09
 * @ Description:
 */

module top(
    input clk,
    input rst,
    input en,
    output warm_up_complete,
    output key_stream
);

logic [79:0] key;
logic [79:0] iv;

assign key = 80'h0;
assign iv = 80'h0;

trivium trivium_impl(
    .clk(clk),
    .rst(rst),
    .en(en),
    .key(key),
    .iv(iv),
    .warm_up_complete(warm_up_complete),
    .key_stream(key_stream)
);

endmodule : top
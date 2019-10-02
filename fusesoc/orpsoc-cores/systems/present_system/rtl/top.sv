/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-01 16:32:35
 * @ Modified by: Your name
 * @ Modified time: 2019-10-01 16:36:42
 * @ Description:
 */

module top(
    input clk,
    input rst,
    input enc_dec,
    output end_key_generation
);

logic [79:0] key;
logic [63:0] text;
logic [63:0] block_o;

assign key = 80'h0;
assign text = 64'h0;

present present_impl(
    .clk(clk),
    .rst(rst),
    .enc_dec(enc_dec),
    .key(key),
    .block_input(text),
    .end_key_generation(end_key_generation),
    .block_output(block_o)
);

endmodule : top
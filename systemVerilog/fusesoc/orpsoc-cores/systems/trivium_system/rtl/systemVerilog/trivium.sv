/*
 * @Author: German Cano Quiveu, germancq@gmail.com 
 * @Date: 2019-09-22 22:30:56 
 * @Last Modified by: German Cano Quiveu, germancq@gmail.com
 * @Last Modified time: 2019-09-22 23:01:06
 */
module trivium(
    input clk,
    input rst,
    input en,
    input [79:0] key,
    input [79:0] iv,
    output warm_up_complete,
    output key_stream
);


    
    
    logic output_bit_A;
    logic input_bit_A;
    logic [92:0] dout_A;

    
    
    logic output_bit_B;
    logic input_bit_B;
    logic [83:0] dout_B;

    
    
    logic output_bit_C;
    logic input_bit_C;
    logic [110:0] dout_C;


    logic a_and;
    logic b_and;
    logic c_and;

    logic A_out;
    logic B_out;
    logic C_out;

    
    logic [$clog2(1152) - 1 : 0] counter_out;

    shift_register #(.DATA_WIDTH(93)) registerA(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_A),
        .din({13'b0,key}),
        .output_bit(output_bit_A),
        .dout(dout_A)
    );

    shift_register #(.DATA_WIDTH(84)) registerB(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_B),
        .din({4'b0,iv}),
        .output_bit(output_bit_B),
        .dout(dout_B)
    );

    shift_register #(.DATA_WIDTH(111)) registerC(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_C),
        .din({3'b111,108'b0}),
        .output_bit(output_bit_C),
        .dout(dout_C)
    );

    counter #(.DATA_WIDTH($clog2(1152))) counter_inst(
        .clk(clk),
        .rst(rst),
        .up(1'b1 & !warm_up_complete),
        .down(1'b0),
        .din(11'h0),
        .dout(counter_out)
    );


    assign warm_up_complete = counter_out == 1152 ? 1'b1 : 1'b0;  // counter_out[7] & counter_out[10];

    assign a_and = dout_A[90] & dout_A[91];
    assign b_and = dout_B[81] & dout_B[82];
    assign c_and = dout_C[108] & dout_C[109];

    
    assign A_out = output_bit_A ^ dout_A[65];
    assign B_out = output_bit_B ^ dout_B[68];
    assign C_out = output_bit_C ^ dout_C[65];


    assign input_bit_A = C_out ^ c_and ^ dout_A[68];
    assign input_bit_B = A_out ^ a_and ^ dout_B[77];
    assign input_bit_C = B_out ^ b_and ^ dout_C[86];


    assign key_stream = A_out ^ B_out ^ C_out;



endmodule : trivium
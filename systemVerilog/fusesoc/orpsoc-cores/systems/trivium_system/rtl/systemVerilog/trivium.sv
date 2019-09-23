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
    logic feedback_bit_output_A;
    logic feedback_bit_input_A;
    logic nonlinear_bit_A;
    
    
    logic output_bit_B;
    logic input_bit_B;
    logic [83:0] dout_B;
    logic feedback_bit_output_B;
    logic feedback_bit_input_B;
    logic nonlinear_bit_B;

    
    
    logic output_bit_C;
    logic input_bit_C;
    logic [110:0] dout_C;
    logic feedback_bit_output_C;
    logic feedback_bit_input_C;
    logic nonlinear_bit_C;

    logic A_out;
    logic B_out;
    logic C_out;

    
    logic [$clog2(1152) - 1 : 0] counter_out;

    shift_register #(.DATA_WIDTH(93),.FDBK_OUTPUT(66),.FDBK_INPUT(69),.NON_LINEAR_INDEX(92)) registerA(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_A),
        .din({13'b0,key}),
        .output_bit(output_bit_A),
        .feedback_bit_output(feedback_bit_output_A),
        .feedback_bit_input(feedback_bit_input_A),
        .nonlinear_bit(nonlinear_bit_A),
        .dout(dout_A)
    );

    shift_register #(.DATA_WIDTH(84),.FDBK_OUTPUT(69),.FDBK_INPUT(78),.NON_LINEAR_INDEX(83)) registerB(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_B),
        .din({4'b0,iv}),
        .output_bit(output_bit_B),
        .feedback_bit_output(feedback_bit_output_B),
        .feedback_bit_input(feedback_bit_input_B),
        .nonlinear_bit(nonlinear_bit_B),
        .dout(dout_B)
    );

    shift_register #(.DATA_WIDTH(111),.FDBK_OUTPUT(66),.FDBK_INPUT(87),.NON_LINEAR_INDEX(110)) registerC(
        .clk(clk),
        .shift_right(1'b0),
        .shift_left(!warm_up_complete | en),
        .load(rst),
        .input_bit(input_bit_C),
        .din({3'b111,108'b0}),
        .output_bit(output_bit_C),
        .feedback_bit_output(feedback_bit_output_C),
        .feedback_bit_input(feedback_bit_input_C),
        .nonlinear_bit(nonlinear_bit_C),
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


    
    assign A_out = output_bit_A ^ feedback_bit_output_A;
    assign B_out = output_bit_B ^ feedback_bit_output_B;
    assign C_out = output_bit_C ^ feedback_bit_output_C;


    assign input_bit_A = C_out ^ nonlinear_bit_C ^ feedback_bit_input_A;
    assign input_bit_B = A_out ^ nonlinear_bit_A ^ feedback_bit_input_B;
    assign input_bit_C = B_out ^ nonlinear_bit_B ^ feedback_bit_input_C;


    assign key_stream = A_out ^ B_out ^ C_out;



endmodule : trivium
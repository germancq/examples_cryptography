module shift_register(
    input clk,
    input shift_right,
    input shift_left,
    input load,
    input input_bit,
    input [DATA_WIDTH-1 : 0] din,
    output logic output_bit,
    output logic feedback_bit_output,
    output logic feedback_bit_input,
    output logic nonlinear_bit,
    output logic [DATA_WIDTH-1 : 0] dout
);

parameter DATA_WIDTH = 8;
parameter FDBK_OUTPUT = 4;
parameter FDBK_INPUT = 5;
parameter NON_LINEAR_INDEX = 2;


always_ff @(posedge clk) begin
    feedback_bit_output <= dout[FDBK_OUTPUT-1];
    feedback_bit_input <= dout[FDBK_INPUT-1];
    nonlinear_bit <= dout[NON_LINEAR_INDEX-1] & dout[NON_LINEAR_INDEX-2];
    if(load == 1)
        begin
            dout <= din;
        end
    else if (shift_right == 1) 
        begin
            output_bit <= dout[0];
            
            dout[DATA_WIDTH-1:0] <= {input_bit,dout[DATA_WIDTH-1:1]};
        end        
    else if (shift_left == 1)  
        begin
            output_bit <= dout[DATA_WIDTH - 1];
            dout[DATA_WIDTH-1:0] <= {dout[DATA_WIDTH-2:0],input_bit};
        end 
end

endmodule : shift_register 
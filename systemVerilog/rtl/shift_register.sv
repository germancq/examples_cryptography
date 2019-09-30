module shift_register(
    input clk,
    input shift_right,
    input shift_left,
    input load,
    input input_bit,
    input [DATA_WIDTH-1 : 0] din,
    output logic output_bit,
    output logic [DATA_WIDTH-1 : 0] dout
);

parameter DATA_WIDTH = 8;

always_ff @(posedge clk) begin

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
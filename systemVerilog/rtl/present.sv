/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 12:33:30
 * @ Modified by: Your name
 * @ Modified time: 2019-09-30 19:28:28
 * @ Description:
 */

module present(

);

endmodule : present




module key_schedule(
    input clk,
    input rst,
    input [79:0] key,
    input [4:0] key_index,
    output logic end_signal,
    output logic [63:0] roundkey
    
);




logic key_register_cl;
logic key_register_w;
logic [79:0] key_register_input;
logic [79:0] key_register_output;

register #(.DATA_WIDTH(80)) key_register(
    .clk(clk),
    .cl(key_register_cl),
    .w(key_register_w),
    .din(key_register_input),
    .dout(key_register_output)
);


logic [4:0] counter_output;
logic counter_up;

counter #(.DATA_WIDTH(5)) counter_impl(
    .clk(clk),
    .rst(rst),
    .up(counter_up),
    .down(1'b0),
    .din(5'h0),
    .dout(counter_output)
);


logic [3:0] s_box_output;

S_box_enc sbox(
    .din(key_register_output[79:76]),
    .dout(s_box_output)
);

logic [2**5-1:0] [63:0] memory_data ;


typedef enum logic [2:0] {IDLE,STORE_KEY,SHIFT_KEY,SBOX_KEY,XOR_KEY,END,WAIT_1,WAIT_2} state_t;
state_t current_state, next_state;

always_comb begin

    next_state = current_state;

    counter_up = 0;
    end_signal = 1'b0;
    key_register_cl = 1'b0;
    key_register_w = 1'b0;
    roundkey = 64'h0;

    case(current_state)
        IDLE : 
            begin
                key_register_input = key;
                key_register_w = 1'b1;
                
                next_state = STORE_KEY;
                
                
            end
        STORE_KEY :
            begin
                
                memory_data[counter_output] = key_register_output[79:16];
                
                if(counter_output == 5'd31) begin
                    next_state = END;
                end
                else begin
                    next_state = SHIFT_KEY;
                end
            end 
        SHIFT_KEY :
            begin
                key_register_input = {key_register_output[18:0],                                      key_register_output[79:19]};
                key_register_w = 1'b1;
                counter_up = 1'b1;
                next_state = SBOX_KEY;
            end       
        SBOX_KEY :
            begin
                key_register_input = {s_box_output,key_register_output[75:0]};
                key_register_w = 1'b1;
                next_state = XOR_KEY;
            end
        XOR_KEY :
            begin
                key_register_input = {key_register_output[79:20],
                     key_register_output[19:15] ^ counter_output,key_register_output[14:0]};
                key_register_w = 1'b1;
                next_state = STORE_KEY;
            end      
        END :
            begin
                end_signal = 1'b1;
                roundkey = memory_data[key_index];
            end    

    endcase
end


always_ff @(posedge clk) begin
    if (rst) begin
        current_state <= IDLE;
    end
    else begin
        current_state <= next_state;
    end
end





endmodule : key_schedule



module S_box_enc(
    input [3:0] din,
    output logic [3:0] dout
);


parameter FILE_MEM = "~/gitProjects/examples_cryptography/systemVerilog/rtl/S_box_enc.mem";

//logic [3:0] s_box_contents [3:0]; //packed array
/*
initial begin
    $readmemh(FILE_MEM,s_box_contents);
end


assign dout = s_box_contents[din];
*/
always_comb begin
    case(din)
        0: dout = 4'hC;
        1: dout = 4'h5;
        2: dout = 4'h6;
        3: dout = 4'hB;
        4: dout = 4'h9;
        5: dout = 4'h0;
        6: dout = 4'hA;
        7: dout = 4'hD;
        8: dout = 4'h3;
        9: dout = 4'hE;
        10: dout = 4'hF;
        11: dout = 4'h8;
        12: dout = 4'h4;
        13: dout = 4'h7;
        14: dout = 4'h1;
        15: dout = 4'h2;
        default:  dout = 4'hC;
    endcase
end


endmodule: S_box_enc




module player_enc(
    input [63:0] din,
    output [63:0] dout
);

always_comb begin
    
    dout[0] = din[0];
    dout[1] = din[4];
    dout[2] = din[8];
    dout[3] = din[12];
    dout[4] = din[16];
    dout[5] = din[20];
    dout[6] = din[24];
    dout[7] = din[28];
    dout[8] = din[32];
    dout[9] = din[36];
    dout[10] = din[40];
    dout[11] = din[44];
    dout[12] = din[48];
    dout[13] = din[52];
    dout[14] = din[56];
    dout[15] = din[60];
    dout[16] = din[1];
    dout[17] = din[5];
    dout[18] = din[9];
    dout[19] = din[13];
    dout[20] = din[17];
    dout[21] = din[21];
    dout[22] = din[25];
    dout[23] = din[29];
    dout[24] = din[33];
    dout[25] = din[37];
    dout[26] = din[41];
    dout[27] = din[45];
    dout[28] = din[49];
    dout[29] = din[53];
    dout[30] = din[57];
    dout[31] = din[61];
    dout[32] = din[2];
    dout[33] = din[6];
    dout[34] = din[10];
    dout[35] = din[14];
    dout[36] = din[18];
    dout[37] = din[22];
    dout[38] = din[26];
    dout[39] = din[30];
    dout[40] = din[34];
    dout[41] = din[38];
    dout[42] = din[42];
    dout[43] = din[46];
    dout[44] = din[50];
    dout[45] = din[54];
    dout[46] = din[58];
    dout[47] = din[62];
    dout[48] = din[3];
    dout[49] = din[7];
    dout[50] = din[11];
    dout[51] = din[15];
    dout[52] = din[19];
    dout[53] = din[23];
    dout[54] = din[27];
    dout[55] = din[31];
    dout[56] = din[35];
    dout[57] = din[39];
    dout[58] = din[43];
    dout[59] = din[47];
    dout[60] = din[51];
    dout[61] = din[55];
    dout[62] = din[59];
    dout[63] = din[63];

end


endmodule : player_enc



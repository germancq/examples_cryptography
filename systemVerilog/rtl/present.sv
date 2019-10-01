/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 12:33:30
 * @ Modified by: Your name
 * @ Modified time: 2019-10-01 16:04:31
 * @ Description:
 */

module present(
    input clk,
    input rst,
    input enc_dec,
    input [79:0] key,
    input [63:0] block_input,
    output end_key_generation,
    output [63:0] block_output
);

    logic [4:0] key_index;
    logic [63:0] roundkey;
    logic [2**5-1:0] [63:0] roundkeys;

    logic [63:0] enc_o,dec_o;

    key_schedule key_sch_impl(
        .clk(clk),
        .rst(rst),
        .key(key),
        .key_index(key_index),
        .end_signal(end_key_generation),
        .roundkey(roundkey),
        .memory_data(roundkeys)
    );

    present_enc_x32 present_enc_impl(
        .roundkeys(roundkeys),
        .block_i(block_input),
        .block_o(enc_o)
    );

    present_dec_x32 present_dec_impl(
        .roundkeys(roundkeys),
        .block_i(block_input),
        .block_o(dec_o)
    );


    assign block_output = enc_dec ? dec_o : enc_o ; 


endmodule : present


module present_enc_x1(
    input clk,
    input [2**5-1:0] [63:0] roundkeys,
    input [63:0] block_i,
    output [63:0] block_o
);

endmodule : present_enc_x1


module present_enc_x32(
    input [2**5-1:0] [63:0] roundkeys,
    input [63:0] block_i,
    output [63:0] block_o
);

    logic [63:0] block_o_0,
                block_o_1,
                block_o_2,
                block_o_3,
                block_o_4,
                block_o_5,
                block_o_6,
                block_o_7,
                block_o_8,
                block_o_9,
                block_o_10,
                block_o_11,
                block_o_12,
                block_o_13,
                block_o_14,
                block_o_15,
                block_o_16,
                block_o_17,
                block_o_18,
                block_o_19,
                block_o_20,
                block_o_21,
                block_o_22,
                block_o_23,
                block_o_24,
                block_o_25,
                block_o_26,
                block_o_27,
                block_o_28,
                block_o_29;

    enc_stage enc_stage_0(
        .block_i(block_i ^ roundkeys[0]),
        .key_i(roundkeys[1]),
        .block_o(block_o_0)
    );
    enc_stage enc_stage_1(
        .block_i(block_o_0),
        .key_i(roundkeys[2]),
        .block_o(block_o_1)
    );
    enc_stage enc_stage_2(
        .block_i(block_o_1),
        .key_i(roundkeys[3]),
        .block_o(block_o_2)
    );
    enc_stage enc_stage_3(
        .block_i(block_o_2),
        .key_i(roundkeys[4]),
        .block_o(block_o_3)
    );
    enc_stage enc_stage_4(
        .block_i(block_o_3),
        .key_i(roundkeys[5]),
        .block_o(block_o_4)
    );
    enc_stage enc_stage_5(
        .block_i(block_o_4),
        .key_i(roundkeys[6]),
        .block_o(block_o_5)
    );
    enc_stage enc_stage_6(
        .block_i(block_o_5),
        .key_i(roundkeys[7]),
        .block_o(block_o_6)
    );
    enc_stage enc_stage_7(
        .block_i(block_o_6),
        .key_i(roundkeys[8]),
        .block_o(block_o_7)
    );
    enc_stage enc_stage_8(
        .block_i(block_o_7),
        .key_i(roundkeys[9]),
        .block_o(block_o_8)
    );
    enc_stage enc_stage_9(
        .block_i(block_o_8),
        .key_i(roundkeys[10]),
        .block_o(block_o_9)
    );
    enc_stage enc_stage_10(
        .block_i(block_o_9),
        .key_i(roundkeys[11]),
        .block_o(block_o_10)
    );
    enc_stage enc_stage_11(
        .block_i(block_o_10),
        .key_i(roundkeys[12]),
        .block_o(block_o_11)
    );
    enc_stage enc_stage_12(
        .block_i(block_o_11),
        .key_i(roundkeys[13]),
        .block_o(block_o_12)
    );
    enc_stage enc_stage_13(
        .block_i(block_o_12),
        .key_i(roundkeys[14]),
        .block_o(block_o_13)
    );
    enc_stage enc_stage_14(
        .block_i(block_o_13),
        .key_i(roundkeys[15]),
        .block_o(block_o_14)
    );
    enc_stage enc_stage_15(
        .block_i(block_o_14),
        .key_i(roundkeys[16]),
        .block_o(block_o_15)
    );
    enc_stage enc_stage_16(
        .block_i(block_o_15),
        .key_i(roundkeys[17]),
        .block_o(block_o_16)
    );
    enc_stage enc_stage_17(
        .block_i(block_o_16),
        .key_i(roundkeys[18]),
        .block_o(block_o_17)
    );
    enc_stage enc_stage_18(
        .block_i(block_o_17),
        .key_i(roundkeys[19]),
        .block_o(block_o_18)
    );
    enc_stage enc_stage_19(
        .block_i(block_o_18),
        .key_i(roundkeys[20]),
        .block_o(block_o_19)
    );
    enc_stage enc_stage_20(
        .block_i(block_o_19),
        .key_i(roundkeys[21]),
        .block_o(block_o_20)
    );
    enc_stage enc_stage_21(
        .block_i(block_o_20),
        .key_i(roundkeys[22]),
        .block_o(block_o_21)
    );
    enc_stage enc_stage_22(
        .block_i(block_o_21),
        .key_i(roundkeys[23]),
        .block_o(block_o_22)
    );
    enc_stage enc_stage_23(
        .block_i(block_o_22),
        .key_i(roundkeys[24]),
        .block_o(block_o_23)
    );
    enc_stage enc_stage_24(
        .block_i(block_o_23),
        .key_i(roundkeys[25]),
        .block_o(block_o_24)
    );
    enc_stage enc_stage_25(
        .block_i(block_o_24),
        .key_i(roundkeys[26]),
        .block_o(block_o_25)
    );
    enc_stage enc_stage_26(
        .block_i(block_o_25),
        .key_i(roundkeys[27]),
        .block_o(block_o_26)
    );
    enc_stage enc_stage_27(
        .block_i(block_o_26),
        .key_i(roundkeys[28]),
        .block_o(block_o_27)
    );
    enc_stage enc_stage_28(
        .block_i(block_o_27),
        .key_i(roundkeys[29]),
        .block_o(block_o_28)
    );
    enc_stage enc_stage_29(
        .block_i(block_o_28),
        .key_i(roundkeys[30]),
        .block_o(block_o_29)
    );
    enc_stage enc_stage_30(
        .block_i(block_o_29),
        .key_i(roundkeys[31]),
        .block_o(block_o)
    );


endmodule : present_enc_x32


module present_dec_x32(
    input [2**5-1:0] [63:0] roundkeys,
    input [63:0] block_i,
    output [63:0] block_o
);

    logic [30][63:0] blocks_o;
    
    

    dec_stage dec_stage_0(
        .block_i(block_i ^ roundkeys[31]),
        .key_i(roundkeys[30]),
        .block_o(blocks_o[0])
    );
    /*
    genvar i;
    generate
        for (i=1;i<31;i=i+1) begin
            dec_stage dec_stage_x(
                .block_i(blocks_o[i-1]),
                .key_i(roundkeys[30-i]),
                .block_o(blocks_o[i])
            );
        end
    endgenerate
    */
    
    dec_stage dec_stage_1(
        .block_i(blocks_o[0]),
        .key_i(roundkeys[29]),
        .block_o(blocks_o[1])
    );
    dec_stage dec_stage_2(
        .block_i(blocks_o[1]),
        .key_i(roundkeys[28]),
        .block_o(blocks_o[2])
    );
    dec_stage dec_stage_3(
        .block_i(blocks_o[2]),
        .key_i(roundkeys[27]),
        .block_o(blocks_o[3])
    );
    dec_stage dec_stage_4(
        .block_i(blocks_o[3]),
        .key_i(roundkeys[26]),
        .block_o(blocks_o[4])
    );
    dec_stage dec_stage_5(
        .block_i(blocks_o[4]),
        .key_i(roundkeys[25]),
        .block_o(blocks_o[5])
    );
    dec_stage dec_stage_6(
        .block_i(blocks_o[5]),
        .key_i(roundkeys[24]),
        .block_o(blocks_o[6])
    );
    dec_stage dec_stage_7(
        .block_i(blocks_o[6]),
        .key_i(roundkeys[23]),
        .block_o(blocks_o[7])
    );
    dec_stage dec_stage_8(
        .block_i(blocks_o[7]),
        .key_i(roundkeys[22]),
        .block_o(blocks_o[8])
    );
    dec_stage dec_stage_9(
        .block_i(blocks_o[8]),
        .key_i(roundkeys[21]),
        .block_o(blocks_o[9])
    );
    dec_stage dec_stage_10(
        .block_i(blocks_o[9]),
        .key_i(roundkeys[20]),
        .block_o(blocks_o[10])
    );
    dec_stage dec_stage_11(
        .block_i(blocks_o[10]),
        .key_i(roundkeys[19]),
        .block_o(blocks_o[11])
    );
    dec_stage dec_stage_12(
        .block_i(blocks_o[11]),
        .key_i(roundkeys[18]),
        .block_o(blocks_o[12])
    );
    dec_stage dec_stage_13(
        .block_i(blocks_o[12]),
        .key_i(roundkeys[17]),
        .block_o(blocks_o[13])
    );
    dec_stage dec_stage_14(
        .block_i(blocks_o[13]),
        .key_i(roundkeys[16]),
        .block_o(blocks_o[14])
    );
    dec_stage dec_stage_15(
        .block_i(blocks_o[14]),
        .key_i(roundkeys[15]),
        .block_o(blocks_o[15])
    );
    dec_stage dec_stage_16(
        .block_i(blocks_o[15]),
        .key_i(roundkeys[14]),
        .block_o(blocks_o[16])
    );
    dec_stage dec_stage_17(
        .block_i(blocks_o[16]),
        .key_i(roundkeys[13]),
        .block_o(blocks_o[17])
    );
    dec_stage dec_stage_18(
        .block_i(blocks_o[17]),
        .key_i(roundkeys[12]),
        .block_o(blocks_o[18])
    );
    dec_stage dec_stage_19(
        .block_i(blocks_o[18]),
        .key_i(roundkeys[11]),
        .block_o(blocks_o[19])
    );
    dec_stage dec_stage_20(
        .block_i(blocks_o[19]),
        .key_i(roundkeys[10]),
        .block_o(blocks_o[20])
    );
    dec_stage dec_stage_21(
        .block_i(blocks_o[20]),
        .key_i(roundkeys[9]),
        .block_o(blocks_o[21])
    );
    dec_stage dec_stage_22(
        .block_i(blocks_o[21]),
        .key_i(roundkeys[8]),
        .block_o(blocks_o[22])
    );
    dec_stage dec_stage_23(
        .block_i(blocks_o[22]),
        .key_i(roundkeys[7]),
        .block_o(blocks_o[23])
    );
    dec_stage dec_stage_24(
        .block_i(blocks_o[23]),
        .key_i(roundkeys[6]),
        .block_o(blocks_o[24])
    );
    dec_stage dec_stage_25(
        .block_i(blocks_o[24]),
        .key_i(roundkeys[5]),
        .block_o(blocks_o[25])
    );
    dec_stage dec_stage_26(
        .block_i(blocks_o[25]),
        .key_i(roundkeys[4]),
        .block_o(blocks_o[26])
    );
    dec_stage dec_stage_27(
        .block_i(blocks_o[26]),
        .key_i(roundkeys[3]),
        .block_o(blocks_o[27])
    );
    dec_stage dec_stage_28(
        .block_i(blocks_o[27]),
        .key_i(roundkeys[2]),
        .block_o(blocks_o[28])
    );
    dec_stage dec_stage_29(
        .block_i(blocks_o[28]),
        .key_i(roundkeys[1]),
        .block_o(blocks_o[29])
    );
    dec_stage dec_stage_30(
        .block_i(blocks_o[29]),
        .key_i(roundkeys[0]),
        .block_o(block_o)
    );
    

endmodule : present_dec_x32



module enc_stage(
    input [63:0] block_i,
    input [63:0] key_i,
    output [63:0] block_o
);

    logic [63:0] s_box_o;

    s_layer_enc slayer_i(
        .din(block_i),
        .dout(s_box_o)
    );

    logic [63:0] p_layer_o;

    player_enc player_i(
        .din(s_box_o),
        .dout(p_layer_o)
    );

    assign block_o = p_layer_o ^ key_i;


endmodule : enc_stage


module dec_stage(
    input [63:0] block_i,
    input [63:0] key_i,
    output [63:0] block_o
);

    logic [63:0] p_layer_o;

    player_dec player_i(
        .din(block_i),
        .dout(p_layer_o)
    );

    logic [63:0] s_box_o;

    s_layer_dec slayer_i(
        .din(p_layer_o),
        .dout(s_box_o)
    );

    

    assign block_o = s_box_o ^ key_i;


endmodule : dec_stage



module key_schedule(
    input clk,
    input rst,
    input [79:0] key,
    input [4:0] key_index,
    output logic end_signal,
    output [63:0] roundkey,
    output logic [2**5-1:0] [63:0] memory_data
    
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

    //logic [2**5-1:0] [63:0] memory_data ;


    typedef enum logic [2:0] {IDLE,STORE_KEY,SHIFT_KEY,SBOX_KEY,XOR_KEY,END,WAIT_1,WAIT_2} state_t;
    state_t current_state, next_state;

    assign roundkey = end_signal ? memory_data[key_index] : 64'h0;

    always_comb begin

        next_state = current_state;

        counter_up = 0;
        end_signal = 1'b0;
        key_register_cl = 1'b0;
        key_register_w = 1'b0;
        

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
                    //roundkey = memory_data[key_index];
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


module S_box_dec(
    input [3:0] din,
    output logic [3:0] dout
);

    always_comb begin
        case(din)
            0: dout = 4'h5;
            1: dout = 4'hE;
            2: dout = 4'hF;
            3: dout = 4'h8;
            4: dout = 4'hC;
            5: dout = 4'h1;
            6: dout = 4'h2;
            7: dout = 4'hD;
            8: dout = 4'hB;
            9: dout = 4'h4;
            10: dout = 4'h6;
            11: dout = 4'h3;
            12: dout = 4'h0;
            13: dout = 4'h7;
            14: dout = 4'h9;
            15: dout = 4'hA;
            default:  dout = 4'h5;
        endcase
    end


endmodule: S_box_dec


module s_layer_enc(
    input [63:0] din,
    output [63:0] dout
);

    genvar i;
    generate
        for (i=0;i<16;i=i+1) begin
            S_box_enc sbox(
                .din(din[(i*4)+3:i*4]),
                .dout(dout[(i*4)+3:i*4])
            );
        end
    endgenerate

    



endmodule : s_layer_enc


module s_layer_dec(
    input [63:0] din,
    output [63:0] dout
);

    genvar i;
    generate
        for (i=0;i<16;i=i+1) begin
            S_box_dec sbox(
                .din(din[(i*4)+3:i*4]),
                .dout(dout[(i*4)+3:i*4])
            );
        end
    endgenerate

    



endmodule : s_layer_dec


module player_enc(
    input [63:0] din,
    output logic [63:0] dout
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


module player_dec(
    input [63:0] din,
    output logic [63:0] dout
);

    always_comb begin
        
        dout[0] = din[0];
        dout[4] = din[1];
        dout[8] = din[2];
        dout[12] = din[3];
        dout[16] = din[4];
        dout[20] = din[5];
        dout[24] = din[6];
        dout[28] = din[7];
        dout[32] = din[8];
        dout[36] = din[9];
        dout[40] = din[10];
        dout[44] = din[11];
        dout[48] = din[12];
        dout[52] = din[13];
        dout[56] = din[14];
        dout[60] = din[15];
        dout[1] = din[16];
        dout[5] = din[17];
        dout[9] = din[18];
        dout[13] = din[19];
        dout[17] = din[20];
        dout[21] = din[21];
        dout[25] = din[22];
        dout[29] = din[23];
        dout[33] = din[24];
        dout[37] = din[25];
        dout[41] = din[26];
        dout[45] = din[27];
        dout[49] = din[28];
        dout[53] = din[29];
        dout[57] = din[30];
        dout[61] = din[31];
        dout[2] = din[32];
        dout[6] = din[33];
        dout[10] = din[34];
        dout[14] = din[35];
        dout[18] = din[36];
        dout[22] = din[37];
        dout[26] = din[38];
        dout[30] = din[39];
        dout[34] = din[40];
        dout[38] = din[41];
        dout[42] = din[42];
        dout[46] = din[43];
        dout[50] = din[44];
        dout[54] = din[45];
        dout[58] = din[46];
        dout[62] = din[47];
        dout[3] = din[48];
        dout[7] = din[49];
        dout[11] = din[50];
        dout[15] = din[51];
        dout[19] = din[52];
        dout[23] = din[53];
        dout[27] = din[54];
        dout[31] = din[55];
        dout[35] = din[56];
        dout[39] = din[57];
        dout[43] = din[58];
        dout[47] = din[59];
        dout[51] = din[60];
        dout[55] = din[61];
        dout[59] = din[62];
        dout[63] = din[63];

    end


endmodule : player_dec

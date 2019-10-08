/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 12:33:30
 * @ Modified by: Your name
 * @ Modified time: 2019-10-07 12:45:07
 * @ Description:
 */

module present_x32(
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


endmodule : present_x32


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

    logic [29:0][63:0] blocks_o;
    
    

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
    logic memory_data_w;

    typedef enum logic [2:0] {IDLE,STORE_KEY,SHIFT_KEY,SBOX_KEY,XOR_KEY,END,WAIT_1,WAIT_2} state_t;
    state_t current_state, next_state;

    assign roundkey = end_signal ? memory_data[key_index] : 64'h0;

    always_comb begin

        next_state = current_state;

        counter_up = 0;
        memory_data_w = 0;
        end_signal = 1'b0;
        key_register_cl = 1'b0;
        key_register_w = 1'b0;
        key_register_input = 80'h0;
        

        case(current_state)
            IDLE : 
                begin
                    key_register_input = key;
                    key_register_w = 1'b1;
                    
                    next_state = STORE_KEY;
                    
                    
                end
            STORE_KEY :
                begin
                    
                    //memory_data[counter_output] = key_register_output[79:16];
                    memory_data_w = 1;

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


    always_ff @(posedge clk) begin
        if (memory_data_w == 1'b1) begin
            memory_data[counter_output] <= key_register_output[79:16];
        end
    end




endmodule : key_schedule










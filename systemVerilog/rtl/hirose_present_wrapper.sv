/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-14 15:28:48
 * @ Modified by: Your name
 * @ Modified time: 2019-11-07 13:39:40
 * @ Description:
 */


module hirose_present_wrapper(
    input clk,
    input rst,
    input [DATA_WIDTH-1:0] plaintext,
    input [63:0] c,
    output [127:0] hash_output,
    output logic end_signal
);

    parameter DATA_WIDTH = 64;

    logic rst_hash;
    logic [15:0] hash_plaintext;
    logic end_hash;
    logic [127:0] hash_o;


    logic h_left_w;
    logic [63:0] h_left_o;
    

    logic h_right_w;
    logic [63:0] h_right_o;

    assign hash_output = {h_left_o,h_right_o};


    hirose_present hash_impl(
        .clk(clk),
        .rst(rst_hash),
        .c(c),
        .plaintext(hash_plaintext),
        .prev_left_value(h_left_o),
        .prev_right_value(h_right_o),
        .end_hash(end_hash),
        .hash_o(hash_o)
    );

    logic [$clog2(DATA_WIDTH)-1:0] counter_output;
    logic counter_up;

    counter #(.DATA_WIDTH($clog2(DATA_WIDTH))) counter_impl(
        .clk(clk),
        .rst(rst),
        .up(counter_up),
        .down(1'b0),
        .din({$clog2(DATA_WIDTH){1'b0}}),
        .dout(counter_output)
    );


    
    

    register #(.DATA_WIDTH(64)) H_left(
        .clk(clk),
        .cl(rst),
        .w(h_left_w),
        .din(hash_o[127:64]),
        .dout(h_left_o)
    );

    register #(.DATA_WIDTH(64)) H_right(
        .clk(clk),
        .cl(rst),
        .w(h_right_w),
        .din(hash_o[63:0]),
        .dout(h_right_o)
    );

    assign hash_plaintext = plaintext >> (counter_output<<4);


    hirose_wrapper_fsm #(.DATA_WIDTH(DATA_WIDTH)) fsm(
            .clk(clk),
            .rst(rst),

            .counter_output(counter_output),
            .end_hash(end_hash),

            .counter_up(counter_up),
            .h_left_w(h_left_w),
            .h_right_w(h_right_w),
            .rst_hash(rst_hash),
            .end_signal(end_signal)
    );


    /*
    typedef enum logic [1:0] {IDLE,WAIT_FOR_ENC,WRITE_PREV_VALUES,END} state_t;
    state_t current_state, next_state;

    

    

    always_comb begin

        next_state = current_state;

        counter_up = 0;
        h_left_w = 0;
        h_right_w = 0;
        rst_hash = 0;

        end_signal = 0;

        

        case(current_state)
            IDLE : 
                begin
                    rst_hash = 1;
                    h_left_w = 1'b1;
                    h_right_w = 1'b1;
                    
                    next_state = WAIT_FOR_ENC;
                end
            WAIT_FOR_ENC :
                begin
                    if(end_hash) begin
                        next_state = WRITE_PREV_VALUES;
                        h_left_w = 1'b1;
                        h_right_w = 1'b1;
                        counter_up = 1'b1;
                    end
                end    
            WRITE_PREV_VALUES :
                begin
                    rst_hash = 1'b1;
                    if(counter_output == (DATA_WIDTH>>4) ) begin
                        next_state = END;
                    end
                    else begin
                        next_state = WAIT_FOR_ENC;
                    end
                end    
            END :
                begin
                    end_signal = 1'b1;
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
    */

endmodule : hirose_present_wrapper



module hirose_wrapper_fsm(
    input clk,
    input rst,

    input [$clog2(DATA_WIDTH)-1:0] counter_output,
    input end_hash,

    output logic counter_up,
    output logic h_left_w,
    output logic h_right_w,
    output logic rst_hash,
    output logic end_signal

);

    parameter DATA_WIDTH = 64;

    typedef enum logic [1:0] {IDLE,WAIT_FOR_ENC,WRITE_PREV_VALUES,END} state_t;
    state_t current_state, next_state;

    

    always_comb begin

        next_state = current_state;

        counter_up = 0;
        h_left_w = 0;
        h_right_w = 0;
        rst_hash = 0;

        end_signal = 0;

        

        case(current_state)
            IDLE : 
                begin
                    rst_hash = 1;
                    h_left_w = 1'b1;
                    h_right_w = 1'b1;
                    
                    next_state = WAIT_FOR_ENC;
                end
            WAIT_FOR_ENC :
                begin
                    if(end_hash) begin
                        next_state = WRITE_PREV_VALUES;
                        h_left_w = 1'b1;
                        h_right_w = 1'b1;
                        counter_up = 1'b1;
                    end
                end    
            WRITE_PREV_VALUES :
                begin
                    rst_hash = 1'b1;
                    if(counter_output == (DATA_WIDTH>>4) ) begin
                        next_state = END;
                    end
                    else begin
                        next_state = WAIT_FOR_ENC;
                    end
                end    
            END :
                begin
                    end_signal = 1'b1;
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

endmodule : hirose_wrapper_fsm
module hirose_present(
    input clk,
    input rst,
    input [63:0] c
);

    logic [63:0] input_left;
    logic [63:0] input_right;
    logic [63:0] output_left;
    logic [63:0] output_right;

    


    present present_left(
        .clk(),
        .rst(),
        .end_key_generation(),
        .key(),
        .block_i().
        .block_o(),
        .enc_dec(1'b0),
        .end_dec(),
        .end_enc()
    );

    present present_right(
        .clk(),
        .rst(),
        .end_key_generation(),
        .key(),
        .block_i().
        .block_o(),
        .enc_dec(1'b0),
        .end_dec(),
        .end_enc()
    );


    register #(.DATA_WIDTH(64)) H_left(
        .clk(),
        .cl(),
        .w(),
        .din(),
        .dout()
    );

    register #(.DATA_WIDTH(64)) H_right(
        .clk(),
        .cl(),
        .w(),
        .din(),
        .dout()
    );


    typedef enum logic { IDLE,UPDATE_KEYS, WAIT_ENC, END  } state_t;
    state_t current_state, next_state;

    always_comb begin
        next_state = current_state;
    end


    always_ff @(posedge clk) begin
        if (rst) begin
            next_state <= IDLE;
        end
        else begin
            next_state <= current_state;
        end
    end


endmodule : hirose_present
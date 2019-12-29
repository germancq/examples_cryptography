/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-12-16 13:06:12
 * @ Modified by: Your name
 * @ Modified time: 2019-12-29 02:48:40
 * @ Description:
 */

module spongent #(
    parameter N = 256,
    parameter c = 256,
    parameter r = 16,
    parameter R = 140,
    parameter lCounter_initial_state = 8'h9E,
    parameter lCounter_feedback_coeff = 9'h11D,
    parameter DATA_WIDTH = 64
)
(
    input clk,
    input rst,
    input [DATA_WIDTH-1:0] msg,
    output [N-1:0] hash,
    output end_hash
);
    parameter b = c+r;

    logic rst_lCounter;
    logic shift_lCounter;
    logic [$clog2(R)-1:0] lCounter_state;

    LFSR #(.DATA_WIDTH($clog2(R))) lCounter(
        .clk(clk),
        .rst(rst_lCounter),
        .shift(shift_lCounter),
        .feedback_coeff(lCounter_feedback_coeff),
        .initial_state(lCounter_initial_state),
        .state(lCounter_state)
    );

    logic [b-1:0] permutation_state;
    logic [b-1:0] permutation_initial_state;
    logic end_permutation;
    logic rst_permutation;

    assign rst_permutation = end_absorbing == 0 ? rst_permutation_from_absorb : rst_permutation_from_squezzing ;

    assign permutation_initial_state = end_absorbing == 0 ? permutation_initial_state_from_absorb : permutation_initial_state_from_squezzing;

    permutation #(.DATA_WIDTH(b),.R(R)) permutation_impl(
        .clk(clk),
        .rst(rst_permutation),
        .initial_state(permutation_initial_state),
        .lCounter_state(lCounter_state),
        .rst_lCounter(rst_lCounter),
        .shift_lCounter(shift_lCounter),
        .end_permutation(end_permutation),
        .state(permutation_state)
    );

    logic [DATA_WIDTH-1+(r - (DATA_WIDTH % r)):0] padded_msg;
    assign padded_msg = msg << (r - (DATA_WIDTH % r)) | 1'b1 << (r - (DATA_WIDTH % r) - 1);

    logic end_absorbing;
    logic [b-1:0] absorbing_state;
    logic rst_permutation_from_absorb;
    logic [b-1:0] permutation_initial_state_from_absorb;

    absorbing_phase #(.DATA_WIDTH(DATA_WIDTH),.b(b),.r(r)) absorbing_phase_impl(
        .clk(clk),
        .rst(rst),
        .end_permutation(end_permutation),
        .padded_msg(padded_msg),
        .permutation_state(permutation_state),
        .rst_permutation(rst_permutation_from_absorb),
        .permutation_initial_state(permutation_initial_state_from_absorb),
        .end_absorbing(end_absorbing),
        .absorbing_state(absorbing_state)  
    );

    logic rst_permutation_from_squezzing;
    logic [b-1:0] permutation_initial_state_from_squezzing;

    squeezing_phase #(.N(N),.r(r),.b(b)) squeezing_phase_impl(
        .clk(clk),
        .rst(rst | ~end_absorbing),
        .end_permutation(end_permutation),
        .permutation_state(permutation_state),
        .rst_permutation(rst_permutation_from_squezzing),
        .permutation_initial_state(permutation_initial_state_from_squezzing),
        .end_squeezing(end_hash),
        .result(hash)
    );

endmodule : spongent


module absorbing_phase #(
    parameter DATA_WIDTH = 256,
    parameter b = 88,
    parameter r = 8
)
(
    input clk,
    input rst,
    input end_permutation,
    input [DATA_WIDTH-1+(r - (DATA_WIDTH % r)):0] padded_msg,
    input [b-1:0] permutation_state,
    output logic rst_permutation,
    output [b-1:0] permutation_initial_state,
    output end_absorbing,
    output logic [b-1:0] absorbing_state
);
    localparam DATA_WIDTH_PADDED = DATA_WIDTH + (r - (DATA_WIDTH % r));
    
    logic [$clog2(DATA_WIDTH_PADDED/r):0] counter_o;
    logic counter_up;

    counter #(.DATA_WIDTH($clog2(DATA_WIDTH_PADDED/r)+1)) counter_impl(
        .clk(clk),
        .rst(rst),
        .up(counter_up),
        .down(1'b0),
        .din({$clog2(DATA_WIDTH_PADDED/r)+1{1'b0}}),
        .dout(counter_o)
    );

    logic [b-1:0] state;
    assign absorbing_state = state;

    logic [r-1:0] msg_chunk;
    assign msg_chunk = padded_msg >> ((DATA_WIDTH_PADDED/r - counter_o - 1)*r);
    assign permutation_initial_state = r==8 ? msg_chunk ^ state : {msg_chunk[7:0],msg_chunk[15:8]} ^ state;

    assign end_absorbing = counter_o == (DATA_WIDTH_PADDED/r) ? 1 : 0;

    typedef enum logic [1:0] {IDLE,PERMUTATION,RST_PERMUTATION,END} state_t;
    state_t current_state, next_state;

    

    always_comb begin
        next_state = current_state;
        rst_permutation = 1;
        counter_up = 0;
        case(current_state)
            IDLE : begin
                next_state = PERMUTATION;
            end
            PERMUTATION : begin
                rst_permutation = 0;
                if(end_permutation == 1) begin
                    //store permutation state
                    counter_up = 1;
                    next_state = RST_PERMUTATION;
                end
            end
            RST_PERMUTATION : begin
                next_state = PERMUTATION;
                if(end_absorbing == 1) begin
                    rst_permutation = 0;
                    next_state = END;
                end
            end
            END : begin
                rst_permutation = 0;
            end
            default:;
        endcase
    end

    always_ff @(posedge clk) begin
        case(current_state)
            IDLE : begin
                state <= 0;
            end
            PERMUTATION : begin
                if(end_permutation == 1) begin
                    //store permutation state
                    state <= permutation_state;
                end
            end
            RST_PERMUTATION : begin
                
            end
            END : begin
                
            end
            default:;
        endcase
    end

    always_ff @(posedge clk) begin
        
        if(rst == 1) begin
            current_state <= IDLE;
        end
        else begin
            current_state <= next_state;
        end
        
    end


endmodule: absorbing_phase



module squeezing_phase #(
    parameter N = 88,
    parameter b = 88,
    parameter r = 8
)
(
    input clk,
    input rst,
    input end_permutation,
    input [b-1:0] permutation_state,
    output logic rst_permutation,
    output [b-1:0] permutation_initial_state,
    output end_squeezing,
    output logic [N-1:0] result
);


    logic [$clog2(N/r):0] counter_o;
    logic counter_up;

    counter #(.DATA_WIDTH($clog2(N/r)+1)) counter_impl(
        .clk(clk),
        .rst(rst),
        .up(counter_up),
        .down(1'b0),
        .din({$clog2(N/r)+1{1'b0}}),
        .dout(counter_o)
    );

    assign end_squeezing = counter_o >= N/r -1  ? 1 : 0;

    logic [b-1:0] state;
    assign permutation_initial_state = state;

    logic [r-1:0] result_chunk;
    assign result_chunk = r==8 ? permutation_state[r-1:0] : {permutation_state[7:0],permutation_state[15:8]};

    typedef enum logic [1:0] {IDLE,PERMUTATION,RST_PERMUTATION,END} state_t;
    state_t current_state, next_state;

    always_comb begin
        next_state = current_state;
        rst_permutation = 1;
        counter_up = 0;
        case(current_state)
            IDLE : begin
                rst_permutation = 0;
                next_state = RST_PERMUTATION;
            end
            RST_PERMUTATION : begin
                next_state = PERMUTATION;
                
                if(end_squeezing == 1) begin
                    next_state = END;
                end
            end
            PERMUTATION : begin
                rst_permutation = 0;
                if(end_permutation == 1) begin
                    next_state = RST_PERMUTATION;
                    counter_up = 1;
                end
            end
            END : begin
                
            end
            default:;
        endcase
    end

    always_ff @(posedge clk) begin

        case(current_state)
            IDLE : begin
                result <= result_chunk;
                state <= permutation_state;
            end
            RST_PERMUTATION : begin
                
            end
            PERMUTATION : begin
                if(end_permutation == 1) begin
                    state <= permutation_state;
                    result <= (result << r) | result_chunk;
                end
            end
            END : begin
                
            end
            default:;
        endcase
    end

    always_ff @(posedge clk) begin
        if(rst == 1) begin
            current_state <= IDLE;
        end
        else begin
            current_state <= next_state;
        end
    end


endmodule : squeezing_phase


module permutation #(
    parameter DATA_WIDTH = 88,
    parameter R = 45
)
(
    input clk,
    input rst,
    input [DATA_WIDTH-1:0] initial_state,
    input [$clog2(R)-1:0] lCounter_state,
    output rst_lCounter,
    output shift_lCounter,
    output end_permutation,
    output [DATA_WIDTH-1:0] state
);

    logic [DATA_WIDTH-1:0] state_reg;
   

    logic [$clog2(R)-1:0] counter_o;

    counter #(.DATA_WIDTH($clog2(R))) counter_impl(
        .clk(clk),
        .rst(rst),
        .up(~end_permutation),
        .down(1'b0),
        .din({$clog2(R){1'b0}}),
        .dout(counter_o)
    );

    assign rst_lCounter = rst;
    assign end_permutation = counter_o == R ? 1 : 0 ;
    assign shift_lCounter = ~end_permutation;
    logic [$clog2(R)-1:0] reverse_lCounter;

    genvar i;

    generate
        for (i = 0;i<$clog2(R) ;i=i+1 ) begin
            assign reverse_lCounter[i] = lCounter_state[$clog2(R)-1-i];
        end
    endgenerate

    



    always_ff @(posedge clk) begin
        if(rst == 1) begin
            state_reg <= initial_state;
        end
        else if(end_permutation == 0 && counter_o == 0) begin
            state_reg <= state_reg ^ lCounter_state ^ (reverse_lCounter << (DATA_WIDTH - $clog2(R)));
        end
        else if(end_permutation == 0) begin
            state_reg <= state ^ lCounter_state ^ (reverse_lCounter << (DATA_WIDTH-$clog2(R)));
        end
    end

    logic [DATA_WIDTH-1:0] state_S_box;
    
    generate 
        for (i = 0;i<(DATA_WIDTH>>2);i=i+1) begin
            S_box s_box_i(
                .din(state_reg[(i<<2)+3:i<<2]),
                .dout(state_S_box[(i<<2)+3:i<<2])
            );
        end
    endgenerate

    pLayer #(.DATA_WIDTH(DATA_WIDTH)) pLayer_impl(
        .din(state_S_box),
        .dout(state)
    );


endmodule : permutation


module S_box(
    input [3:0] din,
    output logic [3:0] dout
);

    always_comb begin
        case(din)
            0: dout = 4'hE;
            1: dout = 4'hD;
            2: dout = 4'hB;
            3: dout = 4'h0;
            4: dout = 4'h2;
            5: dout = 4'h1;
            6: dout = 4'h4;
            7: dout = 4'hF;
            8: dout = 4'h7;
            9: dout = 4'hA;
            10: dout = 4'h8;
            11: dout = 4'h5;
            12: dout = 4'h9;
            13: dout = 4'hC;
            14: dout = 4'h3;
            15: dout = 4'h6;
            default:  dout = 4'hE;
        endcase
    end


endmodule: S_box


module pLayer #(
    parameter DATA_WIDTH = 88
)
(
    input [DATA_WIDTH-1:0] din,
    output [DATA_WIDTH-1:0] dout
);

    genvar i;
    generate
        for (i = 0;i<DATA_WIDTH-1 ;i=i+1 ) begin
            assign dout[(i * DATA_WIDTH>>2) % (DATA_WIDTH-1)] = din[i];
        end
    endgenerate

    assign dout[DATA_WIDTH-1] = din[DATA_WIDTH-1];



endmodule : pLayer

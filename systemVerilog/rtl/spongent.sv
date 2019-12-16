/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-12-16 13:06:12
 * @ Modified by: Your name
 * @ Modified time: 2019-12-16 17:43:37
 * @ Description:
 */

module spongent #(
    parameter N = 88,
    parameter c = 80,
    parameter r = 8,
    parameter lCounter_initial_state = 6'h5,
    parameter lCounter_feedback_coeff = 7'h61,
    parameter DATA_WIDTH = 256
)
(

);
    parameter b = c+r;

    

endmodule : spongent



module permutation #(
    parameter DATA_WIDTH = 88,
    parameter R = 45
)
(
    input clk,
    input rst,
    input initial_state,
    input lCounter_state,
    output rst_lCounter,
    output shift_lCounter,
    output end_permutation,
    output [DATA_WIDTH-1:0] state
);

    //logic stat

    logic [$clog2(R):0] counter_o;

    counter #(.DATA_WIDTH($clog2(R)+1)) (
        .clk(clk),
        .rst(rst),
        .up(~end_permutation),
        .down(1'b0),
        .din('{default:0}),
        .dout()
    );

    assign rst_lCounter = rst;
    assign end_permutation = counter_o == R ? 1 : 0 ;
    assign shift_lCounter = ~end_permutation;

    always_ff @(posedge clk) begin
        if(rst == 1) begin
            state = initial_state;
        end
        else if(end_permutation == 0) begin
            state = state ^ lCounter_state[:0] ^ (lCounter_state[0:] << );
        end
    end


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

    generate
        for (genvar i = 0;i<DATA_WIDTH-1 ;i=i+1 ) begin
            assign dout[(i * DATA_WIDTH>>2) % (DATA_WIDTH-1)] = din[i];
        end
    endgenerate

    assign dout[DATA_WIDTH-1] = din[DATA_WIDTH-1];



endmodule : pLayer

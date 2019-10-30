/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-30 12:07:13
 * @ Modified by: Your name
 * @ Modified time: 2019-10-30 12:42:34
 * @ Description:
 */

module adder(
    input [N-1:0] a,
    input [N-1:0] b,
    output [N-1:0] s,
    output c

);
    parameter N = 32;

    logic [N-1:0] carry_values;

    half_adder h0(
        .a(a[0]),
        .b(b[0]),
        .carry(carry_values[0]),
        .s(s[0])
    );

    genvar i;
    generate 
        for(i=1;i<N;i=i+1) begin
            full_adder f_i(
                .a(a[i]),
                .b(b[i]),
                .c(carry_values[i-1]),
                .carry(carry_values[i]),
                .s(s[i])
            );
        end
    endgenerate

    assign c = carry_values[N-1];

endmodule : adder


module fast_adder(
     input [N-1:0] a,
     input [N-1:0] b,
     output [N-1:0] s,
     output c   
);
    parameter N = 32;

    logic [N>>2:0] carry_values;
    assign carry_values[0] = 0;
    assign c = carry_values[N>>2];

    genvar i;
    generate
        for (i=0;i<(N>>2);i=i+1) begin
            fast_adder_4 f_i(
                .a(a[(4*i)+3:4*i]),
                .b(b[(4*i)+3:4*i]),
                .carry_in(carry_values[i]),
                .s(s[(4*i)+3:4*i]),
                .c(carry_values[i+1])
            );
        end
    endgenerate
    

endmodule : fast_adder


module fast_adder_4(
    input [3:0] a,
    input [3:0] b,
    input carry_in,
    output [3:0] s,
    output c
);

    logic [3:0] carry_values;
    logic [3:0] P;
    logic [3:0] G;

    genvar i;
    generate
        for (i=0;i<4;i=i+1) begin
            full_adder_propagation f_i(
                .a(a[i]),
                .b(b[i]),
                .c(carry_values[i]),
                .s(s[i]),
                .p(P[i]),
                .g(G[i])
            );
        end
    endgenerate    

    //C[i+1] = G[i] + P[i]C[i]
    assign carry_values[0] = carry_in;
    assign carry_values[1] = G[0] | (P[0] & carry_values[0]);
    assign carry_values[2] = G[1] | 
                            (G[0] & P[1]) | 
                            (P[0] & carry_values[0] & P[1]);
    assign carry_values[3] = G[2] |
                            (G[1] & P[2]) |
                            (G[0] & P[1] & P[2]) |
                            (P[0] & carry_values[0] & P[1] & P[2]);
    assign c = G[3] |
               (G[2] & P[3]) |
               (G[1] & P[2] & P[3]) |
               (G[0] & P[1] & P[2] & P[3]) |
               (P[0] & carry_values[0] & P[1] & P[2] & P[3]);                        

endmodule : fast_adder_4




module half_adder(
    input a,
    input b,
    output carry,
    output s
);

    assign s = a ^ b;
    assign carry = a & b;

endmodule : half_adder


module full_adder(
    input a,
    input b,
    input c,
    output carry,
    output s
);

    logic c_0;
    logic c_1;
    logic s_0;

    half_adder h0(
        .a(a),
        .b(b),
        .carry(c_0),
        .s(s_0)
    );

    half_adder h1(
        .a(s_0),
        .b(c),
        .carry(c_1),
        .s(s)
    );

    assign carry = c_0 | c_1;

endmodule : full_adder

module full_adder_propagation(
    input a,
    input b,
    input c,
    output p,
    output g,
    output s
);

    logic c_0;
    logic c_1;
    logic s_0;

    half_adder h0(
        .a(a),
        .b(b),
        .carry(c_0),
        .s(s_0)
    );

    half_adder h1(
        .a(s_0),
        .b(c),
        .carry(c_1),
        .s(s)
    );

    
    assign p = a ^ b;
    assign g = a & b;

endmodule : full_adder_propagation
module galois_adder(
    input [N-1:0] a,
    input [N-1:0] b,
    output [N-1:0] s
);

    parameter N = 8;

    assign s = a ^ b;

endmodule : galois_adder


module galois_multiplication(
    input [(2*N)-2:0] a,
    input [(2*N)-2:0] b,
    input [N:0] p,
    output [N-1:0] s
);

    parameter N = 8;

    logic [(2*N)-2:0] m_out [(N<<1)-2:0];
    genvar i;
    generate 
        for (i=0; i<N;i=i+1 ) begin
            mux2 #(.N((2*N)-1)) m_i(
                .a(0),
                .b(a << i),
                .sel(b[i]),
                .c(m_out[i])
            );
        end
    endgenerate
    
    genvar j;
    generate
        for (j=0;j<N-1;j=j+1) begin
            galois_adder #(.N((2*N)-1)) g_i(
                .a(m_out[j<<1]),
                .b(m_out[(j<<1)+1]),
                .s(m_out[j+N])
            );
        end
    endgenerate

    polinomial_reduction #(.N(N)) polinomial_inst(
        .a(m_out[(N<<1)-2]),
        .p(p),
        .s(s)
    );



endmodule : galois_multiplication


module polinomial_reduction (
    input [(2*N)-2:0] a,
    input [(2*N)-2:0] p,
    output [N-1:0] s
);

    parameter N = 8;
    parameter degree_p = 8;

    logic [(2*N)-2:0] m_out [N-1:0]; 
    logic [(2*N)-2:0] polinomials [N-1:0]; 
    assign polinomials[N-1] = a;
    
    genvar i;
    generate 
        for (i=N-2; i>=0;i=i-1 ) begin
        
            mux2 #(.N((2*N)-1)) m_i(
                .a(0),
                .b(p << (degree_p-N+i)),
                .sel(polinomials[i+1][N+i]),
                .c(m_out[i])
            );
            
            galois_adder #(.N((2*N)-1)) g_i(
                .a(polinomials[i+1]),
                .b(m_out[i]),
                .s(polinomials[i])
            );
        end
    endgenerate

    assign s = polinomials[0];
    

endmodule : polinomial_reduction




module mux2 (
    input [N-1:0] a,
    input [N-1:0] b,
    input sel,
    output [N-1:0] c
);

    parameter N = 8;
    
    assign c = sel ? b : a ;

endmodule : mux2

/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-31 12:05:35
 * @ Modified by: Your name
 * @ Modified time: 2019-10-31 13:51:55
 * @ Description:
 */


module matrix_multiplication(
    input [N-1:0] a [(ROW_A*COL_A)-1:0],
    input [N-1:0] b [(COL_A*COL_B)-1:0],
    input [N:0] p,
    output [N-1:0] s [(ROW_A*COL_B)-1:0]
);

    parameter N = 8;
    parameter COL_A = 4;
    parameter ROW_A = 4;
    parameter COL_B = 1;

    genvar i;
    genvar j;
    genvar k;
    generate
        for (i=0;i<ROW_A;i=i+1) begin
            logic [N-1:0] A_row [COL_A-1:0];
            for (k = 0;k<COL_A;k=k+1) begin
                assign A_row[k] = a[(i*COL_A)+k];
            end


            for (j=0;j<COL_B ;j=j+1) begin
                logic [N-1:0] B_col [COL_A-1:0];
                for (k = 0;k<COL_A;k=k+1) begin
                    assign B_col[k] = b[(k*COL_B)+j];
                end

                row_x_column #(.N(N),.ELEM_SIZE(COL_A)) rc3(
                    .a(A_row),
                    .b(B_col),
                    .p(p),
                    .s(s[(COL_B*i)+j])
                );
            end
        end

    endgenerate

endmodule : matrix_multiplication




module row_x_column(
    input [N-1:0] a [ELEM_SIZE-1:0],
    input [N-1:0] b [ELEM_SIZE-1:0],
    input [N:0] p,
    output [N-1:0] s
);

    parameter N = 8;
    parameter ELEM_SIZE = 4;

    logic [N-1:0] mult_out [(ELEM_SIZE<<1)-2:0];

    genvar i;
    generate
        for (i = 0;i<ELEM_SIZE ;i=i+1 ) begin
            galois_multiplication #(.N(N)) g_m_i(
                .a(a[i]),
                .b(b[i]),
                .p(p),
                .s(mult_out[i])
            );
        end
    endgenerate

    genvar j;
    generate
        for (j = 0;j<ELEM_SIZE-1 ;j=j+1 ) begin
            galois_adder #(.N(N)) g_i(
                .a(mult_out[j<<1]),
                .b(mult_out[(j<<1)+1]),
                .s(mult_out[j+ELEM_SIZE])
            );
        end
    endgenerate

    assign s = mult_out[(ELEM_SIZE<<1)-2];


endmodule : row_x_column


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

/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-31 16:03:20
 * @ Modified by: Your name
 * @ Modified time: 2019-11-04 15:52:43
 * @ Description:
 */

module twofish(

);

endmodule : twofish


module twofish_stage(

);

endmodule : twofish_stage


module key_schedule(
    input [127:0] key,
    output [31:0] Me [1:0],
    output [31:0] Mo [1:0],
    output [31:0] Si [1:0]
);

    assign Me[0] = key[31:0];
    assign Me[1] = key[95:64];
    assign Mo[0] = key[63:32];
    assign Mo[1] = key[127:96];

    logic [7:0] m_0 [7:0];
    assign m_0[0] = key[7:0];
    assign m_0[1] = key[15:8];
    assign m_0[2] = key[23:16];
    assign m_0[3] = key[31:24];
    assign m_0[4] = key[39:32];
    assign m_0[5] = key[47:40];
    assign m_0[6] = key[55:48];
    assign m_0[7] = key[63:56];
    logic [7:0] m_1 [7:0];
    assign m_1[0] = key[71:64];
    assign m_1[1] = key[79:72];
    assign m_1[2] = key[87:80];
    assign m_1[3] = key[95:88];
    assign m_1[4] = key[103:96];
    assign m_1[5] = key[111:104];
    assign m_1[6] = key[119:112];
    assign m_1[7] = key[127:120];
    logic [7:0] RS [31:0];
    assign RS[0] = 8'h01;
    assign RS[1] = 8'hA4;
    assign RS[2] = 8'h55;
    assign RS[3] = 8'h87;
    assign RS[4] = 8'h5A;
    assign RS[5] = 8'h58;
    assign RS[6] = 8'hDB;
    assign RS[7] = 8'h9E;
    assign RS[8] = 8'hA4;
    assign RS[9] = 8'h56;
    assign RS[10] = 8'h82;
    assign RS[11] = 8'hF3;
    assign RS[12] = 8'h1E;
    assign RS[13] = 8'hC6;
    assign RS[14] = 8'h68;
    assign RS[15] = 8'hE5;
    assign RS[16] = 8'h02;
    assign RS[17] = 8'hA1;
    assign RS[18] = 8'hFC;
    assign RS[19] = 8'hC1;
    assign RS[20] = 8'h47;
    assign RS[21] = 8'hAE;
    assign RS[22] = 8'h3D;
    assign RS[23] = 8'h19;
    assign RS[24] = 8'hA4;
    assign RS[25] = 8'h55;
    assign RS[26] = 8'h87;
    assign RS[27] = 8'h5A;
    assign RS[28] = 8'h58;
    assign RS[29] = 8'hDB;
    assign RS[30] = 8'h9E;
    assign RS[31] = 8'h03;

    wire [7:0] s0 [3:0];
    wire [7:0] s1 [3:0];


    matrix_multiplication #(.N(8),.COL_A(8),.ROW_A(4),.COL_B(1)) m0(
        .a(RS),
        .b(m_0),
        .p(9'h14D),
        .s(s0)
    );
    matrix_multiplication #(.N(8),.COL_A(8),.ROW_A(4),.COL_B(1)) m1(
        .a(RS),
        .b(m_1),
        .p(9'h14D),
        .s(s1)
    );

    assign Si[1] = {s0[3],s0[2],s0[1],s0[0]};
    assign Si[0] = {s1[3],s1[2],s1[1],s1[0]};


endmodule : key_schedule


module h_function(
    input [31:0] X,
    input [31:0] L [1:0],
    output [31:0] Z
);
    
    logic [7:0] MDS [15:0];
    assign MDS[0] = 8'h01;
    assign MDS[1] = 8'hEF;
    assign MDS[2] = 8'h5B;
    assign MDS[3] = 8'h5B;
    assign MDS[4] = 8'h5B;
    assign MDS[5] = 8'hEF;
    assign MDS[6] = 8'hEF;
    assign MDS[7] = 8'h01;
    assign MDS[8] = 8'hEF;
    assign MDS[9] = 8'h5B;
    assign MDS[10] = 8'h01;
    assign MDS[11] = 8'hEF;
    assign MDS[12] = 8'hEF;
    assign MDS[13] = 8'h01;
    assign MDS[14] = 8'hEF;
    assign MDS[15] = 8'h5B;


    logic [31:0] X1;
    logic [31:0] X2;
    logic [31:0] Q0;
    logic [31:0] Q1;
    wire [7:0] Q2 [3:0];
    wire [7:0] y [3:0];
    


    /*step1*/
    q0_transform i00(
        .x(X[7:0]),
        .q0(Q0[7:0])
    );
    q1_transform i01(
        .x(X[15:8]),
        .q1(Q0[15:8])
    );
    q0_transform i02(
        .x(X[23:16]),
        .q0(Q0[23:16])
    );
    q1_transform i03(
        .x(X[31:24]),
        .q1(Q0[31:24])
    );
    galois_adder #(.N(32)) a0(
        .a(L[1]),
        .b(Q0),
        .s(X1)
    );
    /*step2*/
    q0_transform i10(
        .x(X1[7:0]),
        .q0(Q1[7:0])
    );
    q0_transform i11(
        .x(X1[15:8]),
        .q0(Q1[15:8])
    );
    q1_transform i12(
        .x(X1[23:16]),
        .q1(Q1[23:16])
    );
    q1_transform i13(
        .x(X1[31:24]),
        .q1(Q1[31:24])
    );
    galois_adder #(.N(32)) a1(
        .a(L[0]),
        .b(Q1),
        .s(X2)
    );
    /*step3*/
    q1_transform i20(
        .x(X2[7:0]),
        .q1(Q2[0])
    );
    q0_transform i21(
        .x(X2[15:8]),
        .q0(Q2[1])
    );
    q1_transform i22(
        .x(X2[23:16]),
        .q1(Q2[2])
    );
    q0_transform i23(
        .x(X2[31:24]),
        .q0(Q2[3])
    );
    /*Matrix*/
    
    matrix_multiplication #(.N(8),.COL_A(4),.ROW_A(4),.COL_B(1)) m0(
        .a(MDS),
        .b(Q2),
        .p(9'h169),
        .s(y)
    );

    assign Z = {y[3],y[2],y[1],y[0]};
    

endmodule : h_function


module q0_transform(
    input [7:0] x,
    output [7:0] q0
);

    logic [3:0] t0 [15:0];
    logic [3:0] t1 [15:0];
    logic [3:0] t2 [15:0];
    logic [3:0] t3 [15:0];

    assign t0[0] = 4'h8;
    assign t0[1] = 4'h1;
    assign t0[2] = 4'h7;
    assign t0[3] = 4'hD;
    assign t0[4] = 4'h6;
    assign t0[5] = 4'hF;
    assign t0[6] = 4'h3;
    assign t0[7] = 4'h2;
    assign t0[8] = 4'h0;
    assign t0[9] = 4'hB;
    assign t0[10] = 4'h5;
    assign t0[11] = 4'h9;
    assign t0[12] = 4'hE;
    assign t0[13] = 4'hC;
    assign t0[14] = 4'hA;
    assign t0[15] = 4'h4;

    assign t1[0] = 4'hE;
    assign t1[1] = 4'hC;
    assign t1[2] = 4'hB;
    assign t1[3] = 4'h8;
    assign t1[4] = 4'h1;
    assign t1[5] = 4'h2;
    assign t1[6] = 4'h3;
    assign t1[7] = 4'h5;
    assign t1[8] = 4'hF;
    assign t1[9] = 4'h4;
    assign t1[10] = 4'hA;
    assign t1[11] = 4'h6;
    assign t1[12] = 4'h7;
    assign t1[13] = 4'h0;
    assign t1[14] = 4'h9;
    assign t1[15] = 4'hD;

    assign t2[0] = 4'hB;
    assign t2[1] = 4'hA;
    assign t2[2] = 4'h5;
    assign t2[3] = 4'hE;
    assign t2[4] = 4'h6;
    assign t2[5] = 4'hD;
    assign t2[6] = 4'h9;
    assign t2[7] = 4'h0;
    assign t2[8] = 4'hC;
    assign t2[9] = 4'h8;
    assign t2[10] = 4'hF;
    assign t2[11] = 4'h3;
    assign t2[12] = 4'h2;
    assign t2[13] = 4'h4;
    assign t2[14] = 4'h7;
    assign t2[15] = 4'h1;

    assign t3[0] = 4'hD;
    assign t3[1] = 4'h7;
    assign t3[2] = 4'hF;
    assign t3[3] = 4'h4;
    assign t3[4] = 4'h1;
    assign t3[5] = 4'h2;
    assign t3[6] = 4'h6;
    assign t3[7] = 4'hE;
    assign t3[8] = 4'h9;
    assign t3[9] = 4'hB;
    assign t3[10] = 4'h3;
    assign t3[11] = 4'h0;
    assign t3[12] = 4'h8;
    assign t3[13] = 4'h5;
    assign t3[14] = 4'hC;
    assign t3[15] = 4'hA;

    /*
    logic [3:0] a0,b0,a1,b1,a2,b2,a3,b3,a4,b4;
    logic [7:0] y;


    always_comb begin
        a0 = x[7:4];
        b0 = x[3:0];
        a1 = a0 ^ b0;
        b1 = a0 ^ {b0[0],b0[3:1]} ^ {a0[0],3'b000};
        a2 = t0[a1];
        b2 = t1[b1];
        a3 = a2 ^ b2;
        b3 = a2 ^ {b2[0],b2[3:1]} ^ {a2[0],3'b000};
        a4 = t2[a3];
        b4 = t3[b3];
        y = {b4,a4};
    end
    assign q0 = y;
    */
    
    assign q0 = {t3[(t0[(x[7:4] ^ x[3:0])] ^ {t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})][0],t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})][3:1]} ^ {t0[(x[7:4] ^ x[3:0])][0],3'b000})],t2[(t0[(x[7:4] ^ x[3:0])] ^ t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})])]};
    


endmodule : q0_transform


module q1_transform(
    input [7:0] x,
    output [7:0] q1
);
    logic [3:0] t0 [15:0];
    logic [3:0] t1 [15:0];
    logic [3:0] t2 [15:0];
    logic [3:0] t3 [15:0];

    assign t0[0] = 4'h2;
    assign t0[1] = 4'h8;
    assign t0[2] = 4'hB;
    assign t0[3] = 4'hD;
    assign t0[4] = 4'hF;
    assign t0[5] = 4'h7;
    assign t0[6] = 4'h6;
    assign t0[7] = 4'hE;
    assign t0[8] = 4'h3;
    assign t0[9] = 4'h1;
    assign t0[10] = 4'h9;
    assign t0[11] = 4'h4;
    assign t0[12] = 4'h0;
    assign t0[13] = 4'hA;
    assign t0[14] = 4'hC;
    assign t0[15] = 4'h5;

    assign t1[0] = 4'h1;
    assign t1[1] = 4'hE;
    assign t1[2] = 4'h2;
    assign t1[3] = 4'hB;
    assign t1[4] = 4'h4;
    assign t1[5] = 4'hC;
    assign t1[6] = 4'h3;
    assign t1[7] = 4'h7;
    assign t1[8] = 4'h6;
    assign t1[9] = 4'hD;
    assign t1[10] = 4'hA;
    assign t1[11] = 4'h5;
    assign t1[12] = 4'hF;
    assign t1[13] = 4'h9;
    assign t1[14] = 4'h0;
    assign t1[15] = 4'h8;

    assign t2[0] = 4'h4;
    assign t2[1] = 4'hC;
    assign t2[2] = 4'h7;
    assign t2[3] = 4'h5;
    assign t2[4] = 4'h1;
    assign t2[5] = 4'h6;
    assign t2[6] = 4'h9;
    assign t2[7] = 4'hA;
    assign t2[8] = 4'h0;
    assign t2[9] = 4'hE;
    assign t2[10] = 4'hD;
    assign t2[11] = 4'h8;
    assign t2[12] = 4'h2;
    assign t2[13] = 4'hB;
    assign t2[14] = 4'h3;
    assign t2[15] = 4'hF;

    assign t3[0] = 4'hB;
    assign t3[1] = 4'h9;
    assign t3[2] = 4'h5;
    assign t3[3] = 4'h1;
    assign t3[4] = 4'hC;
    assign t3[5] = 4'h3;
    assign t3[6] = 4'hD;
    assign t3[7] = 4'hE;
    assign t3[8] = 4'h6;
    assign t3[9] = 4'h4;
    assign t3[10] = 4'h7;
    assign t3[11] = 4'hF;
    assign t3[12] = 4'h2;
    assign t3[13] = 4'h0;
    assign t3[14] = 4'h8;
    assign t3[15] = 4'hA;

    /*
    logic [3:0] a0,b0,a1,b1,a2,b2,a3,b3,a4,b4;
    logic [7:0] y;


    always_comb begin
        a0 = x[7:4];
        b0 = x[3:0];
        a1 = a0 ^ b0;
        b1 = a0 ^ {b0[0],b0[3:1]} ^ {a0[0],3'b000};
        a2 = t0[a1];
        b2 = t1[b1];
        a3 = a2 ^ b2;
        b3 = a2 ^ {b2[0],b2[3:1]} ^ {a2[0],3'b000};
        a4 = t2[a3];
        b4 = t3[b3];
        y = {b4,a4};
    end
    assign q1 = y;
    */
    
    assign q1 = {t3[(t0[(x[7:4] ^ x[3:0])] ^ {t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})][0],t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})][3:1]} ^ {t0[(x[7:4] ^ x[3:0])][0],3'b000})],t2[(t0[(x[7:4] ^ x[3:0])] ^ t1[(x[7:4] ^ {x[0],x[3:1]} ^ {x[4],3'b000})])]};

    


endmodule : q1_transform
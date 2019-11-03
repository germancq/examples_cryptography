/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-31 16:03:20
 * @ Modified by: Your name
 * @ Modified time: 2019-10-31 16:37:24
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

    logic [7:0] s0 [3:0];
    logic [7:0] s1 [3:0];

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

    assign Si[0] = {s0[3],s0[2],s0[1],s0[0]};
    assign Si[1] = {s1[3],s1[2],s1[1],s1[0]};


endmodule : key_schedule


module h_function(

);




endmodule : h_function


module q0_transform(

);


endmodule : q0_transform


module q1_transform(

);


endmodule : q1_transform
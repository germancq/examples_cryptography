/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-09-30 15:29:16
 * @ Modified by: Your name
 * @ Modified time: 2019-09-30 17:17:00
 * @ Description:
 */



module register(
    input clk,
    input cl,
    input w,
    input [DATA_WIDTH-1:0] din,
    output logic [DATA_WIDTH-1:0] dout
);

parameter DATA_WIDTH = 8;

always_ff @(posedge clk) begin
    if (cl) begin
        dout <= { DATA_WIDTH {1'b0} };
    end
    else if (w) begin
        dout <= din;
    end
end

endmodule : register
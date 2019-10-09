/*
 * @Author: German Cano Quiveu, germancq@gmail.com 
 * @Date: 2019-09-21 22:19:51 
 * @Last Modified by: German Cano Quiveu, germancq@gmail.com
 * @Last Modified time: 2019-09-21 23:16:14
 */
module lookup_table(
    input clk,
    input rst,
    input  [ADDR_WIDTH-1:0] addr,
    output logic [DATA_WIDTH-1:0] data
);

parameter DATA_WIDTH = 32;
parameter ADDR_WIDTH = 5;
parameter FILE_MEM = "/home/germancq/criptografia/examples_cryptography/systemVerilog/fusesoc/orpsoc-cores/systems/trivium_system/rtl/systemVerilog/lookuptable_contents.mem";

logic [DATA_WIDTH-1:0] lookup_table_inst [2**ADDR_WIDTH - 1 :0]; //packed array

initial begin
    $readmemh(FILE_MEM,lookup_table_inst);
end



always_ff @(posedge clk) begin
    if(rst == 1)
        begin
            data <= 32'hFFFFFFFF;
        end    
    else  
        begin
            data <= lookup_table_inst[addr];
        end  
end

endmodule : lookup_table
open_project $::env(HLS_OPTIMIZER_PROJECT)
set_top krnl_KALMAN
add_files $::env(HLS_OPTIMIZER_INPUT_FILE)
open_solution "solution1" -flow_target vivado
set_part {xcu200-fsgd2104-2-e}
create_clock -period 3.33 -name default
config_array_partition -auto_partition_threshold 0 -auto_promotion_threshold 0
config_compile -pipeline_loops 0
csynth_design
export_design -format ip_catalog
exit

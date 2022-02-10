open_project PROJECT_NAME
set_top TOP_LEVEL_FUNCTION
add_files PATH_TO_KERNEL_SOURCE_CODE
open_solution "solution1" -flow_target vivado
set_part {xczu9eg-ffvb1156-2-e}
create_clock -period 3.33 -name default
config_array_partition -auto_partition_threshold 0 -auto_promotion_threshold 0
config_compile -pipeline_loops 0
csynth_design
export_design -format ip_catalog
exit

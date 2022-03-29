# Automatic design space exploration for FPGA kernel acceleration

## Authors
Vassilios Kypriotis - Kakolyris Andreas Kosmas - Ferikoglou Aggelos, Microlab 2022

---
## Description

This project aims to automate the process of producing optimized code for HLS kernels. In order to facilitate this goals there are 2 main tools:
1. A Random Optimizer
1. An Optimizer based on Genetic Algorithms

The output after running each tool is the iteration responsible for the lowest latency  as well as the Pareto Optimal points derived from the resource (DSP, BRAM, LUT, FF) consumption and the latency of the produced code.

---

## Project Architecture

Both optimizers are based on a similar architecture. The tool has been designed with a frontend-backend approach in order to be easily extensible int the future.

### Backend Code

The backend code is the code that interacts and places directives on the source files. The python files responsible for this function are:

1. **modules/annotator.py** -  Extracts loop and array locations from the kernel source code. It also is responsible for placing directives directly onto the code.

1. **modules/generators.py** - Helper functions for creating the pragmas. Each function given the appropriate pragma parameters returns the corresponding string.

1. **modules/ds_explorator.py** - Defines a class that interfaces with the frontend layer. From this class the DSE algorithm guides the creation and placement of pragmas.

### Frontend code

1. **randomizer.py**  - A script for generating a new source file with random directives from plain source

1. **randomDSE.py** - The random algorithm for optimization. Runs many syntheses with random directives in parallel

1. **geneticDSE.py** - The genetic algorithm for optimization. Runs many syntheses in parallel and guides the placement of directives based on the NSGA-II algorithm.

### Synthesis scripts

Tcl scripts that invoke Vitis HLS in order to perform synthesis for the given source files. These are used by the frontend as subprocesses.

1. **tcl_scripts/sample_script_alveo_u200.tcl** - For synthesizing on Alveo
1. **tcl_scripts/sample_script_zcu102.tcl** - For synthesizing on ZCU

---

## Installation

Simply cloning the project and having the appropriate Python modules installed (installation commands provided below) will be enough.

```bash
pip3 install pymoo numpy psutil
```

**IMPORTANT: A valid installation of Vitis HLS is also required**

---
## Optimizing Code

In this section we will discuss how to optimize the code using the two tools. Out of the box we support 

***Note 1***: Each folder named **DSE_EXPLORER_X** contains the synthesis results from source file iterationX.cpp<br>
***Note 2***: The following commands are to be run inside the "tool" folder. In case the user wants to run them in another directory, the paths will have to be modified accordingly.

### Random Optimizer

---

**Step 1** Generate random syntheses:<br><br>

```bash
python3 randomDSE.py randomizer.py <kernel_file> <path_to_tcl_script> <Total_time_limit> <Iteration_timeout_limit> <Threads>
```

 **Step 2** Find iteration with lowest latency:<br><br> 
 ```bash
 python3 best_latency.py <number_of_syntheses>
 ```

 ***Note: Run this command in the directory containing all the DSE_EXPLORER_X folders***

 **Step3 (Optional)** Find pareto optimal points:<br><br> 
 ```bash
 python3 extractor/pareto_points.py <path_to_syntheses_directory> <number_of_syntheses>
 ```

The iteration/source file corresponding to each Pareto optimal point is the last element of each list.

### Genetic Algorithm Optimizer

---

Run genetic algorithm:<br><br>
```bash
python3 geneticDSE.py <path_to_kernel_file> <path_to_tcl_script>
```

Example:
```bash
python3 geneticDSE.py ../kalman_filter_kernel.cpp tcl_scripts/sample_script_alve_u200.tcl
``` 

***Note: Any other execution parameter can only be changed inside the source code***

---

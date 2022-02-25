# Kalman Filter @Alveo U200

**Non-Optimized Version
* Latency : 42.76 ms
* Kernel freq : 300 MHz

**Resource utilization for a single FPGA kernel**

Resource      | Used          | Total         | % Utilization
------------- | ------------- | ------------- | -------------
DSP           | 2             | 2280          | 4
BRAM          | 64            | 1440          | ~0
LUT           | 11966         | 394080        | 3
FF            | 4183          | 788160        | ~0


**Optimized Version

* Latency : 1.500 ms
* Kernel freq : 300 MHz

**Resource utilization for a single FPGA kernel**

Resource      | Used          | Total         | % Utilization
------------- | ------------- | ------------- | -------------
DSP           | 128           | 2280          | 5
BRAM          | 1056          | 1440          | 73
LUT           | 73186         | 394080        | 18
FF            | 58939         | 788160        | 7

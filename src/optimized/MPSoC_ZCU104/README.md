# Kalman Filter @MPSoC ZCU102
**Non-Optimized Version**
* Latency : 45.2 ms
* Kernel freq : 300 MHz

**Resource utilization for a single FPGA kernel**

Resource      | Used          | Total         | % Utilization
------------- | ------------- | ------------- | -------------
DSP           | 2             | 2520          | 0
BRAM          | 578           | 1824          | 31
LUT           | 11931         | 274080        | 0
FF            | 3871          | 548160        | 4


**Optimized Version**

* Latency : 2.81
* Kernel freq : 300 MHz

**Resource utilization for a single FPGA kernel**

Resource      | Used          | Total         | % Utilization
------------- | ------------- | ------------- | -------------
DSP           | 128           | 2520          | 5
BRAM          | 624           | 1824          | 34
LUT           | 46968         | 274080        | 17
FF            | 37549         | 548160        | 6

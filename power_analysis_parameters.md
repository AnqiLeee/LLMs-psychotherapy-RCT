## Power Analysis

We employ G*Power (version: 3.1.9) to precompute the required sample size for the experiment.

The input parameters for calculating the sample size are shown in the following table:

|Input| Parameter|
| :---: | :---: |
| `Test family`|F tests|
|`Statistical test`|ANOVA: Repeated measurements, between factors|
| `Type of power analysis`| A priori: Compute required sample size - given alpha, power, and effect size|
|`Effect size f`|0.10|
|`alpha err prob`|0.05|
|`Power (1-beta err prob)`|0.80|
|`Number of groups`|6|
|`Number of measurements`|10|
|`Corr among rep measurements`|0.5|




# sps-cordic
CORDIC Parameter search for Signal Processing Systems course in OU

Contains 2 and 3 value CORDIC in their respective files.
This will create output like:

```
CORDIC:
|I |  Z (deg)  | d| atan(2^-i) | Z+1 (deg) |    xA     |    yA     |     x     |     y     |
|0 |  +61.00   |+1|   +45.00   |  +16.00   |   +2.50   |   -7.00   |   +2.50   |   -7.00   |
|1 |  +16.00   |+1|   +26.57   |  -10.57   |   +6.00   |   -5.75   |   +4.24   |   -4.07   |
|2 |  -10.57   |-1|   +14.04   |   +3.47   |   +4.56   |   -7.25   |   +2.89   |   -4.59   |
|3 |   +3.47   |+0|   +7.13    |   +3.47   |   +4.56   |   -7.25   |   +2.80   |   -4.45   |
|4 |   +3.47   |+1|   +3.58    |   -0.11   |   +5.02   |   -6.96   |   +3.05   |   -4.24   |
|5 |   -0.11   |  |            |           |   +5.02   |   -6.96   |   +3.05   |   -4.24   |

      Result   [ Reference ] (  |Delta|  )
x:  +3.05368   [ +3.06362  ] (  0.00994  )
y:  -4.24043   [ -4.27074  ] (  0.03031  )
CORDIC Gain: 1.642484
Effective stages: 5

Residual angle error (deg): 0.10514 < 0.20
```

This is a course homework return and not an actual module. However, feel free to use it if it is useful for something.

#!/bin/python
import Adafruit_BBIO.ADC as ADC
ADC.setup()

AIN0 = "P9_39"
AIN1 = "P9_40"

value = ADC.read(AIN1)
value = ADC.read(AIN1)*18

print(value)
value = ADC.read_raw(AIN1)
print(value)

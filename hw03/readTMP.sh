#!/bin/bash
#reads tmp sensor @0x48 on i2c-2
temp=`i2cget -y 2 0x48 0x00`
temp2=$(($temp * 9 / 5 + 32))
echo "Temp sensor 1: "$temp2
temp=`i2cget -y 2 0x4a 0x00`
temp2=$(($temp * 9 / 5 + 32))
echo "Temp sensor 2: "$temp2

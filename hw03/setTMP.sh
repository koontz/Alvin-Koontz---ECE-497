#!/bin/bash
# set lower alert to 21C or 70F
i2cset -y 2 0x48 0x02 0x18
# this basically garentees alert goes off when heat is applied 
i2cset -y 2 0x48 0x03 0x18

#repeat for second sensor
i2cset -y 2 0x4a 0x02 0x15
i2cset -y 2 0x4a 0x03 0x15


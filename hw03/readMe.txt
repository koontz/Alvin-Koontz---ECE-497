homework 3

I am unable to get my tmp006 sensor to respond on the i2c bus, it doesnt show up in i2cdetect. The wiring is right so I'm assuming something else has gone wrong
Becuase of this I don't use in any part of my homework

For the tmp101 part of the homework I used pins p9_19 and p9_20 for i2c and pin 13 for the alert
On my board I found the i2c devicies on i2c-2 so thats what all my programs used.
0x48 and 0x4a are the addresses for my tmp sensors

readTMP.sh is a shell file that reads the tempeture of each

setTMP.sh is a shell file that sets the alert tempeture of each

tmp101Reader.py is the program that waits for the alert pin before it reads the tempature sensors

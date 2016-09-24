The readme for homework 4

1) Boneserver.js is like anyother server, it binds it self to a port (in this case 8080) and 
then anyone who can accsess(ie send and recive messages from) that port. When a web browser 
accesses the port the server provides it with the various files it needs to create a graphic 
interface (html, javascript and sometime css files). So the matrixLED.js file is sent to the 
browser where it can be running on the same machine or a complettly different machine. From 
there matrixLED.js can only communicate with the boneServer.js through the specified port, 
the method that is used here to communicate is socket.io which creates a constant connection 
between the server and client. So when the client sends emits the message 'matrix' on this 
connection the server recivces this as a kind of 'get' request where it runs the anonomyous 
function that gets the current state of the led matrix, and then rebrodcasts it on the 
connection by saying " 'matrix' + data_of_matrix ". Now on the client side they get the 
matrix response and run the function that updates the html classes to visually update the 
user to the current state of the led. 

2) When an led is click on in the browser, the table entry has an onclick function that is 
called with the location of the led, the onclick function uses socket.io to communicate with 
the server and tell it which led has been clicked and to set that led to on 

3)the 'on' class colors the led green with the background color and provides a border

4)If I was using boneserver.js a second i2cset emit with io socket would work to set the 
green and the red leds to the correct color. The structure for keeping track of leds would 
have to be changed to have a red and green section. Also the get led data would have to 
redone to include the red from updating from display.

5)Just for funsies I wrote my own server on the bone, just run './server' it is set to use 
port 8090. The server uses python methods for all the control

The following packages are needed to run the server

apt-get install python-smbus
pip install --upgrade Flask
pip install python-socketio
pip install eventlet

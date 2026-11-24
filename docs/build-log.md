#10/27/26
#want square size to be double diameter of pieces to make room for movement. With normal 3cm diameter chess pieces board area will be bigger than any xy gantry can handle. Might have to 3d print chess pieces? Planning on doing a prototype test with hall sensor and magnets. 

#11/7/26
#bought a multimeter, breadboard, magnets, and some sensors to do my first test. I want to place the sensor under a square to detect when a piece is above it. Also if swap the pole of the magnet i can also detect what color piece is above the sensor. First test was with a usb adapter plugged into my computer to provide power for the sensor. I used the multimeter to check and see that the sensor were good and did respond well to the magnet. I tried to simulate the conditions of the board by placing a piece of cardboard between the magnet and sensor but the difference in reading from the sensor's base output was too low. I think i will buy bigger magnets to fix this problem.

#11/8/26
#i am starting to realize that i need a source of adjustable power for testing. Buying a powersupply on amazon is too expensive so i plan on converting an old powersupply from a comupter into one. 

#11/18/26
#nearly electrocuted myself by testing powersupply with cover off. We will never make that mistake again. Also arced that powersupply so it no longer produces 12Vs. 

#11/22/26
#found a new power supply from another pc. Did not make the same mistake as last time. I tested it by connecting the green turn on wire to a black ground wire. This lets it turn on without having to turn on the computer. The fan turns on and all the wire match the voltage they should be producing. I did some research and bought an ATX board from Aliexpress. This one is much cheaper than all of my previous purchases. unfortunately, the shipping is a little slow. It will come by december.

#11/23/26
#I finally started writing some code for the raspberry pi i bought. I looked at some youtube tutorials of other people lighting up LEDS and adapted their circuits to my sensor. Just had to add an extra jumper for the output signal.Now i can see the change in voltage of the sensor without having to put a multimeter on it! The raspberry pi i am using only has 3 analog inputs. I need to connect 64 sensors. Will figure out later. 
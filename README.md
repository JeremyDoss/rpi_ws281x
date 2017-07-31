# RaspberryPi2 B+ Animations Library

A library of animations created using the neopixel library forked from <a href="https://github.com/richardghirst/rpi_ws281x">here.</a>

## Background

I wanted to create a library of custom animations to run on my raspberry pi 2 B+.
The idea was to mount the Pi in my car along with the LEDs so that I could get 
some cool animations running under the hood scoop on my Subaru WRX. I figured it 
would be cooler than just throwing underglow on it. In the end I would like to hook 
it up to be bluetooth controlled from the vehicle. It should start automatically 
with ignition power.


## Hardware

This build is currently tested and working on a strip containing 144 WS2812b LEDs per meter.
It should work for all type WS281X LEDs. These strips run off of 5v power and can be considered 
to draw a MAXIMUM of 60ma per pixel. I had no trouble running 144 using a 5v 2a phone charger at 
reduced brightness.

## Building

* Install Scons (on raspbian, apt-get install scons).
* Make sure to adjust the parameters in main.c to suit your hardare.
  * Signal rate (400kHz to 800kHz).  Default 800kHz.
  * ledstring.invert=1 if using a inverting level shifter.
  * Width and height of LED matrix (height=1 for LED string).
* Type 'scons' from inside the src directory.
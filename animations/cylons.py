# WS2812b 144 led/m strip Cylon/Nightrider example
# Author: Jeremy Doss (jeremy.doss.cs@gmail.com)
#
# Partial port of the Arduino NeoPixel library strandtest example.
# Retains colorWipe and rainbowCycle animations and adds a sweeping 
# Cylon/Nightrider eye animation for running on a strip of NeoPixels.

######## TODO ########
# Refactor and pull out repetitive code from cylonSweep function
# Normalize cycle_ms parameters to represent time to complete entire cycle (L<=>R)
# Render eye position based on system clock and not CPU clock
# Thread library and run as daemon in background
# Make rainbow cylon sweep pattern with static colors
# Make rainbow cylon sweep pattern with shifting colors
# Add bluetooth connectivity and control LEDs (for control once mounted in the car)
######################

import time
import math

from neopixel import *

# LED strip configuration:
LED_COUNT      = 144
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 64
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
	time.sleep(5)

def rainbowCycle(strip, wait_ms=1, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/10000.0)

def renderCylonEye(strip, position, spread):
	ledCount = strip.numPixels()
	for j in range(ledCount):
		offset = abs(position - j)
		if offset == 0:
			strip.setPixelColor(j, Color(255, 0, 0))
		elif offset <= spread:
			# Implements 2^n curve for normalizing brightness relative to cylon eye position
			# Brightness is lower bound to 2^3 and upper bound by 2^8
			power = ((spread - offset + 1) / float(spread)) * 5
			level = math.pow(2, power + 3) - 1
			strip.setPixelColor(j, Color(int(level), 0, 0))
		else:
			strip.setPixelColor(j, Color(0, 0, 0))

def cylonSweep(strip, cycle_ms=1, iterations=10, spread=2):
	ledCount = strip.numPixels()
	for k in range(iterations):
		print("Iteration", k)
		for i in range(ledCount * 2):
			slow = 0
			slowFactor = cycle_ms
			# Sweep left => right
			if i < ledCount:
				eyePosition = i
				loffset = eyePosition
				roffset = (ledCount - 1) - eyePosition
				renderCylonEye(strip, eyePosition, spread)
				if (loffset < float(ledCount)/4):
					slow = 1
					slowFactor = slowFactor * ((float(ledCount)/4) - loffset)
				elif (roffset < float(ledCount)/4):
					slow = 1
					slowFactor = slowFactor * ((float(ledCount)/4) - roffset)
			# Sweep right => left
			else:
				eyePosition = 2 * ledCount - (i + 1)
				loffset = eyePosition
				roffset = (ledCount - 1) - eyePosition
				renderCylonEye(strip, eyePosition, spread)
				if (loffset <= float(ledCount)/4):
					slow = 1
					slowFactor = slowFactor * ((float(ledCount)/4) - loffset)
				elif (roffset <= float(ledCount)/4):
					slow = 1
					slowFactor = slowFactor * ((float(ledCount)/4) - roffset)
			strip.show()
			time.sleep(cycle_ms/10000.0)

			if (slow):
				time.sleep(slowFactor/20000.0)
				slow = 0
				slowFactor = cycle_ms

if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print 'Press Ctrl-C to quit.'
	while True:
		cylonSweep(strip, 1, 8, 32)
		colorWipe(strip, Color(0, 0, 0), 1)
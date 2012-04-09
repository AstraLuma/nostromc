"""
Just a bunch of constants and utilities for the Nostromo.
"""
from pyinput import uinput

LEDS = [uinput.LED_NUML, uinput.LED_CAPSL, uinput.LED_SCROLLL]

def led_pick(nos, led):
	"""
	Lights a single LED (from 0 - 2) and clears the others.
	
	nos must be opened write-only.
	"""
	s = [0,0,0]
	if led is not None:
		s[led] = 1
	ie = uinput.input_event()
	ie.type = uinput.EV_LED
	for i,v in enumerate(s):
		ie.code = LEDS[i]
		ie.value = v
		nos.write(ie)

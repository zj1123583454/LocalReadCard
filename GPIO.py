try:
	import RPi.GPIO
	import time
except ImportError as e:
	print "Import Error",e
	exit()
class GPIO(object):
	def __init__(self):
		RPi.GPIO.setmode(RPi.GPIO.BOARD)
		RPi.GPIO.setup(12,RPi.GPIO.OUT)
		RPi.GPIO.setup(15,RPi.GPIO.OUT)
		RPi.GPIO.setup(16,RPi.GPIO.OUT)
	def LockOpen(self):
		RPi.GPIO.output(15,RPi.GPIO.LOW)
		RPi.GPIO.output(16,RPi.GPIO.HIGH)
		time.sleep(3)
		RPi.GPIO.output(15,RPi.GPIO.LOW)
		RPi.GPIO.output(16,RPi.GPIO.LOW)
		time.sleep(1)
		RPi.GPIO.output(15,RPi.GPIO.HIGH)
		RPi.GPIO.output(16,RPi.GPIO.LOW)
		time.sleep(3)
		RPi.GPIO.output(15,RPi.GPIO.LOW)
		RPi.GPIO.output(16,RPi.GPIO.LOW)
	def BuzzingOpen(self):
		RPi.GPIO.output(12,RPi.GPIO.HIGH)
		time.sleep(0.5)
		RPi.GPIO.output(12,RPi.GPIO.LOW)

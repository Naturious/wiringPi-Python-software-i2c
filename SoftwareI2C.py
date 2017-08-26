import RPi.GPIO as GPIO
import os
def delayMicroseconds(duration):
	time1 = int(os.popen("expr `date +%s%N` / 1000").read()[7:])
	while(True):
		if(int(os.popen("expr `date +%s%N` / 1000").read()[7:]) - time1) >= duration:
			break
class SoftwareI2C:
	
	self.I2C_READ = 1
	self.I2C_WRITE = 0
	self.I2C_ACK = 0
	self.I2C_NACK = 1

	self.I2C_FREQ = 100000 #I2C clock max frequency 100kHz
	self.I2C_HALFPERIOD = (1e6/self.I2C_FREQ)/2
	def __init__(self,scl,sda):
		GPIO.setmode(GPIO.BOARD)
		self.scl = scl
		self.sda = sda

		GPIO.setup(self.scl,GPIO.IN,pull_up_down = GPIO.PUD_UP)
		GPIO.setup(self.sda,GPIO.IN,pull_up_down = GPIO.PUD_UP)

		self.reset()

	def pull(self,pin):
		"""Drives the line to level LOW"""
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,0)
		delayMicroseconds(self.I2C_HALFPERIOD)

	def release(self,pin):
		"""Releases the line and returns line status"""
		GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		delayMicroseconds(self.I2C_HALFPERIOD)
		return GPIO.input(pin)

	def release_wait(self,pin):
		"""In case of clock stretching or busy bus we must wait"""
		GPIO.setup(pin,GPIO.IN,pull_up_down = GPIO.PUD_UP)
		delayMicroseconds(self.I2C_HALFPERIOD)
		while(not(GPIO.input(pin)):
			delayMicroseconds(100)
		delayMicroseconds(self.I2C_HALFPERIOD)

	def start(self):
		"""Pull SDA while SCL is up
		Best practice is to ensure the bus is not busy before start"""
		if(not(self.release(self.sda))
			self.reset()
		self.release_wait(self.scl)

		self.pull(self.sda)
		self.pull(self.scl)		

	def stop(self):
		"""Release SDA while SCL is up"""
		self.release_wait(self.scl)
		if(not(self.release(self.sda))):
			self.reset()

	def reset(self):
		"""Reset bus sequence"""
		self.release(self.sda)
		while True:
			for i in range(9):
				self.pull(self.scl)
				self.release(self.scl)
			if(not(GPIO.input(self.sda))):
				break

		self.pull(self.scl)
		self.pull(self.sda)

		self.stop()

	def send_bit(self, bit):
		"""Sends 0 or 1: 
		Clock down, send bit, clock up, wait, clock down again 
		In clock stretching, slave holds the clock line down in order
		to force master to wait before send more data """
		if(bit)
			self.release(self.sda)
		else:
			self.pull(self.sda)

		self.release_wait(self.scl)
		self.pull(self.scl)

		self.pull(self.sda)

	def read_bit(self):
		"""Reads a bit from sda"""
		self.release(self.sda)
		self.release_wait(self.scl)
		s = GPIO.input(self.sda)
		self.pull(self.scl)
		self.pull(self.sda)
		return s

	def send_byte(self, byte):
		"""Sends 8 bits in a row, MSB first and reads ACK.
		Returns I2C_ACK if device ack'ed"""
		for i in range(8):
			self.send_bit(byte & 0x80)
			byte = byte << 1

		self.read_bit()

	def read_byte(self):
		"""Reads a byte, MSB first"""
		byte = 0x00
		for i in range(8):
			byte = (byte << 1)| self.read_bit()

		return byte
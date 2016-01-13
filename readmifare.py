# Wait for the right MiFare card, light an LED, and exit
#
# Based on the readmifare.py script, with license as follows
# Example of detecting and reading a block from a MiFare NFC card.
# Author: Tony DiCola
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import binascii
import sys
import serial
from time import sleep

import Adafruit_PN532 as PN532
import RPi.GPIO as GPIO

import gsm_test as GSM

GPIO.setmode(GPIO.BCM)

# Setup how the PN532 is connected to the Raspbery Pi
# It is recommended to use a software SPI connection with 4 digital GPIO pins.
CS = 18
MOSI = 23
MISO = 24
SCLK = 25

# Set up how the LED is connected
LED = 17
GPIO.setup(LED, GPIO.OUT)

# Key used to power GSM module on/off
GSM_KEY = 22
GPIO.setup(GSM_KEY, GPIO.OUT)
GPIO.output(GSM_KEY, 0)

# Set up serial port
gsm = GSM.gsm_init()

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()

# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

# Main loop to detect cards and read a block.
print 'Waiting for MiFare card...'
while True:
    # Check if a card is available to read.
    uid = pn532.read_passive_target()
    # Try again if no card is available.
    if uid is None:
        continue

    if binascii.hexlify(uid) == "0d345b95":
        GPIO.output(LED, True)  # Turn LED on
        sleep(1)
        GPIO.output(LED, False) # Turn LED on

        GSM.gsm_send_sms(gsm, 14047961224, "You have mail")

        sys.exit(0)  # Exit the program


# Set pin low for 2 seconds to toggle power
def gsm_onoff():
    GPIO.output(GSM_KEY, 0)
    sleep(2)
    GPIO.output(GSM_KEY, 1)

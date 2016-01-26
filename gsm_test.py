#!/usr/bin/env python

import serial
from time import sleep


# I don't know which of the sleep() commands are actually needed.

def gsm_init():
    """Set up serial connection to GSM module.
    """

    print("Initialising Modem...")
    serialport = serial.Serial("/dev/ttyAMA0", 115200, timeout=30)

    # The module sets the baudrate automatically based on the first message.
    serialport.write("AT\n")
    print(serialport.readline().strip())
    print(serialport.readline().strip())

    return serialport


# This really should check that the network is connected before sending
def gsm_send_sms(port, phone_number, message):
    """Sends MESSAGE to PHONE_NUMBER using gsm module at PORT

PHONE_NUMBER has no special formatting (10 digits).
    """

    print("Sending SMS")
    serialport = port

    # Sets GSM to "Text-Mode"
    serialport.write("AT+CMGF=1\n")
    print(serialport.readline().strip())
    print(serialport.readline().strip())

    # Start of an SMS cmd
    sms_cmd = 'AT+CMGS="{}"\n'.format(phone_number)
    # ASCII ctrl+z signals the end of the text
    sms_cmd += "{}\x1A".format(message)
    serialport.write(sms_cmd)

    sleep(30)    # Sometimes takes a while to send
    print(serialport.readline().strip())
    print(serialport.readline().strip())
    print(serialport.readline().strip())
    print(serialport.readline().strip())
    print(serialport.readline().strip())


def main():
    s = gsm_init()

    # Spam Charles with a text
    gsm_send_sms(s, 18433033157, "Hi")

if __name__ == '__main__':
    main()

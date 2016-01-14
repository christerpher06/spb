#!/usr/bin/env python

import serial
from time import sleep


# I don't know which of the sleep() commands are actually needed.

def gsm_init():
    """Set up serial connection to GSM module.
    """

    print("Initialising Modem...")
    serialport = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

    # The module sets the baudrate automatically based on the first message.
    serialport.write("AT\r\n")
    serialport.readlines()

    serialport.write("ATE0\r\n")
    serialport.readlines()

    return serialport


# This really should check that the network is connected before sending
def gsm_send_sms(port, phone_number, message):
    """Sends MESSAGE to PHONE_NUMBER using gsm module at PORT

PHONE_NUMBER has no special formatting (10 digits).
    """

    print("Sending SMS")
    serialport = port

    # Sets GSM to "Text-Mode"
    serialport.write("AT+CMGF=1\r\n")
    response = serialport.readlines(None)
    sleep(1)
    print(response)

    # Start of an SMS cmd
    sms_cmd = 'AT+CMGS="{}"\r\n'.format(phone_number)
    #print(sms_cmd)
    serialport.write(sms_cmd)
    response = serialport.readlines(None)
    print(response)
    sleep(1)

    # Append the given message
    msg_cmd = "{}\r\n".format(message)
    print(msg_cmd)
    serialport.write(msg_cmd)

    # ASCII ctrl+z signals the end of the text
    serialport.write("\x1A")
    sleep(30)    # Sometimes takes a while to send
    response = serialport.readlines(None)
    print(response)


def main():
    s = gsm_init()

    # Spam Charles with a text
    gsm_send_sms(s, 18433033157, "Hi")

if __name__ == '__main__':
    main()

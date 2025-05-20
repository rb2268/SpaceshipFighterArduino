# Riley Becker
# 5/18/25
# Purpose: Uploads python code to arduino through pyserial, then uses Arduino
# interface to transmit these commands as digital input to two LEDs

# First import Pyserial: pip install pyserial

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

#Import the port attatched to either IOUSBHOSTDEVICE (not wifi or bluetooth 
# or n/a)
#Example—type: "usbmodem142301" for "/dev/cu.usbmodem142301 - IOUSBHostDevice"
portName = input("Select ports for Arduino # ")
use = ""
for i in range(len(portsList)):
    if portsList[i].startswith("/dev/cu." + str(portName)):
        use = "/dev/cu." + str(portName)
        print(use)
try:
    serialInst.baudRate = 9600
    serialInst.port = use
    serialInst.open()
except serial.SerialException as e:
    print(f"Failed to open board at serial port {e}")
    exit()

#Read in values from the serial
def readSerial():
    if serialInst.in_waiting:
        packet = serialInst.readline()
        print(packet.decode('utf'))
    return

def writeSerial():
    command = input("Arduino Command (ON/OFF/exit:) ")
    serialInst.write(command.encode('utf-8'))
    if(command == "exit"):
        command = "OFF"
        serialInst.write(command.encode('utf-8'))
        exit()

while (True): #Query loop
    #Cannot have both readSerial and writeSerial at the same time
    readSerial()
    # writeSerial()
    # "ON" and "OFF" work automatically, no need to add to the query

    
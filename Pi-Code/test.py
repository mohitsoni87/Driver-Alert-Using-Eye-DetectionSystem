import RPi.GPIO as GPIO
import socket
GPIO.setmode(GPIO.BCM)
s = socket.socket()
pin = 17
GPIO.setup(pin, GPIO.OUT)
# Define the port on which you want to connect

IP = '192.168.43.226'
port = 4444

# connect to the server on local computer
s.connect((IP, port))
while 1:
    var = (s.recv(1024).decode())
    if(var == '1'):
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

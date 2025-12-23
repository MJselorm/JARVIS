import serial # type: ignore
import time

class ArduinoController:
    def __init__(self, port='COM6', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None

    def connect(self):
        if self.arduino is None or not self.arduino.is_open:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            print("Arduino connected")

    def light_on(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(b'1')

    def light_off(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(b'0')

    def close(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Arduino disconnected")

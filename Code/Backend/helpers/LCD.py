import RPi.GPIO as GPIO
import time
from RPi import GPIO
from subprocess import check_output





class LCD:
    def __init__(self, E=20, RS=21, DB0=16, DB1=12, DB2=25, DB3=24, DB4=23, DB5=26, DB6=19, DB7=13):
        self.E = E
        self.RS = RS
        self.DB0 = DB0
        self.DB1 = DB1
        self.DB2 = DB2
        self.DB3 = DB3
        self.DB4 = DB4
        self.DB5 = DB5
        self.DB6 = DB6
        self.DB7 = DB7
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(E, GPIO.OUT)
        GPIO.setup(RS, GPIO.OUT)

    @staticmethod
    def decode(a):
        string_a = a.decode(encoding='utf-8')
        return string_a

    def _initList(self):
        global bits
        bits = [16, 12, 25, 24, 23, 26, 19, 13]

    def _initGPIO(self):
        for pin in bits:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.E, GPIO.HIGH)
        global length
        length = 0

    def _init_LCD(self):
        self.send_instruction(0x38)  # function set
        self.send_instruction(0x0F)  # display on/of
        self.send_instruction(0x01)  # clear display or cursor home

    def send_instruction(self, value):
        GPIO.output(self.RS, GPIO.LOW)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.E, GPIO.HIGH)
        time.sleep(0.01)

    def set_data_bits(self, value):
        mask = 0b00000001
        for index in range(0, 8):
            pin = bits[index]

            if value & mask:
                GPIO.output(pin, GPIO.HIGH)

            else:
                GPIO.output(pin, GPIO.LOW)

            mask = mask << 1

    def send_character(self, value):
        GPIO.output(self.RS, GPIO.HIGH)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.E, GPIO.HIGH)
        time.sleep(0.01)

    def write_message(self, message):
        global length
        for letter in message:
            self.send_character(ord(letter))
            length += 1
            if length == 16:
                self.send_instruction(0x80 | 0x40)

    def second_row(self):
        self.send_instruction(0x80 | 0x40)

    def first_row(self):
        self.send_instruction(0x80 | 0x00)

    def clear_display(self):
        self.send_instruction(0x01)

    def display_on_off(self, on):
        if on:
            self.send_instruction(0xC)
        else:
            self.send_instruction(0x8)

    def options(self):
        cursor = input("Cursor aan/uit: ")
        blink = input("Flikkeren van blokje aan/uit: ")

        if cursor == "aan":
            cursor = 0x02
        if cursor == "uit":
            cursor = 0x00

        if blink == "aan":
            blink = 0x01
        if blink == "uit":
            blink = 0x00

        ops = 0xC | cursor | blink
        self.send_instruction(ops)

    def showIP(self):       
        ips = check_output(['hostname', '--all-ip-addresses'])
        ip = LCD.decode(ips)
        loc = ip.find(" ")
        print(ip[0:loc])
        self.first_row()
        self.write_message(f"{ip[0:loc]}")

    def setup(self, first_message):
        self._initList()
        self._initGPIO()
        self._init_LCD()
        self.first_row()
        self.write_message(f"{first_message}")

#!/usr/bin/env python
# encoding: utf-8

# A simple LCD1602 display program
# By https://github.com/reed-chan

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Pin number
RS = 1
RW = 2
E = 3
DB7 = 4
DB6 = 5
DB5 = 6
DB4 = 7
DB3 = 8
DB2 = 9
DB1 = 10
DB0 = 11
#Display info
ROW = 2
COLUMN = 16
ROW1_ADRESS = 0x80
ROW2_ADRESS = 0xC0
E_PAUSE = 0.01
#Function 
TWO_ROW_8BIT_5X7 = 0x38
TWO_ROW_8BIT_5X10 = 0x3c
#Entry mode
LEFT_TO_RIGHT = 0x06
#Cursor display
OPEN_CURSOR = 0x0f
CLOSE_CURSOR = 0x0c
#Clear display
CLEAR_DISPLAY = 0x01

#Initializing
def lcd_inint():
	print('initializing')
	GPIO.setup([RS,RW,E,DB7,DB6,DB5,DB4,DB3,DB2,DB1,DB0], GPIO.OUT, initial=False)
	write_comd(TWO_ROW_8BIT_5X7)
	write_comd(LEFT_TO_RIGHT)
	write_comd(CLOSE_CURSOR)
	write_comd(CLEAR_DISPLAY)
#Write command
def write_comd(comd_data):
	GPIO.output(RS, False)
	GPIO.output(RW, False)
	GPIO.output(E, False)
	comd(comd_data)
	time.sleep(E_PAUSE)
	GPIO.output(E, True)
	time.sleep(E_PAUSE)
	GPIO.output(E, False)
#Write data
def write_data(comd_data):
	GPIO.output(RS, True)
	GPIO.output(RW, False)
	GPIO.output(E, False)
	comd(comd_data)
	time.sleep(E_PAUSE)
	GPIO.output(E, True)
	time.sleep(E_PAUSE)
	GPIO.output(E, False)
#Read busy flag
def is_busy():
	return False
#Bit calculate
def comd(comd_data):				
	GPIO.output([DB7,DB6,DB5,DB4,DB3,DB2,DB1,DB0], False)
	if (comd_data&0x80):
		GPIO.output(DB7, True)
	if (comd_data&0x40):
		GPIO.output(DB6, True)        
	if (comd_data&0x20):
		GPIO.output(DB5, True)
	if (comd_data&0x10):
		GPIO.output(DB4, True)                
	if (comd_data&0x08):
		GPIO.output(DB3, True)
	if (comd_data&0x04):
		GPIO.output(DB2, True)        
	if (comd_data&0x02):
		GPIO.output(DB1, True)
	if (comd_data&0x01):
		GPIO.output(DB0, True)                

#Display String
def test_display(test_text):
	write_comd(CLEAR_DISPLAY)
	i = 0
	for letter in test_text:
		if(i==32):
			i=0
		if(i<16):
			write_comd(ROW1_ADRESS+i)
			write_data(ord(letter))
		else:
			write_comd(ROW2_ADRESS+i-16)
			write_data(ord(letter))
		i = i + 1

if __name__ == '__main__':
	lcd_inint()
	print("Input :q to stop")
	while True:
		input_str = input()
		if(input_str == ":q"):
			break
		test_display(input_str)
	GPIO.cleanup()
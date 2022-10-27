import serial
import time

port = serial.Serial('COM4', 9600)

time.sleep(1)

res = []

res.append(port.readline())

numbers = []

for i, string in enumerate(res):
    for word in string.split():
        if word.isdigit():
            numbers.append(int(word))

thisExp.addData('heart_rate', numbers)

port.close()

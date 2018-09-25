import time
import machine


pin = machine.Pin(16, machine.Pin.OUT)

while True:
    pin.value(1)
    time.sleep(2)
    pin.value(0)
    time.sleep(2)

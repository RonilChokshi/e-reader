from machine import Pin
import time
button = Pin(10, Pin.IN, Pin.PULL_UP)
led = Pin("LED",Pin.OUT)
while True:
    if button.value() == 0:
        led.on()
        print("Button pressed!")
    else:
        led.off()
        print("Button released!")
    time.sleep(0.2)
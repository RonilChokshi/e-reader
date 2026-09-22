from machine import Pin
import time

button = Pin(10, Pin.IN, Pin.PULL_UP)
led = Pin("LED",Pin.OUT)

last_button_state = 1

while True:         #Testing button toggle

    current_button_state = button.value()

    if last_button_state == 1 and current_button_state == 0:

        led.value(not led.value())
        print("Button pressed!")

    last_button_state = current_button_state

    time.sleep(0.02)

'''Testing physical buttons: while True:
    if button.value() == 0:
        led.on()
        print("Button pressed!")
    else:
        led.off()
        print("Button released!")
    time.sleep(0.2)'''
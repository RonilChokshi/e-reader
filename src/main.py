from machine import Pin
import time

button_1 = Pin(10, Pin.IN, Pin.PULL_UP)
button_2 = Pin(6, Pin.IN, Pin.PULL_UP)
led = Pin("LED",Pin.OUT)

last_button1_state = 1
last_button2_state = 1

while True:         #Testing button toggle

    current_button1_state = button_1.value()
    current_button2_state = button_2.value()

    if last_button1_state == 1 and current_button1_state == 0:
        led.value(1)
        print("Button 1 pressed!")
    last_button1_state = current_button1_state

    if last_button2_state == 1 and current_button2_state == 0:
        led.value(0)
        print("Button 2 pressed!")
    last_button2_state = current_button2_state

    time.sleep(0.02)

'''Testing physical buttons: while True:
    if button.value() == 0:
        led.on()
        print("Button pressed!")
    else:
        led.off()
        print("Button released!")
    time.sleep(0.2)'''
from machine import Pin, SPI
import time

spi = SPI(
    0,
    baudrate=10_000_000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(0)
)

cs = Pin(1, Pin.OUT)
cs.value(1)

print(spi)

cs.value(0)

spi.write(b'\xAA')

cs.value(1)

print("SPI transaction complete!")

'''button_1 = Pin(10, Pin.IN, Pin.PULL_UP)  practicing time.ticks_ms()
button_2 = Pin(6, Pin.IN, Pin.PULL_UP)
led = Pin("LED",Pin.OUT)

last_button1_state = 1
last_button2_state = 1

previous_time = time.ticks_ms()
while True:
    led.value(0)
    current_time = time.ticks_ms()
    passed = time.ticks_diff(current_time,previous_time)
    if passed >= 1000:
        led.value(1)
        print("1 second has passed!")
        previous_time = current_time'''

'''while True:         #Testing 2 or 1 button toggle

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

    time.sleep(0.02)'''

'''Testing physical buttons: while True:
    if button.value() == 0:
        led.on()
        print("Button pressed!")
    else:
        led.off()
        print("Button released!")
    time.sleep(0.2)'''
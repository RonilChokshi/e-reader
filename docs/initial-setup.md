# Initial Setup

This document records the initial setup of my DIY e-reader project.

The goal of this project is to build a custom e-reader using a
Raspberry Pi Pico 2 W, an e-paper display, physical buttons,
microSD storage, and eventually Wi-Fi and a battery.

I am documenting the project in detail, including small setup
steps, things I learn, mistakes, problems, and solutions.

---

## 1. Development Environment

### 1.1 GitHub

A GitHub repository was created for this project:

`RonilChokshi/e-reader`

GitHub will be used to store the project online and keep a history
of the project's development.

### 1.2 Visual Studio Code

Visual Studio Code is being used as the main development
environment for the project.

### 1.3 Git

Git is being used to track changes to the project.

The local project folder is connected to the GitHub repository.

---

## 2. Raspberry Pi Pico 2 W

The main microcontroller for the e-reader is a Raspberry Pi Pico 2 W.

The Pico 2 W will eventually be connected to:

- An e-paper display
- Physical buttons
- A microSD card
- Wi-Fi
- A battery

The project is being developed incrementally, starting with getting
the Pico working before connecting the other hardware.

---

## 3. Connecting the Pico to the PC

I connected the Raspberry Pi Pico 2 W to my PC using the official
Raspberry Pi USB cable.

At this stage, the Pico was simply sitting on my desk and was not
connected to the breadboard.

---

## 4. BOOTSEL Mode

### 4.1 What is BOOTSEL?

The Pico has a button labelled `BOOTSEL`.

BOOTSEL is used to put the Pico into its USB bootloader mode.
In this mode, the Pico can appear as a USB storage device, allowing
firmware such as MicroPython to be installed.

### 4.2 Entering BOOTSEL Mode

To enter BOOTSEL mode:

1. The Pico was disconnected from USB.
2. The `BOOTSEL` button was pressed and held.
3. While holding the button, the Pico was connected to the PC using
   the USB cable.
4. The button was then released.

The Pico appeared on the PC as a removable drive named `RP2350`.

### 4.3 Why is the drive called `RP2350`?

The RP2350 is the microcontroller used by the Pico 2 W.

The Pico 2/Pico 2 W uses `RP2350` as the name of its USB mass-storage
bootloader drive.

This was initially confusing because the original Raspberry Pi Pico
uses a drive named `RPI-RP2`.

---

## 5. Installing and Testing MicroPython

### 5.1 Installing MicroPython

I downloaded the MicroPython firmware for the Raspberry Pi Pico 2 W
and copied the `.uf2` file to the `RP2350` drive while the Pico was
in BOOTSEL mode.

After the firmware was copied, the `RP2350` drive disappeared and
the Pico rebooted.

### 5.2 Setting Up MicroPico

I installed the MicroPico extension in VS Code.

I then initialized the e-reader folder as a MicroPico project.

MicroPico successfully detected and connected to the Raspberry Pi
Pico 2 W.

### 5.3 First MicroPython Test

The VS Code terminal displayed the MicroPython REPL:

`MicroPython v1.29.0 ... Raspberry Pi Pico 2 W with RP2350`

I ran:

```python
print("Hello from my Pico 2 W!")
```
### 5.4 Running a Python File on the Pico

I created `src/main.py` and wrote my first MicroPython program:

```python
from machine import Pin

print("Hello from my e-reader!")
```

Initially, I accidentally used VS Code's normal Python Run button.
This attempted to execute the file using Python 3.11 on my PC, which
resulted in:

```text
ModuleNotFoundError: No module named 'machine'
```

I learned that `machine` is a MicroPython module available on the Pico,
but not a standard Python module on my PC.

I then used MicroPico to upload `main.py` to the Pico and used the
MicroPico Run button in the bottom left to execute it.

The Pico successfully printed:

```text
Hello from my e-reader!
```

This established the basic development workflow for the project:

1. Write MicroPython code in VS Code.
2. Upload the file to the Pico using MicroPico.
3. Run the file on the Pico.
4. View the output through the MicroPython REPL (Read-eval-print loop).

## 5.5 Connecting and Testing a Physical Button

After getting MicroPython running successfully, I wanted to test whether the Pico could interact with physical hardware.

The first component I tested was a tactile push button.

### Physical Connection

I connected the button between GPIO 10 and GND:

```text
Pico GP10 ───── button ───── GND
```

I used two jumper wires to connect the Pico directly to the button rather than mounting the Pico into the breadboard.

The button is a simple mechanical switch. When it is not pressed, the electrical connection between its two sides is open. When it is pressed, the connection closes.

Conceptually:

```text
Button released:

GP10 ─────/ ───── GND
          open


Button pressed:

GP10 ──────────── GND
          closed
```

### Understanding GPIO Inputs

GPIO stands for **General-Purpose Input/Output**.

A GPIO pin can generally be configured as either an input or an output.

For this experiment, GP10 is configured as an input because I want the Pico to **read** whether the button is pressed.

In MicroPython:

```python
button = Pin(10, Pin.IN, Pin.PULL_UP)
```

The three important parts are:

```python
Pin(10, Pin.IN, Pin.PULL_UP)
```

- `10` specifies GPIO 10 (GP10).
- `Pin.IN` configures the GPIO as an input.
- `Pin.PULL_UP` enables the Pico's internal pull-up resistor.

### Why Do We Need a Pull-Up Resistor?

An input GPIO should not normally be left electrically "floating".

If the Pico simply reads a GPIO pin with nothing determining its voltage, the input can pick up electrical noise and potentially alternate unpredictably between HIGH and LOW.

We therefore need a way to give the input a defined default state.

A **pull-up resistor** connects the GPIO weakly to the positive supply voltage. In this case, the Pico provides an internal pull-up resistor, so no external resistor is required.

Conceptually:

```text
             3.3 V
               │
        internal pull-up
          resistor
               │
               ├──────── GP10
               │
             button
               │
              GND
```

When the button is **not pressed**, the pull-up resistor causes GP10 to be HIGH.

When the button **is pressed**, GP10 is connected directly to GND, which is LOW.

Therefore:

```text
Button released → GP10 = HIGH → 1
Button pressed   → GP10 = LOW  → 0
```

This can initially feel backwards because we might expect a pressed button to produce `1`.

However, with a pull-up configuration, pressing the button actually pulls the GPIO **down to ground**, so the pressed state is `0`.

### What Does "Pull-Up" Mean?

The term "pull-up" describes the default direction of the GPIO voltage.

The resistor is effectively "pulling" the GPIO toward the positive supply voltage.

It is a relatively weak connection, meaning that when the button is pressed, the much stronger connection to GND wins and the GPIO becomes LOW.

This gives us a stable default state:

```text
                released
                   ↓
3.3 V ── resistor ── GP10 ── button ── GND
                         ↑
                       HIGH


                 pressed
                   ↓
3.3 V ── resistor ── GP10 ── button ── GND
                         │
                         └────────────── GND
                              LOW
```

### Key Electronics Concepts Learned

A pull-up resistor does two important things:

1. It gives GP10 a defined default HIGH state when the button is open.
2. It limits the current when the button is pressed.

The resistor does not "create" voltage or make charge move. The Pico's 3.3 V supply provides the potential difference, while the resistor limits the current according to Ohm's law:

```text
I = V / R
```

When the button is released, GP10 is connected to 3.3 V through the pull-up resistor:

```text
GP10 ≈ 3.3 V → HIGH → 1
```

When the button is pressed, GP10 is connected directly to GND:

```text
GP10 ≈ 0 V → LOW → 0
```

The voltage drop occurs across the resistor when current flows. The button itself has very low resistance, so there is approximately no voltage drop across the closed button.

Without the pull-up resistor, the GPIO would be left floating when the button was released, meaning the Pico could not reliably determine whether the input was HIGH or LOW.

If the resistor were completely absent, pressing the button would create a very-low-resistance path directly between 3.3 V and GND, resulting in a short circuit and potentially excessive current.

The important distinction is:

- **Voltage** is the potential difference between two points.
- **Current** is the flow of electric charge.
- **Resistance** opposes and limits current.
- A potential difference across a resistance causes current to flow according to Ohm's law.

### Reading the GPIO

Once the pin has been configured, I can read its current state with:

```python
button.value()
```

This returns the current digital state of the GPIO.

For this setup:

```python
button.value() == 1
```

means the button is released, while:

```python
button.value() == 0
```

means the button is pressed.

I therefore used:

```python
if button.value() == 0:
    print("Button pressed!")
else:
    print("Button released!")
```

### Testing the Button

The complete button test was:

```python
from machine import Pin
import time

button = Pin(10, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Button pressed!")
    else:
        print("Button released!")

    time.sleep(0.2)
```

The program continuously reads GP10 and prints the current state of the button.

The `while True:` loop means the program continues running indefinitely.

The `time.sleep(0.2)` pauses the program for 0.2 seconds between readings. Without this delay, the Pico would repeatedly read and print the button state extremely quickly.

### Result

The button worked successfully.

When the button was released, the REPL printed:

```text
Button released!
```

When the button was pressed, it printed:

```text
Button pressed!
```

This was my first successful test of a physical input controlling a MicroPython program on the Pico.

## 5.6 Button State and Press Detection

After successfully using the button to control the built-in LED, I wanted to make the LED toggle state each time the button was pressed.

The first version I wrote myself was:

```python
from machine import Pin
import time

button = Pin(10, Pin.IN, Pin.PULL_UP)

led = Pin("LED", Pin.OUT)

while True:

    button_check = button.value()

    led_check = led.value()

    if button_check == 0:

        if led_check == 0:

            led.on()

        if led_check == 1:

            led.off()
```

### What My Code Does

My code reads both the button state and the current LED state:

```python
button_check = button.value()
led_check = led.value()
```

The button state tells the program whether the button is currently pressed:

```text
1 → released
0 → pressed
```

The LED state tells the program whether the LED is currently on or off:

```text
1 → ON
0 → OFF
```

The program then checks whether the button is pressed.

If it is pressed and the LED is currently off, the LED is turned on:

```python
if button_check == 0:
    if led_check == 0:
        led.on()
```

If the button is pressed and the LED is currently on, the LED is turned off:

```python
if led_check == 1:
    led.off()
```

This creates a toggle:

```text
OFF → ON
ON  → OFF
```

### An Unexpected Problem

Although this code worked, the LED sometimes appeared to flicker or did not toggle reliably.

The reason is that the `while True` loop runs extremely quickly.

The program was effectively doing this while the button was held down:

```text
Button pressed
     ↓
Toggle LED
     ↓
Button still pressed
     ↓
Toggle LED again
     ↓
Button still pressed
     ↓
Toggle LED again
     ↓
...
```

Therefore, the LED could be toggled many times while the button was held down.

The program was responding to the **button's state** rather than to a single **button press event**.

### Detecting a Button Press

To solve this, I used the previous button state as well as the current button state.

The improved version was:

```python
from machine import Pin
import time

button = Pin(10, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

last_button_state = 1

while True:

    current_button_state = button.value()

    if last_button_state == 1 and current_button_state == 0:

        led.value(not led.value())
        print("Button pressed!")

    last_button_state = current_button_state

    time.sleep(0.02)
```

### Comparing the Two Versions

The main difference is **what the program is looking for**.

My original code asks:

> "Is the button currently pressed?"

The improved code asks:

> "Has the button just changed from released to pressed?"

The important transition is:

```text
Previous state    Current state
      1      →          0
   released           pressed
                   ↓
              NEW PRESS
```

Once this transition is detected, the LED is toggled once.

If the button remains held:

```text
1 → 0    → toggle
0 → 0    → nothing
0 → 0    → nothing
0 → 0    → nothing
```

When the button is released:

```text
0 → 1    → nothing
```

And when it is pressed again:

```text
1 → 0    → toggle
```

This means one physical button press produces one LED toggle.

### Understanding `last_button_state`

The variable:

```python
last_button_state = 1
```

stores the state of the button during the previous loop iteration.

The current state is then obtained using:

```python
current_button_state = button.value()
```

The program compares the two:

```python
if last_button_state == 1 and current_button_state == 0:
```

This specifically detects the transition from:

```text
HIGH → LOW
 1  →  0
```

which corresponds to pressing the button because the input uses a pull-up resistor.

After checking the button, the previous state is updated:

```python
last_button_state = current_button_state
```

This allows the program to compare the current state with the state from the next loop iteration.

### Using `led.value()` to Toggle the LED

The improved code uses:

```python
led.value(not led.value())
```

`led.value()` reads the LED's current output state:

```text
0 → OFF
1 → ON
```

The `not` operator reverses that state:

```text
not 0 → True → 1
not 1 → False → 0
```

Therefore:

```python
led.value(not led.value())
```

means:

> Read the current LED state and set it to the opposite state.

This produces:

```text
OFF → ON
ON  → OFF
```

### Why `time.sleep(0.02)` Is Used

The improved version checks the button every 20 milliseconds:

```python
time.sleep(0.02)
```

This prevents the loop from running unnecessarily fast and also gives the program a reasonable sampling interval for the button.

The delay is short enough that the button still feels instantaneous when pressed.

### State vs. Event

This experiment introduced an important distinction:

**State:**

> What is the button doing right now?

```python
button.value()
```

**Event:**

> Did the button just change from released to pressed?

```text
previous = 1
current  = 0
```

The original program reacted to the **state** of the button.

The improved program detects a **press event** by comparing the previous and current states.

This distinction will be important later when physical buttons are used to control actions on the e-reader, such as changing pages.

### Result

The improved program successfully allowed one button press to toggle the LED once, without continuous flickering while the button was held.

This was my first introduction to storing a previous hardware state and detecting a change between two states.

## 5.7 Working with Multiple Buttons

After learning how to detect a press from a single button, I added a second physical button to learn how multiple inputs can be handled independently.

### Physical Connection

The buttons were connected as:

```text
Button 1 → GP10 → GND
Button 2 → GP6  → GND
```

Both GPIO inputs use the Pico's internal pull-up resistors.

### Testing Two Buttons

The goal was simple:

- **Button 1 → turn the LED ON**
- **Button 2 → turn the LED OFF**

I wrote the following code:

```python
from machine import Pin
import time

button_1 = Pin(10, Pin.IN, Pin.PULL_UP)
button_2 = Pin(6, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

last_button1_state = 1
last_button2_state = 1

while True:
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
```

### What I Learned

The main concept I learned was that each button can be treated as an independent input. Each button has its own current state and previous state, allowing the program to detect a new press separately.

I also understood more clearly that:

```python
button.value()
```

reads the **current electrical state** of the GPIO pin every time it is called. It is not a toggle command.

With the pull-up resistor:

```text
Released → 1
Pressed  → 0
```

The program compares the previous and current states to detect the transition:

```text
1 → 0 = new button press
```

### Result

Both buttons worked successfully. Button 1 turned the LED on, while Button 2 turned it off.

This experiment introduced me to handling multiple hardware inputs and applying the same state/event logic independently to each input.

## 5.8 Non-Blocking Timing with `ticks_ms()`

I learned how to measure elapsed time on the Pico without using `time.sleep()`.

The basic functions are:

```python
time.ticks_ms()
```

which gives the current time in milliseconds, and:

```python
time.ticks_diff(current_time, previous_time)
```

which calculates the time elapsed between two timestamps.

I tested this using:

```python
from machine import Pin
import time

led = Pin("LED", Pin.OUT)

previous_time = time.ticks_ms()

while True:
    led.value(0)

    current_time = time.ticks_ms()

    passed = time.ticks_diff(current_time, previous_time)

    if passed >= 1000:
        led.value(1)
        print("1 second has passed!")
        previous_time = current_time
```

### How It Works

At the beginning, I store a timestamp:

```python
previous_time = time.ticks_ms()
```

Inside the `while True` loop, I continuously get the current timestamp:

```python
current_time = time.ticks_ms()
```

I then calculate how much time has passed:

```python
passed = time.ticks_diff(current_time, previous_time)
```

If at least 1000 milliseconds have passed:

```python
if passed >= 1000:
```

the LED is turned on and the message is printed. `previous_time` is then updated so that the next one-second interval can begin.

### What I Learned

Why:

```python
if passed >= 1000:
```

is preferable to:

```python
if passed == 1000:
```

The loop may not check the timer at exactly 1000 ms, so checking whether at least 1000 ms have passed is more reliable.
Most importantly, I learned that this approach allows the program to **measure elapsed time without stopping the entire program with `time.sleep()`**.
This will be useful later when the Pico needs to handle multiple things such as buttons, the display, storage, and Wi-Fi.

## 5.9 SPI Fundamentals

Before connecting the e-paper display, I learned how the Pico communicates with external hardware using SPI (Serial Peripheral Interface).

### What Is SPI?

SPI is a communication protocol/interface used to exchange data between a controller, such as the Pico, and peripheral devices such as displays, SD cards, sensors, and other hardware.

The RP2350 inside the Pico 2 W contains dedicated hardware for implementing SPI communication.

SPI commonly uses four main signals:

```text
MOSI → Controller → Peripheral
MISO ← Controller ← Peripheral
SCK  → Clock signal
CS   → Selects the peripheral
```

### SPI Signals

**MOSI — Master Out, Slave In**

Carries data from the Pico to the peripheral.

**MISO — Master In, Slave Out**

Carries data from the peripheral back to the Pico.

**SCK — Serial Clock**

The Pico generates the clock signal used to synchronize the data transfer between the Pico and the peripheral.

**CS — Chip Select**

Selects which peripheral the Pico is communicating with. Multiple peripherals can share MOSI, MISO, and SCK while using separate CS pins.

For example:

```text
SPI0
 ├── MOSI ─────┬── E-paper
 ├── MISO ─────┤
 └── SCK ──────┤
               │
       CS1 ─── E-paper
       CS2 ─── SD card
```

Only the peripheral whose CS is active participates in the communication.

### Sending Data with SPI

SPI transfers data as individual bits. For example:

```text
10110010
```

The bits are transferred sequentially while the clock provides the timing reference.

SPI is also full-duplex, meaning data can be sent from the Pico to a peripheral through MOSI while data is simultaneously sent back through MISO.

### SPI Mode: CPOL and CPHA

The Pico and peripheral must agree on how the clock and data are synchronized.

**CPOL — Clock Polarity**

Determines the clock's idle/default level:

```text
CPOL = 0 → clock idles LOW
CPOL = 1 → clock idles HIGH
```

**CPHA — Clock Phase**

Determines which clock edge is used to sample the data.

The combination of CPOL and CPHA determines the SPI mode:

```text
Mode 0 → CPOL 0, CPHA 0
Mode 1 → CPOL 0, CPHA 1
Mode 2 → CPOL 1, CPHA 0
Mode 3 → CPOL 1, CPHA 1
```

The correct mode depends on the peripheral being used.

### SPI Hardware in the RP2350

The RP2350 has two independent SPI controllers:

```text
RP2350
├── SPI0
└── SPI1
```

These are separate hardware SPI controllers capable of communicating independently.

They are not different versions of SPI. They are two separate pieces of hardware capable of implementing the same SPI protocol.

One SPI controller can also communicate with multiple peripherals by sharing MOSI, MISO, and SCK while giving each peripheral a separate CS pin.

### SPI Configuration in MicroPython

MicroPython allows the RP2350's SPI hardware to be configured using:

```python
from machine import SPI, Pin

spi = SPI(
    0,
    baudrate=10_000_000,
    polarity=0,
    phase=0,
    sck=Pin(...),
    mosi=Pin(...),
    miso=Pin(...)
)
```

The first argument selects the SPI controller:

```python
SPI(0, ...)
```

selects SPI0, while:

```python
SPI(1, ...)
```

selects SPI1.

Other parameters configure the SPI hardware:

```text
baudrate → SPI clock frequency
polarity → CPOL
phase    → CPHA
sck      → GPIO used for SCK
mosi     → GPIO used for MOSI
miso     → GPIO used for MISO
```

The RP2350 already contains the physical SPI hardware. The MicroPython code configures that hardware for the specific peripheral being used.

### Baud Rate

The baud rate specifies the target SPI clock frequency.

For example:

```python
baudrate=10_000_000
```

represents a target SPI clock of 10 MHz, or approximately 10 million clock cycles per second.

The SPI hardware generates this clock using the RP2350's internal clocking and hardware dividers, so the achievable frequency depends on the hardware configuration.

### Key Understanding

The overall communication system can be viewed as three layers:

```text
Python code
    ↓
MicroPython
    ↓
RP2350 SPI hardware
    ↓
GPIO pins
    ↓
Physical SPI signals
    ↓
Peripheral device
```

This helped me understand that when I configure `SPI(...)` in MicroPython, I am not creating SPI in software from scratch. I am configuring dedicated SPI hardware that already exists inside the RP2350.

## 5.10 RP2350 SPI Controllers and GPIO Function Selection

After configuring SPI in MicroPython, I wanted to understand how the SPI signals actually reach the physical GPIO pins on the Pico.

### The RP2350 Has Two SPI Controllers

The RP2350 contains two independent hardware SPI controllers:

```text
SPI0
SPI1
```

These are separate hardware peripherals inside the microcontroller. They can independently handle SPI communication.

This does **not** mean that the Pico can only communicate with two SPI devices. One SPI controller can communicate with multiple devices by sharing the SPI communication lines and using separate Chip Select (CS) signals for each device.

### Internal SPI Signals vs Physical GPIO Pins

The SPI controller exists inside the RP2350, while the GPIO pins are physical connections to the outside world.

For example, SPI0 internally has signals such as:

```text
SPI0 RX
SPI0 CSn
SPI0 SCK
SPI0 TX
```

These signals need to be connected to physical GPIO pins so that they can reach an external device.

The RP2350 uses **GPIO function selection**, also called **multiplexing**, to make this connection.

### What Is GPIO Function Selection?

A GPIO pin is not permanently assigned to one purpose.

A physical GPIO can be configured to act as:

- a normal GPIO
- an SPI signal
- a UART signal
- an I2C signal
- or another supported peripheral function

The RP2350 contains internal routing hardware that connects the selected peripheral signal to the physical GPIO.

Conceptually:

```text
             RP2350
        ┌────────────────┐
        │                │
        │     SPI0       │
        │                │
        │ SCK ───────────┼──┐
        │ TX  ───────────┼──┤
        │ RX  ───────────┼──┤
        │                │  │
        └────────────────┘  │
                            ↓
                  GPIO Function Selection
                            ↓
                    Physical GPIO pins
```

So when I configure:

```python
sck=Pin(2)
```

I am not manually creating an SPI clock on GP2.

Instead, I am telling MicroPython to configure the RP2350 so that the SPI clock signal is routed to GP2.

### Example SPI0 Mapping

One valid SPI0 pin mapping is:

```text
GP0 → SPI0 RX  → MISO
GP1 → SPI0 CSn → CS
GP2 → SPI0 SCK → Clock
GP3 → SPI0 TX  → MOSI
```

This is why the pins appear together in the Pico pinout. They represent a valid combination of physical GPIOs that can be connected to the SPI0 peripheral.

There are also other valid GPIO mappings for SPI0 and SPI1.

### A GPIO Is Not Permanently an "SPI Pin"

This was an important concept for me.

Earlier, I used GP10 as a button:

```python
button = Pin(10, Pin.IN, Pin.PULL_UP)
```

In that program, GP10 was being used as a normal GPIO input.

The physical pin itself is not permanently a "button pin."

The RP2350 can configure a GPIO for different supported functions depending on what the program requires.

Therefore:

```text
Physical GPIO
      ↓
Can be connected to different internal functions
      ↓
GPIO / SPI / UART / I2C / etc.
```

The selected function determines what the pin does.

### The Complete Picture

I can now think of SPI communication as several layers:

```text
Python code
     ↓
MicroPython SPI API
     ↓
RP2350 SPI hardware
     ↓
GPIO function selection
     ↓
Physical GPIO pin
     ↓
External SPI device
```

For example:

```python
spi = SPI(
    0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(0)
)
```

means that MicroPython configures the RP2350's SPI0 peripheral and routes its SPI signals to the selected GPIOs.

The SPI hardware then handles the actual communication, while the GPIO function-selection system connects those internal signals to the physical pins.

This helped me understand that the Pico's pins are not the communication protocol itself. They are the **physical interface through which the RP2350's internal hardware peripherals communicate with external devices**.

## 5.11 Configuring SPI in MicroPython

After understanding how the RP2350 routes its internal SPI signals to GPIO pins, I configured the SPI hardware using MicroPython.

### Creating an SPI Object

I used the following code:

```python
from machine import SPI, Pin

spi = SPI(
    0,
    baudrate=10_000_000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(0)
)

print(spi)
```

The `SPI()` object represents the RP2350's hardware SPI peripheral that I want to use.

### Understanding the Configuration

```python
SPI(0)
```

selects **SPI controller 0**.

The requested SPI clock frequency was:

```python
baudrate=10_000_000
```

which requests a clock speed of 10 MHz.

I noticed that the Pico reported:

```text
baudrate=8000000
```

instead of 10 MHz.

This is because the SPI clock is generated from the RP2350's internal clock using hardware dividers, so not every arbitrary frequency can necessarily be generated exactly. MicroPython therefore configures the closest achievable frequency.

The actual configured frequency in this experiment was **8 MHz**.

### SPI Clock Configuration

I used:

```python
polarity=0
phase=0
```

These correspond to:

```text
CPOL = 0
CPHA = 0
```

which is **SPI Mode 0**.

`polarity` determines the clock's idle level, while `phase` determines which clock edge is used for sampling data.

### GPIO Assignment

I configured:

```python
sck=Pin(2)
mosi=Pin(3)
miso=Pin(0)
```

which resulted in:

```text
GP2 → SPI0 SCK  → Clock
GP3 → SPI0 TX   → MOSI
GP0 → SPI0 RX   → MISO
```

The RP2350's GPIO function-selection system connects these physical GPIOs to the corresponding SPI0 signals.

### Checking the Configuration

When I printed the SPI object:

```python
print(spi)
```

the Pico returned:

```text
SPI(0, baudrate=8000000, polarity=0, phase=0, bits=8, sck=2, mosi=3, miso=0)
```

This showed the actual configuration of the SPI peripheral.

The output also showed:

```text
bits=8
```

meaning the SPI peripheral is configured to transfer data in **8-bit units**.

### What I Learned

This experiment helped connect the previous concepts together.

When I write:

```python
spi = SPI(...)
```

I am not manually creating the SPI signals with Python.

Instead, I am configuring the **dedicated SPI hardware inside the RP2350**.

The RP2350 then handles the clock generation and bit shifting according to the configured SPI settings.

The overall process is:

```text
Python code
     ↓
MicroPython SPI configuration
     ↓
RP2350 SPI0 hardware
     ↓
GPIO function selection
     ↓
GP2 / GP3 / GP0
     ↓
Physical SPI signals
```

At this point, the SPI peripheral was configured, but I had not yet transmitted any data.

## 5.12 Sending Data Through SPI

After configuring the SPI peripheral, I wanted to actually transmit data through it.

I used:

```python
from machine import SPI, Pin

spi = SPI(
    0,
    baudrate=10_000_000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(0)
)

print(spi)

spi.write(b'\xAA')

print("Byte sent!")
```

### Sending a Byte

The important line is:

```python
spi.write(b'\xAA')
```

This tells the SPI peripheral to transmit the byte `0xAA`.

In binary:

```text
0xAA = 10101010
```

The SPI hardware takes these bits and sends them sequentially through the MOSI pin.

Conceptually:

```text
MOSI → 1 0 1 0 1 0 1 0
```

At the same time, the SPI hardware generates the clock signal on SCK.

The receiving device uses the clock to determine when to sample the MOSI signal.

### What Happens Inside the Pico

The process can be thought of as:

```text
spi.write(b'\xAA')
        ↓
     MicroPython
        ↓
    RP2350 SPI0
        ↓
  Convert byte into bits
        ↓
Generate clock + shift bits
        ↓
      MOSI (GP3)
```

The important thing I learned is that Python does **not** manually toggle GP3 eight times.

The dedicated SPI hardware inside the RP2350 performs the bit shifting and clock generation.

### From Byte to Electrical Signal

The byte:

```text
10101010
```

is represented electrically on the MOSI line as a sequence of HIGH and LOW voltage levels.

The clock on SCK provides the timing reference for these bits.

Conceptually:

```text
MOSI:  1    0    1    0    1    0    1    0
       ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑
SCK:  _|‾|__|‾|__|‾|__|‾|__|‾|__|‾|__|‾|__|‾|_
```

The receiving SPI device can therefore reconstruct the original byte from the electrical signals.

### Result

The Pico successfully transmitted the byte and printed:

```text
Byte sent!
```

This was my first successful SPI transmission.

It helped me understand the complete path from software data to physical electrical signals:

```text
Python byte
    ↓
MicroPython
    ↓
RP2350 SPI hardware
    ↓
Bits
    ↓
MOSI + SCK electrical signals
    ↓
External SPI device
```

This experiment also made the purpose of SPI much clearer to me. A GPIO pin represents a physical electrical signal, while SPI provides the communication protocol and dedicated hardware that allows digital data to be transferred efficiently between chips.

## 5.13 Chip Select (CS)

After successfully transmitting a byte through SPI, I learned about the **Chip Select (CS)** signal and why it is used with SPI devices.

### Why Is CS Needed?

SPI is designed as a shared communication bus. Multiple SPI devices can share the same:

- MOSI
- MISO
- SCK

However, the Pico needs a way to indicate which device it currently wants to communicate with.

Each SPI device can therefore have its own **Chip Select (CS)** signal.

Conceptually:

```text
                    ┌── E-paper
                    │
MOSI ───────────────┼── SD card
SCK  ───────────────┼── Sensor
MISO ───────────────┼── ...
                    │

CS1 ─────────────────── E-paper
CS2 ─────────────────── SD card
CS3 ─────────────────── Sensor
```

The communication lines are shared, while each device has its own CS signal.

### Active-Low Chip Select

SPI devices commonly use an active-low CS signal, often written as **CSn**.

This means:

```text
CS = 1 → device not selected
CS = 0 → device selected
```

Therefore, the Pico can select a device by pulling its CS pin LOW.

### Adding CS to the SPI Experiment

I added GP1 as the CS GPIO:

```python
from machine import SPI, Pin

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
```

The sequence is:

```text
CS HIGH
   ↓
CS LOW
   ↓
Transmit data
   ↓
CS HIGH
```

Conceptually:

```text
CS   ───────┐____________┌──────
            │            │
            │  selected  │
            │            │
SCK          └─┐_┌─┐_┌─┐_┌─┐_
                 

MOSI          1 0 1 0 1 0 1 0
```

When CS is LOW, the selected SPI device knows that the following clock and data signals are intended for it.

### CS Is Still a GPIO

An important thing I learned is that CS does not necessarily need to be controlled by the SPI peripheral itself.

I can control it as a normal GPIO:

```python
cs = Pin(1, Pin.OUT)
```

and then manually select and deselect the device:

```python
cs.value(0)   # select device

spi.write(data)

cs.value(1)   # deselect device
```

This means that SPI communication involves multiple signals with different responsibilities:

```text
MOSI → carries data
MISO → carries data back
SCK  → provides timing
CS   → selects the device
```

### Why This Is Different From a Button

When I used a button, I only needed to read the voltage on one GPIO:

```python
button.value()
```

There was only one device connected to that input, so there was no need to select a device.

SPI is different because it is a **communication bus** where multiple devices can share the same communication lines.

CS provides the device-selection mechanism.

### Important Distinction

CS is not what makes SPI communication possible by itself.

The SPI peripheral is responsible for implementing the SPI communication protocol, including clock generation and data shifting.

CS simply tells a particular peripheral:

> "You are the device I am communicating with right now."

This experiment gave me the complete basic SPI transaction:

```text
Select device
     ↓
Transmit/receive data
     ↓
Deselect device
```

## 5.14 Why Use SPI Instead of Directly Controlling GPIOs?

While learning SPI, I initially wondered why I needed an SPI peripheral at all.

If a GPIO pin can output HIGH or LOW, it seemed like I could simply control several GPIO pins directly and communicate with an external device that way.

This question helped me understand the difference between a **GPIO** and a **communication protocol/peripheral**.

### GPIOs Are Physical Electrical Interfaces

A GPIO pin allows the microcontroller to interact directly with an electrical signal.

For example, with a button:

```text
GP10 ─── button ─── GND
```

I can simply read:

```python
button.value()
```

and determine whether the pin is HIGH or LOW.

The button only requires a simple electrical state:

```text
HIGH → released
LOW  → pressed
```

There is no complex communication protocol involved.

### SPI Requires Coordinated Signals

An SPI device is different.

For example, to send the byte:

```text
10101010
```

the Pico needs to produce a specific sequence of data and clock signals.

The receiving device needs to know:

- which wire contains the data
- which wire contains the clock
- when to sample the data
- what clock polarity and phase are being used
- when a transaction starts and ends
- which device is being communicated with

The SPI protocol defines these rules.

### SPI Could Be Created Using GPIOs

It is technically possible to implement SPI manually using ordinary GPIOs.

For example, I could configure:

```python
sck = Pin(2, Pin.OUT)
mosi = Pin(3, Pin.OUT)
cs = Pin(1, Pin.OUT)
```

and manually change their states:

```python
mosi.value(1)
sck.value(1)
sck.value(0)

mosi.value(0)
sck.value(1)
sck.value(0)

# and so on...
```

This technique is called **bit-banging**.

I would essentially be manually creating the SPI waveform using GPIOs.

However, this becomes inefficient and difficult when transmitting large amounts of data.

### Using the Hardware SPI Peripheral

Instead of manually controlling every bit, I can configure the RP2350's dedicated SPI hardware:

```python
spi = SPI(...)
```

and then simply write:

```python
spi.write(data)
```

The SPI hardware handles the low-level communication.

It generates the clock, shifts the bits through MOSI, samples MISO when receiving data, and follows the configured SPI timing.

Therefore:

```text
Without hardware SPI:

Python
  ↓
Manually control GPIO
  ↓
Manually generate clock
  ↓
Manually send each bit


With hardware SPI:

Python
  ↓
spi.write(data)
  ↓
RP2350 SPI hardware
  ↓
Clock + data generated automatically
```

### The E-Paper Example

This became much clearer when I thought about the actual e-paper display.

The Waveshare display is a **400 × 300** pixel display.

For a black-and-white image, there are:

```text
400 × 300 = 120,000 pixels
```

If each pixel is represented by one bit, that is:

```text
120,000 bits
```

or:

```text
15,000 bytes
```

of pixel data.

Manually toggling GPIOs for every bit would be extremely inefficient.

Instead, the program can provide the data to the SPI peripheral:

```python
spi.write(pixel_data)
```

and the RP2350's SPI hardware handles the actual bit-level transmission.

### The Important Concept

This helped me understand that:

> **GPIOs are the physical electrical interface, while SPI is a communication protocol implemented by dedicated hardware that uses those physical connections.**

The GPIO is the wire.

SPI defines **how information is communicated over that wire**.

The overall process is:

```text
Application data
      ↓
MicroPython
      ↓
SPI peripheral
      ↓
MOSI / SCK / MISO / CS
      ↓
Electrical signals
      ↓
External device's SPI interface
      ↓
Received bytes
      ↓
Device interprets those bytes
```

For example, when I send:

```python
spi.write(b'\xAA')
```

the byte:

```text
0xAA
```

becomes:

```text
10101010
```

The SPI hardware converts this into the appropriate electrical signal sequence on MOSI, synchronized by SCK.

The receiving device's SPI interface reconstructs the bits into the original byte.

### Two Layers of Communication

I also learned that there are actually two different layers involved.

**SPI layer:**

```text
How do we reliably transfer these bits?
```

**Device protocol layer:**

```text
What do these bytes actually mean?
```

SPI itself does not know what a particular byte means.

For example, a byte received by an e-paper controller might represent a command, an address, or part of the display data depending on the display's own communication protocol.

Therefore:

```text
SPI
↓
transfers the bits

Device controller
↓
interprets what those bits mean
```

This was the point where I understood why SPI is necessary for communicating with devices such as the e-paper display, SD card, and other peripherals.
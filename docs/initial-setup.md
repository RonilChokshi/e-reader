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

The resistor also limits the current when the button is pressed. Without a resistor, directly connecting the 3.3 V supply to GND would create an unwanted short circuit.

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
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
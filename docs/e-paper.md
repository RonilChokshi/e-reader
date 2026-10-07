# 02 — E-Paper Display

This section documents the process of connecting, understanding, and communicating with the Waveshare Pico-ePaper-4.2 display.

The goal is not only to make the display work, but to understand how the Pico communicates with the display at the hardware and software level.

## 1. Understanding the Display Interface

The Waveshare Pico-ePaper-4.2 exposes several pins used for power, SPI communication, and additional control signals.

The main pins are:

```text
VCC
GND
DIN
CLK
CS
DC
RST
BUSY
```

The SPI-related pins are:

```text
DIN → MOSI
CLK → SCK
CS  → Chip Select
```

The remaining control pins are:

```text
DC
RST
BUSY
```

I will learn the purpose of these signals before writing the display driver.

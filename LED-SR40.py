import utime
from machine import Pin
import neopixel
import time

# Ultrasonic sensor setup
trigger = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

# LED setup
NUM_LEDS = 16  # Number of LEDs
PIN = 0         # Data pin

np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

# Patterns for 'A' and 'C'
A_PATTERN = [
    0b0110,  # _XX_
    0b1001,  # X__X
    0b1111,  # XXXX
    0b1001   # X__X
]

C_PATTERN = [
    0b1111,  # XXX_
    0b0001,  # X___
    0b1000,  # X___
    0b1111   # XXX_
]

# Function to clear all LEDs
def clear_leds():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

# Function to display a 4x4 pattern on LEDs
def display_pattern(pattern, row_offset):
    clear_leds()
    for row in range(4):
        for col in range(4):
            if pattern[row] & (1 << (3 - col)):
                index = (row + row_offset) * 4 + col
                if 0 <= index < NUM_LEDS:
                    np[index] = (25, 25, 25)  # White color
    np.write()

# Function to read distance from ultrasonic sensor
def read_distance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep(0.00001)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance

# Main loop
while True:
    distance = read_distance()
    print("Distance: ", distance, "cm")

    # If distance is less than 20 cm, light up LEDs with 'A' pattern
    if distance < 20:
        display_pattern(A_PATTERN, 4)
    else:
        # Otherwise, scroll patterns 'A' to 'C'
        for offset in range(5):
            display_pattern(A_PATTERN, 4 - offset)
            time.sleep(0.1)
        for offset in range(5):
            display_pattern(C_PATTERN, 4 - offset)
            time.sleep(0.1)

    time.sleep(1)

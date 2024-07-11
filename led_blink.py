from machine import Pin
import time

LED_PIN = 15

led = Pin( LED_PIN, Pin.OUT )

while True:
    led.high()
    time.sleep( 1 )
    led.low()
    time.sleep( 1 )

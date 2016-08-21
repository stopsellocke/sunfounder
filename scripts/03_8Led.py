#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

pins = [11, 12, 13, 15, 16, 18, 22, 7]
BtnPin = 40
sCurAction = 'left_right'
bWantActionChange = False

def setup():
  GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
    GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led

def wait_for_btn():
  GPIO.add_event_detect(BtnPin, GPIO.FALLING, bouncetime=200) # wait for falling
  GPIO.add_event_callback(BtnPin, swAction) # wait for falling
  while True:
    loop()
    pass   # Don't do anything

def swAction(ev=None):
  global sCurAction
  sCurAction = 'knight_rider'
  global bWantActionChange
  bWantActionChange = True
  print 'Action:'+sCurAction

def loop():
  while True:
    reset()
    global sCurAction
    if sCurAction == 'left_right':
      left_right()
    elif sCurAction == 'right_left':
      right_left()
    elif sCurAction == 'knight_rider':
      knight_rider()
    elif sCurAction == 'blink':
      blink()
    elif sCurAction == 'on_off':
      set_on_off()

def reset():
  for pin in pins:
    GPIO.output(pin, GPIO.HIGH)    # turn off all leds

def get_all_pins():
  return list(pins)

def get_inactive_pins():
  inactive_pins = []
  for pin in pins:
    if GPIO.input(pin) == GPIO.HIGH:
      inactive_pins.append(pin)
  return inactive_pins

def get_active_pins():
  active_pins = []
  for pin in pins:
    if GPIO.input(pin) == GPIO.LOW:
      active_pins.append(pin)
  return active_pins

def want_action_change(fSleep):
  global bWantActionChange
  if bWantActionChange:
    bWantActionChange = False
    return True
  time.sleep(0.5)
  return False

def right_left():
  all_pins = get_all_pins()
  for pin in all_pins:
    GPIO.output(pin, GPIO.LOW)
    if want_action_change(0.1):
      return True
    GPIO.output(pin, GPIO.HIGH)

def left_right():
  all_pins = get_all_pins()
  all_pins.reverse()
  for pin in all_pins:
    GPIO.output(pin, GPIO.LOW)	
    if want_action_change(0.1):
      return True
    GPIO.output(pin, GPIO.HIGH)

def knight_rider():
  all_pins = get_all_pins()
  last_pin = -1
  for pin in all_pins:
    if pin == last_pin:
      continue
    last_pin = pin
    GPIO.output(pin, GPIO.LOW)	
    if want_action_change(0.1):
      return True
    GPIO.output(pin, GPIO.HIGH)
  all_pins.reverse()
  for pin in all_pins:
    if pin == last_pin:
      continue
    last_pin = pin
    GPIO.output(pin, GPIO.LOW)	
    if want_action_change(0.1):
      return True
    GPIO.output(pin, GPIO.HIGH)

def blink():
  status = GPIO.LOW
  while True:
    status = GPIO.LOW if status == GPIO.HIGH else GPIO.HIGH
    for pin in pins:
      GPIO.output(pin, status)	
    time.sleep(0.5)

def get_inactive_pins():
  inactive_pins = []
  for pin in pins:
    if GPIO.input(pin) == GPIO.HIGH:
      inactive_pins.append(pin)
  return inactive_pins

def get_active_pins():
  active_pins = []
  for pin in pins:
    if GPIO.input(pin) == GPIO.LOW:
      active_pins.append(pin)
  return active_pins

def set_on():
  inactive_pins = get_inactive_pins()
  while len(inactive_pins) > 0:
    for index, pin in enumerate(inactive_pins):
      GPIO.output(pin, GPIO.LOW)
      time.sleep(0.2)
      if index+1 != len(inactive_pins):
        GPIO.output(pin, GPIO.HIGH)
      else:
        inactive_pins.pop()

def set_off():
  active_pins = get_active_pins()
  inactive_pins = get_inactive_pins();
  active_pins.reverse()
  while len(active_pins) > 0:
    pin = active_pins.pop()
    GPIO.output(pin, GPIO.HIGH)
    inactive_pins.insert(0,pin)
    for index, pin in enumerate(inactive_pins):
      GPIO.output(pin, GPIO.LOW)
      time.sleep(0.2)
      GPIO.output(pin, GPIO.HIGH)

def set_on_off():
  while True:
    set_on()
    time.sleep(0.2)
    set_off()
    time.sleep(0.4)

def destroy():
  for pin in pins:
    GPIO.output(pin, GPIO.HIGH)    # turn off all leds
  GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
  setup()
  try:
    wait_for_btn()
#    loop()
#    knight_rider()
#    blink()
#    set_on_off()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()


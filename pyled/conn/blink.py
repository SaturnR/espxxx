from machine import Pin, PWM, ADC
import time

i = 0
incr = False

pr = Pin(13, Pin.OUT)
pg = Pin(12, Pin.OUT)
pb = Pin(14, Pin.OUT)

rpwm = PWM(pr)
gpwm = PWM(pg)
bpwm = PWM(pb)

rpwm.freq(500)
rpwm.duty(1023)

gpwm.freq(500)
gpwm.duty(1023)

bpwm.freq(500)
bpwm.duty(1023)

adc = ADC(0)

delay = 0.2
inc_val = 1

def change(val):
  return int((1023 - val) * i/50) + val

while True:
  if incr:
    i += inc_val
    if i > 50:
      incr = False
      i = 50
  else:
    i -= inc_val
    if i < 0:
      i = 0
      incr = True
  
  v = adc.read()
  
  if v > 1000:
    delay = 0.02
  else:
    delay = 0.2
  
  r = change({0})
  g = change({1})
  b = change({2})

  time.sleep(delay)
  
  rpwm.duty(r)
  gpwm.duty(g)
  bpwm.duty(b)

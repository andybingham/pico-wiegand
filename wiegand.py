import time
import rp2
from machine import Pin

# PIO State machine for recieving Wiegand data
# Needs two to cover D0 and D1
# set x = 0 for D0 and &ff for D1


@rp2.asm_pio(autopull=True, pull_thresh=8)
def wiegand_bit():
    wrap_target()
    wait(1, 0)  # wait for the start of a bit
    wait(0, 0)  # wait for the end of a bit
    in(x, 1)  # send the bit, x will be 00, or ff
    wrap()


sm-d0 = rp2.StateMachine(0,wiegand_bit,freq=1000, set_base=Pin(5), set_x=0, in_shiftdir=0)
sm-d1 = rp2.StateMachine(1,wiegand_bit,freq=1000, set_base=Pin(6), set_x=1, in_shiftdir=0)

sm-d0.active()
sm-d1.active()

while True:
    print data.append(sm-d0.get())
import time
import rp2
from machine import Pin

# PIO State machine for recieving Wiegand data
# Needs two to cover D0 and D1
# set x = 0 for D0 and &ff for D1
# uses autpush with threshold of 17 bits to pish the date in two pieces

@rp2.asm_pio(autopush=True, push_thresh=17, set_init=rp2.PIO.IN_HIGH)
def wiegand_bit():
    wrap_target()
        wait(0, 1, 0)  # wait for the start of a bit
        in_(x, 1)  # send the bit, x will be 00, or ff
        wait(1, 1, 0)  # wait for the end of a bit
    wrap()

smD0 = rp2.StateMachine(0, wiegand_bit, freq=8000000,
                        set_base=Pin(5), in_shiftdir=0)

smD1 = rp2.StateMachine(1, wiegand_bit, freq=8000000,
                        set_base=Pin(6), in_shiftdir=0)

smD0.active(1)
smD0.exec('set(x,0)')
smD1.active(1)
smD1.exec('set(x,255)')

print("Starting")
while True:
    byte = smD0.get()
    print('Byte')
    print(byte)

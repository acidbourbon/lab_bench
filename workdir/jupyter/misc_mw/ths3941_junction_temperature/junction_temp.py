#!/usr/bin/env python3

import agilent_34410A_multimeter as mult
mult.init("192.168.0.222")

def junctemp(v):
  return v*309.2-282.5

def read_junction_temp():
  jt = junctemp(mult.read_voltage())
  if jt < -30:
   jt = -30
  return jt



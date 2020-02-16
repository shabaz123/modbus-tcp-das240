#!/usr/bin/python3

#***********************************************************
#  das240.py
#  MODBUS TCP code for BK Precision / Sefram DAS2x0-BAT
#  (DAS220-BAT and DAS240-BAT)
#  rev 1.0 Jan 2020 - first revision - shabaz
#
# usage: 
#   import das240 as das
#   val=das.read("xx.xx.xx.xx", n)
#   print("value is " + val)
#   das.log("xx.xx.xx.xx", n, "mylogfile.log")
#
# notes:
#   "xx.xx.xx.xx" is replaced with IP address of DAS2x0
#   n is the channel to read (1-200 for analog,
#                             1001-1012 for logic)
#   returned value is a floating point voltage, or
#   0 or 1 for logic channels.
#   use channel 999 or 1999 for test purposes
#   (returns 1.2345 or 1)
# license: 
#
#   free for any use
#***********************************************************

from datetime import datetime
import struct
from pyModbusTCP.client import ModbusClient as mb

def read(device_ip, reqchan):
  ANA = 0
  LOGIC = 1

  regstart = 0x08
  validchan = 0
  testmode = 0
  type = ANA

  # check valid channel request
  if ((reqchan>0) and (reqchan < 201)):
    validchan = 1

  if ((reqchan > 1000) and (reqchan < 1013)):
    type = LOGIC
    validchan = 1

  if (reqchan==999):
    validchan = 1
    type = ANA
    testmode = 1

  if (reqchan==1999):
    validchan = 1
    type = LOGIC
    testmode = 2

  if (validchan == 0):
    print("Error - invalid channel number!")
    exit(1)

  if (testmode==0):
    c = mb(host=device_ip, auto_open=True, auto_close=True)
  if (type==ANA):
    if (testmode==0):
      regval = c.read_input_registers(regstart+((reqchan-1)*2), 2)
    elif (testmode==1):
      regval = [0x3f9e, 0x0419] # this should convert to 1.2345
      #regval=[0xbfb4, 0x6e00]
    if (regval is None):
      print("Error - no data received")
    elif (len(regval)==2):
      s=struct.pack('<H', regval[1])+struct.pack('<H', regval[0])
      u=struct.unpack('<f', s)
      return(u[0])
    else:
      print ("Error - unexpected data received") 
  elif (type==LOGIC):
    if (testmode==0):
      regval = c.read_discrete_inputs(regstart+(reqchan-1001), 1)
    elif (testmode==2):
      regval=[True]
    if (regval is None):
      print("Error - no logic chan data received")
    else:
      if (regval[0]==True):
        return(1)
      else:
        return(0)

def log(device_ip, reqchan, fname):
  with open(fname, 'a+') as fp:
    value = read(device_ip, reqchan)
    fp.write("{0:.6f}\r\n".format(value))
    fp.close()
    with open("time_"+fname, 'a+') as tfp:
      t = datetime.now()
      tfp.write(t.strftime("%H:%M:%S\n"))
      tfp.close()
    return (value)



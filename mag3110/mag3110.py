#!/usr/bin/python


 # =======================================================
 # Antonio Casini - Mag3110 magnetometer Class
 # =======================================================

import smbus
import time
from tk_i2c import Tk_I2C

OUT_X_MSB = 0x01
OUT_X_LSB = 0X02
OUT_Y_MSB = 0X03
OUT_y_LSB = 0X04
OUT_Z_MSB = 0X05
OUT_Z_LSB = 0X06

SYSMOD = 0x08
DIE_TEMP = 0X0f
CTRL_REG1 = 0x10
CTRL_REG2 = 0x11

OS_DR = 0x81      # Data sheet table 30-31 / 0x81 5Hz = ACTIVE mode
MRST_RAW = 0x82   # AUTO_MRST_EN + RAW    

ADDR_MAG = 0x0e
BUS = 1

class Raw_MAG3110(object):

   def __init__(self, bus_n=BUS, address=ADDR_MAG):
       "Raw data 16-Bit signed"
       self.i2c = Tk_I2C(address, smbus.SMBus(bus_n))
       self.address = address
       self.i2c.write8(CTRL_REG1, OS_DR)  # Operation modes 
       self.i2c.write8(CTRL_REG2, MRST_RAW)

   def read_Temp(self):
       "Read temp from register 8-bit signed"
       temp = self.i2c.readS8(DIE_TEMP)
       return temp

   def read_X16(self):
       "Read X mag from register 16-bit signed"
       Xmag = self.i2c.readS16(OUT_X_MSB)
       return Xmag

   def read_Y16(self):
       "Read Y mag from register 16-bit signed"
       Ymag = self.i2c.readS16(OUT_Y_MSB)
       return Ymag

   def read_Z16(self):
       "Read Z mag from register 16-bit signed"
       Zmag = self.i2c.readS16(OUT_Z_MSB)
       return Zmag

   def CurrSysMode(self):
       "Read Current system mode"
       sys = self.i2c.readU8(SYSMOD)
       return sys 

   def read_CTRLREG(self):
       "Read Control register 1 and 2"
       ctrl1 = self.i2c.readU8(CTRL_REG1)
       ctrl2 = self.i2c.readU8(CTRL_REG2)
       return ctrl1, ctrl2

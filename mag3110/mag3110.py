#!/usr/bin/python


 # =======================================================
 # Antonio Casini - Mag3110 magnetometer Class
 # =======================================================

import smbus
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
MRST_RAW = 0xA0   # AUTO_MRST_EN + RAW - 1010 0000 -
MRST_NRM = 0x80   # AUTO_MRST_EN + Normal Mode - data values are corrected by
                  # the user register values.    

ADDR_MAG = 0x0e   # I2C adrress of mag3110 device.
BUS = 1           # Check your system - For Raspberry Rev.2 = 1
CALTMP = 29.5     # In RTemp() offset temperature.

class Raw_MAG3110(object):

   def __init__(self, bus_n=BUS, address=ADDR_MAG):
       "Raw data 16-Bit signed"
       self.i2c = Tk_I2C(address, smbus.SMBus(bus_n))
       self.address = address
       self.i2c.write8(CTRL_REG1, 0x00)    # Set STANDBY mode - Read DataSheet :-)
       self.i2c.write8(CTRL_REG2, MRST_RAW)
       self.i2c.write8(CTRL_REG1, OS_DR)   # Operation modes 

   def StaAct(self, action):
       "Put mag3110 in ACTIVE (1) or STANDBY (0) mode"
       if action != 0 | action != 1:
         return False 
       register = self.i2c.readU8(CTRL_REG1)
       if (action!=0) & (action != (register & 0x01)):
         self.i2c.write8(CTRL_REG1, (register | 0x01))
         return 1
       elif action != (register & 0x01):
         self.i2c.write8(CTRL_REG1, (register & 0xfe))
         return 2
       else:
         return False       
    
   def rTemp(self):
       "Read temp from register 8-bit signed"
       temp = self.i2c.readS8(DIE_TEMP)
       return (temp + CALTMP)

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
       if sys == 0:
	 return "00: STANDBY mode. "
       elif sys == 1:
         return "01: ACTIVE mode, RAW data."
       elif sys == 2:
         return "10: ACTIVE mode, non-RAW user-corrected data."
       return False 

   def read_CTRLREG(self, reg):
       "Read Control register: 1 for REG1 and 2 for REG2."
       if reg == 1:
         ctrl1 = self.i2c.readU8(CTRL_REG1)
         return ctrl1
       elif reg == 2:
         ctrl2 = self.i2c.readU8(CTRL_REG2)
         if ctrl2 == 16:
           return "Mag_RST - Magnetic Sensor Reset"
         elif ctrl2 == 32:
           return "RAW mode - No user data correction"
         else: 
           return ctrl2 
       return False


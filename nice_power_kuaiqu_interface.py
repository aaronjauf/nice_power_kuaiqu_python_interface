
# pip3 install pyserial


#########################################################################
# definitions + init
usbDevWithPath = "/dev/ttyUSB0"

import serial

ser = serial.Serial(port=usbDevWithPath, baudrate=9600, timeout=1)
ser.flush()

FORMAT_SIX_DIGITS = "{:07.3f}" # pad zeros, 6 digits in total (without counting "."), 3 decimal places

def psu_write(cmd):
  ser.write(cmd.encode())

def psu_read_decode():
  data = ser.read_until(b">")
  cv_mode = data[1] == '1' # 1 is constant voltage mode, C is constant current mode (PSU off is also constant current mode)
  val = float(data[3:9].decode())*1e-3
  return val
  
def psu_read_ok():
  data = ser.read_until(b">").decode()
  if 'OK' in data:
    return 1
  else:
    return 0

def psu_read_raw():
  data = ser.read_until(b">").decode()
  return data

def get_voltage(): # actual voltage (not the voltage set)
  cmd = "<02000000000>"
  psu_write(cmd)
  return psu_read_decode()

def get_current(): # actual current (not the current set)
  cmd = "<04000000000>"
  psu_write(cmd)
  return psu_read_decode()

def set_psu_remote(): # remote control mode (needed for set commands)
  cmd = "<09100000000>"
  psu_write(cmd)
  cmd = "<01004580000>"
  psu_write(cmd)
  cmd = "<03006920000>"
  psu_write(cmd)
  return psu_read_ok()

def set_psu_local(): # local control mode
  cmd = "<09200000000>"
  psu_write(cmd)
  return psu_read_ok()

def set_output_on():
  cmd = "<07000000000>"
  ser.write(cmd.encode())
  return psu_read_ok()
  
def set_output_off():
  cmd = "<08000000000>"
  ser.write(cmd.encode())
  return psu_read_ok()

def set_voltage(val):
  val_formatted = FORMAT_SIX_DIGITS.format(val).replace(".", "")
  cmd = "<01"+val_formatted+"000>"
  ser.write(cmd.encode())
  return psu_read_ok()

def set_current(val):
  val_formatted = FORMAT_SIX_DIGITS.format(val).replace(".", "")
  cmd = "<03"+val_formatted+"000>"
  ser.write(cmd.encode())
  return psu_read_ok()

#########################################################################
# main


print(get_voltage())
print(get_current())

set_psu_remote()
set_output_off()
set_voltage(8.0)
set_current(12.0)
set_psu_local()



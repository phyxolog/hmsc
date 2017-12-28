import logging
import struct
import ftypes
import helper

class BMP:
  def __init__(self, file=None):
    self.file = file
    self.type = ftypes.BITMAP
    self.utype = self.type.upper()

  def scan(self, data, current_offset=0, buffer_size=0, callback=None):
    index = data.find(b"B")
    buffer = bytearray(9)
    offsets = []

    while index != -1:
      offset = current_offset + index
      
      self.file.seek(offset)
      self.file.readinto(buffer)
      if list(buffer[0:2]) == [0x42, 0x4D] and list(buffer[5:9]) == [0x00, 0x00, 0x00, 0x00]:
        size, = struct.unpack('i', buffer[2:6])
        offsets.append({"type": self.type, offset: offset, size: size})
        if callback != None:
          callback(self.utype, offset, size)

      index = data.find(b"B", index + 1)
    
    self.file.seek(current_offset + buffer_size)

    return offsets
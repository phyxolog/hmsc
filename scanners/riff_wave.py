import logging
import struct
import ftypes
import helper

class RIFF_WAVE:
  def __init__(self, file=None, callback=None):
    self.file = file
    self.type = ftypes.RIFF_WAVE
    self.utype = self.type.upper()
    self.callback = callback

  def scan(self, data, current_offset=0, buffer_size=0):
    index = data.find(b"R")
    buffer = bytearray(12)
    offsets = []

    while index != -1:
      offset = current_offset + index

      self.file.seek(offset)
      self.file.readinto(buffer)
      if list(buffer[0:4]) == [0x52, 0x49, 0x46, 0x46] and list(buffer[8:12]) == [0x57, 0x41, 0x56, 0x45]:
        riff, size, fformat = struct.unpack('<4sI4s', buffer)
        offsets.append({"type": self.type, "offset": offset, "size": size})
        if self.callback != None:
          self.callback(self.utype, offset, size)

      index = data.find(b"R", index + 1)

    self.file.seek(current_offset + buffer_size)

    return offsets

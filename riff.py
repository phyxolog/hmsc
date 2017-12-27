import logging
import struct

class RIFF:
  def __init__(self, file=None):
    self.file = file

  def scan(self, data, current_offset=0, buffer_size=0):
    index = data.find(b"R")
    buffer = bytearray(12)
    offsets = []

    while index != -1:
      offset = current_offset + index
      offsets.append(offset)
      self.file.seek(offset)
      self.file.readinto(buffer)
      # logging.debug("Found RIFF WAVE at @{0}".format(hex(offset)))
      riff, size, fformat = struct.unpack('<4sI4s', buffer)
      if "".join(map(chr, riff)) == "RIFF":
        print(current_offset)
      # print("Riff: %s, Chunk Size: %i, format: %s" % ("".join(map(chr, riff)), size, fformat))      
      index = data.find(b"R", index + 1)
    
    self.file.seek(current_offset + buffer_size)

    return offsets
import logging

class RIFF:
  def __init__(self, file=None):
    self.file = file

  def scan(self, data, current_offset=0):
    index = data.find(b"R")
    buffer = bytearray(12)
    offsets = []

    while index != -1:
      offset = current_offset + index
      offsets.append(offset)
      self.file.seek(offset)
      self.file.readinto(buffer)
      logging.debug("Found RIFF WAVE at @{0}".format(hex(offset)))
      index = data.find(b"R", index + 1)
    
    self.file.seek(current_offset)

    return offsets
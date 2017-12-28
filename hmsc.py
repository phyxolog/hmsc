import sys
import os
import io
import itertools
import logging

import helper

from riff import RIFF
from bmp import BMP

# Configurate logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] --> %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

class HMSC:
  def __init__(self, file_name, buffer_size=65536):
    self.file = io.open(file_name, "rb")
    self.buffer_size = buffer_size
    self.current_offset = 0
    self.file_size = os.path.getsize(file_name)
    self.offsets = []
    self.finders = [RIFF(file=self.file), BMP(file=self.file)]

  def log_callback(self, type, offset, size):
    logging.debug("Found {0} at @{1}, {2}".format(type, hex(offset).upper(), helper.humn_size(size)))

  def run(self):
    logging.debug("Running file scanner...")
    read_bytes = 0
    if self.file_size < self.buffer_size:
      self.buffer_size = self.file_size

    self.buffer = bytearray(self.buffer_size)

    while read_bytes < self.file_size:
      if read_bytes + self.buffer_size > self.file_size:
        self.buffer_size = self.file_size - read_bytes
        self.buffer = bytearray(self.buffer_size)

      numread = self.file.readinto(self.buffer)
      if numread == self.buffer_size:
        self.current_offset = read_bytes
        for finder in self.finders:
          self.offsets += finder.scan(self.buffer, self.current_offset, self.buffer_size, self.log_callback)
      else:
        logging.error("Error reading from file")
        break

      read_bytes += self.buffer_size

    if read_bytes == self.file_size:
      logging.debug("The file is completely scanned... Preparing for compress")
    else:
      logging.error("An error occurred while scanning (file not completely scanned)")

print("HMSC [Hyper Media Streams Compressor] v0.0.1 pre-alpha")
print("by phyxolog (https://github.com/phyxolog)\n")

hmsc = HMSC(file_name="media.data")
hmsc.run()
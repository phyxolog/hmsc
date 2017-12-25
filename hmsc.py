import os
import io
import itertools
import logging
import sys

from bm import BMSearch

# Configurate logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] --> %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

class Finder:
    def __init__(self, file_name, buffer_size=65536):
        self.file = io.open(file_name, "rb")
        self.buffer_size = buffer_size
        self.current_offset = 0
        self.file_size = os.path.getsize(file_name)
        self.offsets = []

    def find_riff_wave_offsets(self, data):
      print(data.find(b"R"))
      # print(BMSearch(data, 0x52))
      return []

    def find_offsets(self, data):
      riff_wave_offsets = self.find_riff_wave_offsets(data)
      self.offsets = sum([self.offsets, riff_wave_offsets])

    def run(self):
      logging.debug("Running file scanner...")
      read_bytes = 0
      if self.file_size <= self.buffer_size:
        self.buffer_size = self.file_size

      self.buffer = bytearray(self.buffer_size)

      while read_bytes < self.file_size:
        if read_bytes + self.buffer_size > self.file_size:
          self.buffer_size = self.file_size - read_bytes
          self.buffer = bytearray(self.buffer_size)

        numread = self.file.readinto(self.buffer)
        if numread == self.buffer_size:
          self.current_offset = read_bytes
          self.find_offsets(self.buffer)
        else:
          logger.error("Error reading from file")
          break

        read_bytes += self.buffer_size

      if read_bytes == self.file_size:
        logging.debug("The file is completely scanned")
      else:
        logging.error("An error occurred while scanning (file not completely scanned)")

print("HMSC [Hyper Media Streams Compressor] v0.0.1 pre-alpha")
print("by phyxolog (https://github.com/phyxolog)\n")

finder = Finder(file_name="music.data")
finder.run()

import os
import io
import itertools
import logging
import sys

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
        
        self.file_size = os.path.getsize(file_name)
        self.offsets = []

    def find_offsets(data):
        pass

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
        print(numread)

        read_bytes += self.buffer_size

      if read_bytes == self.file_size:
        logging.debug("The file is completely scanned")
      else:
        logging.error("An error occurred while scanning (file not completely scanned)")

print("HMSC [Hyper Media Streams Compressor] v0.0.1 pre-alpha")
print("by phyxolog (https://github.com/phyxolog)\n")

finder = Finder(file_name="music.data")
finder.run()

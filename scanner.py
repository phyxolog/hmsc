import sys
import os
import io
import itertools
import logging
import glob
import imp

import helper

class Scanner:
  def __init__(self, file_name, buffer_size=65536):
    self.file = io.open(file_name, "rb")
    self.buffer_size = buffer_size
    self.current_offset = 0
    self.file_size = os.path.getsize(file_name)
    self.offsets = []
    self.scanners = []

    # Init scanners
    scanner_scripts = glob.glob("scanners/*.py")
    for script in scanner_scripts:
      module_name = os.path.basename(script).split(".")[0].upper()
      module = imp.load_source(module_name, script)
      self.scanners.append(getattr(module, module_name)(file=self.file))

  def log_callback(self, type, offset, size):
    logging.debug("Found {0} at @{1}, {2}".format(type, hex(offset).upper(), helper.humn_size(size)))

  def run(self):
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
        for finder in self.scanners:
          self.offsets += finder.scan(self.buffer, self.current_offset, self.buffer_size, self.log_callback)
      else:
        logging.error("Error reading from file")
        break

      read_bytes += self.buffer_size

    if read_bytes == self.file_size:
      logging.debug("The file is completely scanned")
      return self.offsets
    else:
      logging.error("An error occurred while scanning (file not completely scanned)")
      return None
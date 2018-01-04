import sys
import io
import os
import logging
import helper

import ftypes

class Extractor:
  def __init__(self, file_name, results, extract_dir):
    self.file = io.open(file_name, "rb")
    self.file_size = os.path.getsize(file_name)
    self.extract_dir = extract_dir
    self.results = results
    self.__create_extract_dir()

  def __create_extract_dir(self):
    if self.extract_dir == None:
      self.extract_dir = "extract_data"

    if not os.path.exists(self.extract_dir):
      os.makedirs(self.extract_dir)

  def __gen_file_name(self, i, result):
    return ".".join([os.path.join(self.extract_dir, str(i).zfill(10)), ftypes.type_to_ext(result["type"])])    

  def __extract(self, offset, size, type, out_file_name):
    logging.debug("Extracting {0} to {1}, {2}".format(type.upper(), out_file_name, helper.humn_size(size)))

    read_bytes = 0
    buffer_size = 131072 # 128kB
    buffer = bytearray(buffer_size)
    file = io.open(out_file_name, "wb")
    self.file.seek(offset)

    if size < buffer_size:
      buffer_size = size
      buffer = bytearray(buffer_size)

    while read_bytes < size:
      if read_bytes + buffer_size > size:
        buffer_size = size - read_bytes
        buffer = bytearray(buffer_size)

      self.file.readinto(buffer)
      file.write(buffer)
      read_bytes += buffer_size

    if read_bytes != size:
      logging.error("Error extracting {0}, size: {1}, at {2}".format(type.upper(), helper.humn_size(size), hex(offset).upper()))

    file.close()

  def run(self):
    i = 1
    for result in self.results:
      self.__extract(result["offset"], result["size"], result["type"], self.__gen_file_name(i, result))
      i += 1
    self.file.close()

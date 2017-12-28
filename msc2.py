import sys
import os
import io
import itertools
import logging
import argparse

import scanner
import compressor
import extractor
import insertor

# Configurate logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] --> %(message)s")
ch.setFormatter(formatter)
root.addHandler(ch)

if __name__ == "__main__":
  description = "MSC2 [Media Streams Compressor 2] v0.0.1 pre-alpha (https://github.com/phyxolog)"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("--option", dest="option", action="store", choices=["c", "s", "e"], required=True, help="c - compress, s - scan, e")
  parser.add_argument("file", metavar="file", type=str, help="path for file to processing")
  args = parser.parse_args()

  logging.info("Running scanner...")

  scanner = scanner.Scanner(file_name=args.file)
  results = scanner.run()

  if results == None:
    sys.exit(1)

  if args.option == "c":
    logging.info("Compressing...")
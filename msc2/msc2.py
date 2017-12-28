import sys
import os
import io
import itertools
import logging

import scanner
import compressor
import extractor
import insertor

# Configurate logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] --> %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

print("HMSC [Hyper Media Streams Compressor] v0.0.1 pre-alpha")
print("by phyxolog (https://github.com/phyxolog)\n")

logging.info("Running scanner...")

scanner = scanner.Scanner(file_name="data/media.data")
results = scanner.run()
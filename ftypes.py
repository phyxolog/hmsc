RIFF_WAVE = "riff_wave"
BITMAP = "bitmap"

EXT = {}
EXT[RIFF_WAVE] = "wav"
EXT[BITMAP] = "bmp"

def type_to_ext(type):
  return EXT[type]
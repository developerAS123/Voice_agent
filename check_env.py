import sys
import numpy as np, scipy, sounddevice as sd, soundfile as sf, matplotlib

print("Python     :", sys.version.split()[0])
print("numpy      :", np.__version__)
print("scipy      :", scipy.__version__)
print("soundfile  :", sf.__version__)
print("matplotlib :", matplotlib.__version__)
print("\nAudio devices:")
print(sd.query_devices())
print("\nDefault (input, output):", sd.default.device)
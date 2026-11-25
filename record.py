import numpy as np
import sounddevice as sd # Handles real-time audio I/O
import soundfile as sf # Reads/writes WAV files

SR=16000 # # sample rate 16 kHz is the standard for speech models
SECONDS=5

input(f"Press Enter then speak for {SECONDS} seconds: ")
audio=sd.rec(int(SECONDS*SR), samplerate=SR, channels=1, dtype="float32") # total number of samples to capture , Mono recording (one microphone channel), Audio samples stored as 32-bit floats in the range [-1.0, 1.0]
sd.wait()
audio=audio[:,0] # takes column 0, flattening it to a 1-D array of shape (80000,). Most audio libraries (and speech models) expect 1-D mono arrays.
sf.write("data/test.wav", audio, SR, subtype="PCM_16")

rms = float(np.sqrt(np.mean(audio ** 2))) # root mean square average loudness of the signal
peak = float(np.max(np.abs(audio))) # the loudest single sample in the recording
dbfs = 20 * np.log10(rms + 1e-12)
print(f"samples={len(audio)}  duration={len(audio)/SR:.2f}s")
print(f"rms={rms:.4f}  peak={peak:.3f}  loudness={dbfs:.1f} dBFS")

if peak >= 0.99:
    print("WARNING: clipping. Move away from the mic or lower the input volume.")

if dbfs < -45:
    print("WARNING: very quiet. Raise the mic level or speak closer.")

print("Playing back...")
sd.play(audio, SR)
sd.wait()
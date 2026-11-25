import matplotlib
matplotlib.use("Agg")                  # no GUI needed, saves to a file
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

audio, sr = sf.read("data/test.wav", dtype="float32")
t = np.arange(len(audio)) / sr

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax1.plot(t, audio, linewidth=0.5)
ax1.set_ylabel("Amplitude")
ax1.set_title("Waveform")
ax2.specgram(audio, NFFT=512, Fs=sr, noverlap=256, cmap="magma")
ax2.set_ylabel("Frequency (Hz)")
ax2.set_xlabel("Time (s)")
ax2.set_title("Spectrogram")
plt.tight_layout()
plt.savefig("docs/audio_view.png", dpi=120)
print("saved docs/audio_view.png")
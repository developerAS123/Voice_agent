import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly # high-quality polyphase resampling with a built-in anti-aliasing / anti-imaging filter

audio, sr = sf.read("data/test.wav", dtype="float32")

# 16 kHz -> 8 kHz (resample_poly includes an anti-aliasing filter)
low = resample_poly(audio, up=1, down=2) # output rate is input_rate × up / down = 16000 × 1/2 = 8000 Hz. Half the samples
sf.write("data/test_8k.wav", low, 8000)

# mu-law companding (G.711 idea): 8-bit logarithmic encoding used by phone systems
def mulaw_encode(x, mu=255):
    x = np.clip(x, -1, 1)
    y = np.sign(x) * np.log1p(mu * np.abs(x)) / np.log1p(mu)
    return ((y + 1) / 2 * mu + 0.5).astype(np.uint8)

def mulaw_decode(q, mu=255):
    y = q.astype(np.float32) / mu * 2 - 1
    return np.sign(y) * ((1 + mu) ** np.abs(y) - 1) / mu

phone = mulaw_decode(mulaw_encode(low))
print("8 kHz mu-law size:", len(low), "bytes (1 byte per sample) vs",
      len(audio) * 2, "bytes for 16 kHz int16")

# Upsample back to 16 kHz so you can hear what an STT model gets from a phone line
phone_16k = resample_poly(phone, up=2, down=1)
sf.write("data/test_phone.wav", phone_16k, 16000)

print("Original..."); sd.play(audio, sr); sd.wait()
print("Phone quality..."); sd.play(phone_16k, 16000); sd.wait()
# The phone version sounds muffled because everything above 4 kHz is gone. This is why telephony STT is harder and less accurate.
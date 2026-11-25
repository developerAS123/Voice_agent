import numpy as np
import soundfile as sf

audio, sr = sf.read("data/test.wav", dtype="float32")
print("sample rate:", sr, "| samples:", len(audio))

# float32 [-1, 1] -> int16 PCM bytes (what WebSocket, WebRTC and phone systems carry)
pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
print("bytes:", len(pcm), "| bytes/sec:", len(pcm) / (len(audio) / sr))   # expect 32000

# int16 bytes -> float32 again, and check how small the quantization error is
back = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
print("max round-trip error:", float(np.max(np.abs(audio - back))))

def frames(pcm_bytes, ms=20, sample_rate=16000):
    size = int(sample_rate * ms / 1000) * 2            # 2 bytes per int16 sample
    for i in range(0, len(pcm_bytes) - size + 1, size):
        yield pcm_bytes[i:i + size]

frame_list = list(frames(pcm))
print("frame size (bytes):", len(frame_list[0]))        # expect 640
print("number of 20 ms frames:", len(frame_list))       # about 250 for 5 s
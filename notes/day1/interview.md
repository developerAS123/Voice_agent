# Q1. Compare a cascaded voice agent with a speech-to-speech model. When would you choose each?
A cascade chains VAD, STT, LLM and TTS as separate components. A speech-to-speech model takes audio in and produces audio out directly.
The cascade is more controllable and debuggable. You can inspect the transcript, swap any component, use strong text LLMs with tool calling, add guardrails, use custom voices and manage cost. Its drawbacks are higher latency because the stages add up, and lost paralinguistic information such as tone and emotion.
Speech-to-speech gives lower latency, more natural conversation, better interruption handling and preserved prosody. Its drawbacks are less control, harder observability, trickier tool use and often higher cost.
I would choose a cascade for regulated or tool-heavy workflows like booking or banking, where auditability matters. I would choose speech-to-speech for companion-style or highly conversational products. Many teams use a hybrid.

# Q2. Why is speech commonly processed at 16 kHz mono 16-bit, and how many bytes per second is that?
Speech information is mostly below 8 kHz. By the Nyquist theorem, a 16 kHz sample rate captures frequencies up to 8 kHz, which is enough for intelligible speech and for models like Whisper. Mono is enough because speech is a single source, and 16-bit gives adequate dynamic range.
Data rate: 16,000 samples/s x 2 bytes x 1 channel = 32,000 bytes/s. A 20 ms frame is 320 samples, which is 640 bytes. Telephone audio is lower still, at 8 kHz with 8-bit mu-law, which is 8,000 bytes/s.

# Q3. What latency should a voice agent target, and where does the time go?
Humans leave about 200 to 300 ms between turns. Practically, a voice-to-voice response under about one second feels natural, and above about 1.5 to 2 seconds feels broken.
The time is spent on: endpointing (waiting to be sure the user finished, often 300 to 700 ms), STT, LLM time-to-first-token, generating the first sentence, TTS time-to-first-byte, and network plus audio buffering. I would instrument each stage, track p50 and p95, and optimize the largest contributor first, using techniques such as streaming, smaller models, warm models and shorter endpointing.

# Q4. What is the difference between WAV, PCM, mu-law and Opus?
PCM is the raw, uncompressed sequence of samples. WAV is a file container that wraps PCM (and sometimes other formats) with a header describing sample rate and channels. Mu-law (G.711) is a simple logarithmic 8-bit companding used by traditional telephony at 8 kHz, which gives about 2:1 compression over 16-bit and good quality for speech. Opus is a modern lossy codec with low latency and variable bitrate, and it is the standard codec in WebRTC.
In practice: phone streams arrive as mu-law, WebRTC uses Opus, and your STT model wants 16 kHz float or int16 PCM, so you decode and resample at the edges of your system.
#Q5. Why do real-time audio systems use small frames, such as 20 ms, and what is a jitter buffer?
Small frames keep latency low because you do not wait for a large chunk before processing or sending. They also let VAD and interruption logic react quickly. The trade-off is more packets and per-packet overhead, so 10 to 40 ms is the usual range, with 20 ms most common.
Networks deliver packets with variable delay (jitter) and sometimes out of order. A jitter buffer holds a few packets and releases them at a steady pace so playback is smooth. A bigger buffer is more robust but adds latency, so the buffer size is a deliberate latency-vs-quality trade-off.

# Q5. Why do real-time audio systems use small frames, such as 20 ms, and what is a jitter buffer?
Small frames keep latency low because you do not wait for a large chunk before processing or sending. They also let VAD and interruption logic react quickly. The trade-off is more packets and per-packet overhead, so 10 to 40 ms is the usual range, with 20 ms most common.
Networks deliver packets with variable delay (jitter) and sometimes out of order. A jitter buffer holds a few packets and releases them at a steady pace so playback is smooth. A bigger buffer is more robust but adds latency, so the buffer size is a deliberate latency-vs-quality trade-off.
# Target budget in milliseconds for one conversational turn. Edit and experiment.
budget = {
    "endpointing (silence wait)": 500,
    "STT": 250,
    "LLM time to first sentence": 400,
    "TTS time to first byte": 150,
    "network + audio buffering": 100,
}
total = sum(budget.values())
for stage, ms in budget.items():
    print(f"{stage:32s}{ms:5d} ms  {'#' * (ms // 25)}")
print(f"{'TOTAL voice-to-voice':32s}{total:5d} ms")
print("OK for natural conversation" if total <= 1200 else "Too slow: cut something")
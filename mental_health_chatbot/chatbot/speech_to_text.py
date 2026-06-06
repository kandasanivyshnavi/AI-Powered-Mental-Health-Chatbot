import whisper
import sounddevice as sd
import numpy as np
import wave

# Load Whisper model once
model = whisper.load_model("small")

def record_audio(filename="recorded_audio.wav", duration=5, samplerate=16000):
    print("🎤 Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    print("✅ Recording complete!")

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    return filename

def transcribe_audio(audio_path):
    print("📝 Transcribing...")
    result = model.transcribe(audio_path)
    print("💬 Transcription:", result["text"])
    return result["text"]

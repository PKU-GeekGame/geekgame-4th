import opuslib
import wave
import pickle

decoder = opuslib.Decoder(48000, 2)
with open('udp14_opus.pkl', 'rb') as f, wave.open('udp14.wav', 'wb') as wav:
    opus = pickle.load(f)
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.setframerate(48000)
    for data in opus:
        if not data:
            break
        pcm = decoder.decode(data, frame_size=960)
        wav.writeframes(pcm)

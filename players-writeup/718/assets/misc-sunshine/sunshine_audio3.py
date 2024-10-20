import wave
import numpy as np
from scipy.fft import fft

for i in range(1, 17):
    wav_file = wave.open(f'udp14_{i}.wav', 'r')
    n_frames = wav_file.getnframes()
    framerate = wav_file.getframerate()

    frames = wav_file.readframes(n_frames)
    audio_data = np.frombuffer(frames, dtype=np.int16)

    frequencies = fft(audio_data)

    frequencies_magnitude = np.abs(frequencies)
    frequencies = np.fft.fftfreq(len(frequencies_magnitude), 1.0 / framerate)

    half_length = len(frequencies_magnitude) // 2
    frequencies = frequencies[:half_length]
    frequencies_magnitude = frequencies_magnitude[:half_length]

    peak_indices = np.argsort(frequencies_magnitude)[-2:]
    peak_frequencies = frequencies[peak_indices]
    peak_magnitudes = frequencies_magnitude[peak_indices]
    peak_frequencies = [f * 2 for f in peak_frequencies]

    print(f"{peak_frequencies}")

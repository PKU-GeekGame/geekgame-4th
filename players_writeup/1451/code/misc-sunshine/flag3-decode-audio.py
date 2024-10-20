import opuslib
import opuslib.api.decoder as decoder
import wave


sample_rate = 48000
channels = 2
decoder_state = decoder.create_state(sample_rate, channels)

pcm_output = bytearray()

for i in range(2117 + 1):
    with open(f"./audioout/{i}.dat", 'rb') as f:
        opus_data = f.read()
    frame_size = 480
    pcm_frame = decoder.decode(decoder_state, opus_data, len(opus_data), frame_size, False)
    pcm_output.extend(pcm_frame)


output_file = wave.open("output.wav", "wb")
output_file.setnchannels(channels)
output_file.setsampwidth(2)
output_file.setframerate(sample_rate)
output_file.writeframes(pcm_output)

# 关闭文件
output_file.close()

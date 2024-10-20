import sys
import argparse
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


class DtmfGenerator:
    DTMF_TABLE = {
        "1": np.array([1209, 697]),
        "2": np.array([1336, 697]),
        "3": np.array([1477, 697]),
        "A": np.array([1633, 697]),
        "4": np.array([1209, 770]),
        "5": np.array([1336, 770]),
        "6": np.array([1477, 770]),
        "B": np.array([1633, 770]),
        "7": np.array([1209, 852]),
        "8": np.array([1336, 852]),
        "9": np.array([1477, 852]),
        "C": np.array([1633, 852]),
        "*": np.array([1209, 941]),
        "0": np.array([1336, 941]),
        "#": np.array([1477, 941]),
        "D": np.array([1633, 941]),
    }

    def __init__(
        self,
        phone_number: str,
        Fs: float,
        time: float,
        delay: float,
        amp: float,
    ):
        self.signal = self.compose(phone_number, Fs, time, delay, amp)

    def __dtmf_function(
        self, number: str, Fs: float, time: float, delay: float, amp: float
    ) -> np.array:
        """
        Function which generate DTMF tone (samples) to one specific character
        and its delay

        :number: Represents the character to be converted to DTMF tone
        :Fs: Sample frequency used to generate the signal in Hz
        :time: Duration of each tone in seconds
        :delay: Duration of delay between each tone in seconds

        :return: Array with samples to the DTMF tone and delay
        """

        time_tone = np.arange(0, time, (1 / Fs))
        time_delay = np.arange(0, delay, (1 / Fs))

        tone_samples = amp * (
            np.sin(2 * np.pi * self.DTMF_TABLE[number][0] * time_tone)
            + np.sin(2 * np.pi * self.DTMF_TABLE[number][1] * time_tone)
        )
        delay_samples = np.sin(2 * np.pi * 0 * time_delay)

        return np.append(tone_samples, delay_samples)

    def compose(
        self,
        phone_number: str,
        Fs: float,
        time: float,
        delay: float,
        amp: float,
    ) -> np.array:
        """
        Function which generate DTMF tones (samples) to compose a signal
        representing the phone number

        :number: Represents the number to be converted to DTMF tone
        :Fs: Sample frequency used to generate the signal in Hz
        :time: Duration of each tone in seconds
        :delay: Duration of delay between each tone in seconds

        :return: Array with samples to the DTMF tone and delay
        """

        signal = np.array([])

        for number in phone_number:
            tone_delay_signal = self.__dtmf_function(number, Fs, time, delay, amp)
            signal = np.append(signal, tone_delay_signal)

        return signal

    def test_signal(
        self,
        filename: str,
        phone_number: str,
        Fs: float,
        time: float,
        delay: float,
    ):
        """
        Function which debug DTMF tones generated in the WAV file plotting their frequencies

        :filename: WAV filename to debug
        :phone_number: Phone number to verify
        :Fs: Sample frequency used to generate the signal in Hz
        :time: Duration of each tone in seconds
        :delay: Duration of delay between each tone in seconds

        :return: A graph with tones and their frequencies
        """

        rate, signal = wav.read(filename)
        n_columns_axis = np.ceil(np.sqrt(len(phone_number))).astype(int)
        n_rows_axis = np.ceil(len(phone_number) / n_columns_axis).astype(int)
        fig, axis = plt.subplots(n_rows_axis, n_columns_axis)
        fig.suptitle("DTMF tones frequencies")
        for i in np.arange(0, 2 * len(phone_number), 2):
            self.__test_tone(
                signal[i * int(Fs * time) : (i + 1) * int(Fs * time)],
                Fs,
                time,
                delay,
                axis,
                n_rows_axis,
                n_columns_axis,
                (i / 2) + 1,
            )
        plt.tight_layout()
        plt.show()

    def __test_tone(
        self,
        signal: np.array,
        Fs: float,
        time: float,
        delay: float,
        axis,
        n_rows_axis: int,
        n_columns_axis: int,
        index: int,
    ):
        """
        Function which debug one DTMF tone generated in the WAV file plotting its frequency

        :signal: Array with the tone to be plotted
        :Fs: Sample frequency used to generate the signal in Hz
        :time: Duration of each tone in seconds
        :delay: Duration of delay between each tone in seconds
        :axix: Axis of matplotlib to plot the tone
        :n_rows_axis: Number of rows into subplot of matplotlib
        :n_columns_axis: Number of columns into subplot of matplotlib
        :index: Index of the tone

        :return: A graph with one tone and its frequencies
        """

        tone_fft = np.fft.fft(signal, Fs)
        time_tone = np.arange(0, time + (1 / Fs), (1 / Fs))
        freq = np.fft.fftfreq(len(tone_fft), time_tone[1] - time_tone[0])

        row = int(np.ceil(index / n_columns_axis))
        column = int(index - ((row - 1) * n_columns_axis))
        axis[row - 1, column - 1].plot(freq, np.abs(tone_fft))
        axis[row - 1, column - 1].set_title("Tone {}".format(int(index)))
        axis[row - 1, column - 1].set_xlabel("Frequency (Hz)")
        axis[row - 1, column - 1].set_ylabel("Amplitude")
        axis[row - 1, column - 1].set_xlim([600, 2000])


def main():
    try:
        parser = argparse.ArgumentParser(description="DTMF generator to phone numbers.")
        parser.add_argument(
            "-p",
            "--phonenumber",
            required=True,
            type=str,
            help="Phone number to encoder (Only numbers)",
        )
        parser.add_argument(
            "-f",
            "--samplefrequency",
            required=True,
            type=int,
            help="Sample Frequency (Hz)",
        )
        parser.add_argument(
            "-t",
            "--toneduration",
            required=True,
            type=float,
            help="Tones duration (s)",
        )
        parser.add_argument(
            "-s",
            "--silence",
            required=True,
            type=float,
            help="Silence duration between tones duration (s)",
        )
        parser.add_argument(
            "-a",
            "--amplitude",
            required=True,
            type=float,
            help="Amplitude of the sine waves",
        )
        parser.add_argument(
            "-o",
            "--output",
            required=True,
            type=str,
            help="Filename output for WAV file",
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Enable FFT graph of each tone (character) to debug",
        )
        args = parser.parse_args()

        dtmf = DtmfGenerator(
            args.phonenumber,
            args.samplefrequency,
            args.toneduration,
            args.silence,
            args.amplitude,
        )
        wav.write(args.output, args.samplefrequency, dtmf.signal)
        if args.debug:
            dtmf.test_signal(
                args.output,
                args.phonenumber,
                args.samplefrequency,
                args.toneduration,
                args.silence,
            )
    except SystemExit:
        pass


if __name__ == "__main__":
    main()

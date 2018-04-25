from threading import Thread
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "/audio.wav"


class AudioRecorderThread(Thread):

    session_path = None
    audio = None
    stream = None
    recording = False
    waveFile = None

    def __init__(self, session_path):
        super(AudioRecorderThread, self).__init__()
        self.session_path=session_path
        self.audio = pyaudio.PyAudio()
        self.waveFile = wave.open(self.session_path + WAVE_OUTPUT_FILENAME, "wb")
        self.waveFile.setnchannels(CHANNELS)
        self.waveFile.setframerate(RATE)

    def run(self):
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)
        self.waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        self.recording=True
        while self.recording:
            data = self.stream.read(CHUNK)
            self.waveFile.writeframes(data)
        self.waveFile.close()
        self.stop()
        return


    def stop(self):
        self.recording=False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.stream = None
        self.waveFile = None
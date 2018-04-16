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
    frames = []

    def __init__(self, session_path):
        super(AudioRecorderThread, self).__init__()
        self.session_path=session_path
        self.audio = pyaudio.PyAudio()

    def run(self):
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)
        self.recording=True
        while self.recording:
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        self.stop()
        return


    def stop(self):
        self.recording=False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        waveFile = wave.open(self.session_path + WAVE_OUTPUT_FILENAME, "wb")
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()
        self.audio.terminate()
        self.frames = []
        self.stream = None
import sounddevice as sd
import soundfile as sf
import queue
import threading
import uuid


class AudioRecorder:
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.recording = False
        self.q = queue.Queue()
        self.thread = None
        self.filename = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def _record(self):
        with sf.SoundFile(
            self.filename,
            mode="w",
            samplerate=self.samplerate,
            channels=self.channels,
        ) as file:
            with sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                callback=self._callback,
            ):
                while self.recording:
                    file.write(self.q.get())

    def start(self):
        self.filename = f"recording_{uuid.uuid4()}.wav"
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        self.thread.join()
        return self.filename
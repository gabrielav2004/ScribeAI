import time
import os
from sound_utils import AudioRecorder
from transcriber import GroqTranscriber


class RealtimeTranscriber:
    def __init__(self, chunk_duration=5, output_type="text"):
        self.chunk_duration = chunk_duration
        self.output_type = output_type
        self.recorder = AudioRecorder()
        self.transcriber = GroqTranscriber()
        self.running = False

    def start(self):
        self.running = True
        print("Real-time transcription started... (Ctrl+C to stop)")

        try:
            while self.running:
                self.recorder.start()
                time.sleep(self.chunk_duration)

                file_path = self.recorder.stop()

                result = self.transcriber.transcribe_file(
                    file_path,
                    output_type=self.output_type,
                )

                if self.output_type == "verbose_json":
                    for segment in result.segments:
                        print(
                            f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}"
                        )
                else:
                    if result.strip():
                        print("You said:", result)

                # Optional cleanup
                os.remove(file_path)

        except KeyboardInterrupt:
            self.stop()
            print("\nReal-time transcription stopped.")

    def stop(self):
        self.running = False
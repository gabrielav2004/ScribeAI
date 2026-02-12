from transcriber import GroqTranscriber
from sound_utils import AudioRecorder
from rt_transcribe import RealtimeTranscriber


def static_file_mode():
    path = input("Enter audio file path: ")
    output_type = input("Output type (text / verbose_json): ") or "text"

    transcriber = GroqTranscriber()
    result = transcriber.transcribe_file(path, output_type=output_type)

    if output_type == "verbose_json":
        for segment in result.segments:
            print(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}")
    else:
        print("\nTranscription:\n", result)


def live_record_mode():
    recorder = AudioRecorder()
    transcriber = GroqTranscriber()

    input("Press Enter to start recording...")
    recorder.start()

    input("Press Enter to stop recording...")
    file_path = recorder.stop()

    result = transcriber.transcribe_file(file_path)

    print("\nTranscription:\n", result)


def realtime_mode():
    output_type = input("Output type (text / verbose_json): ") or "text"
    rt = RealtimeTranscriber(chunk_duration=5, output_type=output_type)
    rt.start()


if __name__ == "__main__":
    print("Choose Mode:")
    print("1 - Static File")
    print("2 - Live Record Then Transcribe")
    print("3 - Real-Time (Chunk-Based)")

    choice = input("Enter choice: ")

    if choice == "1":
        static_file_mode()
    elif choice == "2":
        live_record_mode()
    elif choice == "3":
        realtime_mode()
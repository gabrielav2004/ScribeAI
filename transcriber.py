import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqTranscriber:
    def __init__(self, api_key=None, model="whisper-large-v3"):
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = model

    def transcribe_file(self, file_path, output_type="text"):
        """
        output_type options:
            - "text"
            - "verbose_json"
        """

        with open(file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model=self.model,
                temperature=0,
                response_format=output_type,
            )

        if output_type == "verbose_json":
            return transcription

        return transcription.text
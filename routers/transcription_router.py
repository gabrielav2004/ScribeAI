import os
import uuid
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from sound_utils import AudioRecorder
from transcriber import GroqTranscriber
from rt_transcribe import RealtimeTranscriber

router = APIRouter(prefix="/transcription", tags=["Transcription"])

transcriber = GroqTranscriber()
recorder = AudioRecorder()
realtime_instance = None


# ✅ 1️⃣ Static File Upload Transcription
@router.post("/static")
async def transcribe_static(
    file: UploadFile = File(...),
    output_type: str = "text"
):
    allowed_ext = [".mp3", ".wav", ".m4a", ".webm", ".mp4", ".mpeg"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    temp_filename = f"temp_{uuid.uuid4()}{ext}"

    with open(temp_filename, "wb") as f:
        f.write(await file.read())

    result = transcriber.transcribe_file(
        temp_filename,
        output_type=output_type
    )

    os.remove(temp_filename)

    if output_type == "verbose_json":
        return result

    return JSONResponse(content={"transcription": result})


# ✅ 2️⃣ Start Live Recording (Server Mic)
@router.post("/live/start")
def start_live_recording():
    recorder.start()
    return {"message": "Recording started"}


# ✅ 3️⃣ Stop Live Recording + Transcribe
@router.post("/live/stop")
def stop_live_recording(output_type: str = "text"):
    file_path = recorder.stop()

    result = transcriber.transcribe_file(
        file_path,
        output_type=output_type
    )

    os.remove(file_path)

    if output_type == "verbose_json":
        return result

    return {"transcription": result}


# ✅ 4️⃣ Start Real-Time Transcription (Background)
@router.post("/realtime/start")
def start_realtime(background_tasks: BackgroundTasks):
    global realtime_instance

    if realtime_instance is not None:
        return {"message": "Real-time transcription already running"}

    realtime_instance = RealtimeTranscriber(chunk_duration=5)

    background_tasks.add_task(realtime_instance.start)

    return {"message": "Real-time transcription started"}


# ✅ 5️⃣ Stop Real-Time
@router.post("/realtime/stop")
def stop_realtime():
    global realtime_instance

    if realtime_instance is None:
        return {"message": "Real-time transcription not running"}

    realtime_instance.stop()
    realtime_instance = None

    return {"message": "Real-time transcription stopped"}
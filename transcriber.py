from faster_whisper import WhisperModel
import subprocess
import os

model = WhisperModel("turbo", device="cpu", compute_type="int8")

def transcribe(ogg_path: str) -> str:
    wav_path = ogg_path.replace(".ogg", ".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", ogg_path, wav_path],
        check=True, capture_output=True
    )
    segments, _ = model.transcribe(
        wav_path,
        language="vi",
        initial_prompt="Cuộc gọi bán hàng. Số điện thoại Việt Nam gồm 10 chữ số bắt đầu bằng 0."
    )
    os.remove(wav_path)
    return " ".join(segment.text for segment in segments)


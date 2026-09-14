from dataclasses import dataclass
from faster_whisper import WhisperModel


@dataclass
class Segment:
    start: float
    end: float
    text: str


class WhisperTranscriber:
    def __init__(self, model_size: str = "large-v3"):
        print(f"モデルを読み込み中: {model_size}")
        self.model = WhisperModel(model_size, device="auto", compute_type="auto")

    def transcribe(
        self,
        audio_path: str,
        start: float | None = None,
        end: float | None = None,
    ) -> list[Segment]:
        print(f"文字起こし中: {audio_path}")
        if end is not None and (start or 0.0) >= end:
            raise ValueError("start は end より小さい値を指定してください")

        clip_timestamps: str = "0"
        if start is not None or end is not None:
            start_val = start if start is not None else 0.0
            clip_timestamps = f"{start_val},{end}" if end is not None else f"{start_val}"
            print(f"時間範囲指定: {start_val:.2f}s -> {end if end is not None else '末尾'}")

        segments, info = self.model.transcribe(
            audio_path,
            language="ja",
            beam_size=5,
            clip_timestamps=clip_timestamps,
        )
        print(f"検出言語: {info.language} (確信度: {info.language_probability:.2f})")

        result = []
        for seg in segments:
            result.append(Segment(start=seg.start, end=seg.end, text=seg.text.strip()))
            print(f"  [{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text.strip()}")

        return result

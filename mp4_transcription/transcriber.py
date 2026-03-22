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

    def transcribe(self, audio_path: str) -> list[Segment]:
        print(f"文字起こし中: {audio_path}")
        segments, info = self.model.transcribe(
            audio_path,
            language="ja",
            beam_size=5,
        )
        print(f"検出言語: {info.language} (確信度: {info.language_probability:.2f})")

        result = []
        for seg in segments:
            result.append(Segment(start=seg.start, end=seg.end, text=seg.text.strip()))
            print(f"  [{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text.strip()}")

        return result

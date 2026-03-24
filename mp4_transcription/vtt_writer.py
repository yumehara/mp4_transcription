from pathlib import Path
from .transcriber import Segment


def _format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def write_vtt(segments: list[Segment], output_path: str | Path) -> None:
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, start=1):
            start = _format_timestamp(seg.start)
            end = _format_timestamp(seg.end)
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{seg.text}\n\n")
    print(f"VTTファイルを保存しました: {output_path}")

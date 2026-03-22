import re
from pathlib import Path
from .transcriber import Segment


def parse_vtt(vtt_path: str | Path) -> list[Segment]:
    """WebVTTファイルを読み込んでSegmentのリストに変換する。"""
    vtt_path = Path(vtt_path)
    text = vtt_path.read_text(encoding="utf-8")

    # タイムスタンプ行のパターン: HH:MM:SS.mmm --> HH:MM:SS.mmm
    timestamp_pattern = re.compile(
        r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})"
    )

    segments: list[Segment] = []
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        match = timestamp_pattern.match(lines[i].strip())
        if match:
            start = _parse_timestamp(match.group(1))
            end = _parse_timestamp(match.group(2))
            # 次の行以降がテキスト（空行まで）
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            segment_text = "\n".join(text_lines)
            if segment_text:
                segments.append(Segment(start=start, end=end, text=segment_text))
        else:
            i += 1

    return segments


def _parse_timestamp(ts: str) -> float:
    """HH:MM:SS.mmm を秒数（float）に変換する。"""
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

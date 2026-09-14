import argparse
import sys
from pathlib import Path

from .transcriber import WhisperTranscriber
from .vtt_writer import write_vtt
from .segment_processor import process_segments
from .time_utils import parse_time_arg

VALID_MODELS = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MP4ファイルを文字起こししてVTT字幕ファイルを生成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python -m mp4_transcription.main video.mp4
  python -m mp4_transcription.main video.mp4 --output subtitles.vtt
  python -m mp4_transcription.main video.mp4 --model medium
  python -m mp4_transcription.main video.mp4 --start 01:30 --end 05:00
  python -m mp4_transcription.main video.mp4 --start 90 --end 300
        """,
    )
    parser.add_argument("input", type=Path, help="入力MP4ファイルのパス")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="出力VTTファイルのパス（省略時は入力ファイルと同じ場所に同名で保存）",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="large-v3",
        choices=VALID_MODELS,
        help="Whisperモデルのサイズ（デフォルト: large-v3）",
    )
    parser.add_argument(
        "--start",
        "-s",
        type=parse_time_arg,
        default=None,
        help="文字起こしを開始する時刻（秒数 / MM:SS / HH:MM:SS、省略時は先頭から）",
    )
    parser.add_argument(
        "--end",
        "-e",
        type=parse_time_arg,
        default=None,
        help="文字起こしを終了する時刻（秒数 / MM:SS / HH:MM:SS、省略時は末尾まで）",
    )

    args = parser.parse_args()

    if args.end is not None and (args.start or 0.0) >= args.end:
        parser.error("--start は --end より小さい値を指定してください")

    input_path: Path = args.input
    if not input_path.exists():
        print(f"エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not input_path.is_file():
        print(f"エラー: ファイルではありません: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path: Path = args.output or input_path.with_suffix(".vtt")

    transcriber = WhisperTranscriber(model_size=args.model)
    segments = transcriber.transcribe(str(input_path), start=args.start, end=args.end)
    segments = process_segments(segments)

    if not segments:
        print("警告: 文字起こし結果が空です。", file=sys.stderr)

    write_vtt(segments, output_path)


if __name__ == "__main__":
    main()

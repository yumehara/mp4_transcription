import argparse
import sys
from pathlib import Path

from .vtt_parser import parse_vtt
from .translator import translate_segments, LANGUAGE_NAMES
from .vtt_writer import write_vtt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="日本語VTTファイルを任意の言語に翻訳して新しいVTTファイルを生成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python -m mp4_transcription.translate input.vtt --lang en
  python -m mp4_transcription.translate input.vtt --lang ko --output korean.vtt

利用可能な言語コード:
  en    English（英語）
  zh    Chinese Simplified（中国語簡体字）
  zh-TW Chinese Traditional（中国語繁体字）
  ko    Korean（韓国語）
  fr    French（フランス語）
  de    German（ドイツ語）
  es    Spanish（スペイン語）
  pt    Portuguese（ポルトガル語）
  it    Italian（イタリア語）
  ru    Russian（ロシア語）
  ar    Arabic（アラビア語）
  th    Thai（タイ語）
  vi    Vietnamese（ベトナム語）
  id    Indonesian（インドネシア語）

事前に ANTHROPIC_API_KEY 環境変数を設定してください:
  export ANTHROPIC_API_KEY="your-api-key"
        """,
    )
    parser.add_argument("input", type=Path, help="入力VTTファイルのパス")
    parser.add_argument(
        "--lang",
        "-l",
        required=True,
        help="翻訳先の言語コード（例: en, ko, zh, fr）",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="出力VTTファイルのパス（省略時は入力ファイル名に言語コードを付加）",
    )

    args = parser.parse_args()

    input_path: Path = args.input
    if not input_path.exists():
        print(f"エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)

    # 出力パスの決定（例: input.vtt → input.en.vtt）
    output_path: Path = args.output or input_path.with_suffix(f".{args.lang}.vtt")

    segments = parse_vtt(input_path)
    if not segments:
        print("エラー: VTTファイルにセグメントが見つかりませんでした。", file=sys.stderr)
        sys.exit(1)

    print(f"読み込み完了: {len(segments)} セグメント")

    translated = translate_segments(segments, args.lang)
    write_vtt(translated, output_path)


if __name__ == "__main__":
    main()

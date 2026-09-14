import argparse


def parse_time(value: str) -> float:
    """時刻文字列を秒（float）に変換する。

    対応フォーマット:
      - 秒数のみ: "90", "90.5"
      - MM:SS: "01:30"
      - HH:MM:SS: "01:02:03", "01:02:03.500"
    """
    text = value.strip()
    parts = text.split(":")
    if len(parts) > 3 or len(parts) == 0:
        raise ValueError(f"不正な時刻形式です: {value}")

    try:
        numbers = [float(p) for p in parts]
    except ValueError as e:
        raise ValueError(f"不正な時刻形式です: {value}") from e

    seconds = 0.0
    for n in numbers:
        seconds = seconds * 60 + n

    if seconds < 0:
        raise ValueError(f"時刻は0以上を指定してください: {value}")

    return seconds


def parse_time_arg(value: str) -> float:
    """argparse用の type 関数。エラー時に分かりやすいメッセージを出す。"""
    try:
        return parse_time(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"{e} (指定可能な形式: 秒数 / MM:SS / HH:MM:SS)"
        ) from e

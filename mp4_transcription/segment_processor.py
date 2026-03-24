from .transcriber import Segment


def remove_duplicates(segments: list[Segment]) -> list[Segment]:
    """同一テキストのセグメントを除去（最初の1件を残す）"""
    seen: set[str] = set()
    result = []
    for seg in segments:
        if seg.text not in seen:
            seen.add(seg.text)
            result.append(seg)
    return result


def remove_rolling_captions(segments: list[Segment]) -> list[Segment]:
    """ローリングキャプションを除去

    seg[i].text が seg[i+1].text の部分文字列であれば seg[i] を削除する。
    例: 「今日は」→「今日は良い天気」の場合、前者を除去。
    """
    result = []
    for i, seg in enumerate(segments):
        if i + 1 < len(segments) and seg.text in segments[i + 1].text:
            continue
        result.append(seg)
    return result


def process_segments(segments: list[Segment]) -> list[Segment]:
    """全後処理を適用するパイプライン"""
    segments = remove_rolling_captions(segments)
    segments = remove_duplicates(segments)
    return segments

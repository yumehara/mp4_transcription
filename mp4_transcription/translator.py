import json
import anthropic
from .transcriber import Segment

LANGUAGE_NAMES = {
    "en": "English",
    "zh": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
}


def translate_segments(segments: list[Segment], target_lang: str) -> list[Segment]:
    """
    セグメントリストを指定言語に翻訳して返す。
    Claude API (claude-opus-4-6) を使用。
    """
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    print(f"翻訳中: 日本語 → {lang_name} ({target_lang})")

    # 全セグメントのテキストをまとめてJSONで渡す
    source_texts = [{"id": i, "text": seg.text} for i, seg in enumerate(segments)]

    client = anthropic.Anthropic()

    prompt = f"""以下のJSON配列は日本語の字幕テキストです。
各要素の "text" フィールドを{lang_name}に翻訳してください。
"id" フィールドは変更せず、翻訳後のテキストを "text" フィールドに入れてください。
JSON配列のみを返し、説明文は不要です。

{json.dumps(source_texts, ensure_ascii=False, indent=2)}"""

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        response_text = stream.get_final_message().content[0].text

    # JSONを抽出してパース
    # コードブロック記法（```json ... ```）が含まれている場合も考慮
    response_text = response_text.strip()
    if response_text.startswith("```"):
        lines = response_text.splitlines()
        response_text = "\n".join(lines[1:-1])

    translated_list: list[dict] = json.loads(response_text)
    translated_map = {item["id"]: item["text"] for item in translated_list}

    result = []
    for i, seg in enumerate(segments):
        translated_text = translated_map.get(i, seg.text)
        result.append(Segment(start=seg.start, end=seg.end, text=translated_text))

    print(f"翻訳完了: {len(result)} セグメント")
    return result

import deepl
from dotenv import load_dotenv

load_dotenv()

from .transcriber import Segment

# DeepL の言語コードマッピング（入力コード → DeepL ターゲットコード）
LANGUAGE_MAP = {
    "en": "EN-US",
    "en-gb": "EN-GB",
    "zh": "ZH-HANS",
    "zh-TW": "ZH-HANT",
    "ko": "KO",
    "fr": "FR",
    "de": "DE",
    "es": "ES",
    "pt": "PT-BR",
    "pt-pt": "PT-PT",
    "it": "IT",
    "ru": "RU",
    "ar": "AR",
    "id": "ID",
    "nl": "NL",
    "pl": "PL",
    "sv": "SV",
    "tr": "TR",
}

LANGUAGE_NAMES = {
    "en": "English（英語）",
    "zh": "Chinese Simplified（中国語簡体字）",
    "zh-TW": "Chinese Traditional（中国語繁体字）",
    "ko": "Korean（韓国語）",
    "fr": "French（フランス語）",
    "de": "German（ドイツ語）",
    "es": "Spanish（スペイン語）",
    "pt": "Portuguese BR（ポルトガル語）",
    "it": "Italian（イタリア語）",
    "ru": "Russian（ロシア語）",
    "ar": "Arabic（アラビア語）",
    "id": "Indonesian（インドネシア語）",
    "nl": "Dutch（オランダ語）",
    "pl": "Polish（ポーランド語）",
    "sv": "Swedish（スウェーデン語）",
    "tr": "Turkish（トルコ語）",
}


def translate_segments(segments: list[Segment], target_lang: str) -> list[Segment]:
    """
    セグメントリストを指定言語に翻訳して返す。
    DeepL API（無料版・有料版どちらも対応）を使用。
    DEEPL_AUTH_KEY 環境変数が必要。
    """
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    deepl_lang = LANGUAGE_MAP.get(target_lang.lower(), target_lang.upper())

    print(f"翻訳中: 日本語 → {lang_name} ({target_lang})")

    translator = deepl.Translator()  # DEEPL_AUTH_KEY 環境変数を自動で読む

    # セグメントのテキストをまとめてリスト送信（APIコール回数を最小化）
    source_texts = [seg.text for seg in segments]
    results = translator.translate_text(
        source_texts,
        source_lang="JA",
        target_lang=deepl_lang,
    )

    translated = []
    for seg, result in zip(segments, results):
        translated.append(Segment(start=seg.start, end=seg.end, text=result.text))

    print(f"翻訳完了: {len(translated)} セグメント")
    return translated

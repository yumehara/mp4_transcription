# MP4 Transcription

MP4ファイルを文字起こしして、WebVTT形式の字幕ファイルを生成するCLIツールです。
音声認識には [faster-whisper](https://github.com/SYSTRAN/faster-whisper) を使用し、ローカル環境で動作します。

## 必要環境

- Python 3.10以上
- [Poetry](https://python-poetry.org/)
- [ffmpeg](https://ffmpeg.org/)

```bash
brew install ffmpeg
```

## セットアップ

```bash
git clone <repository>
cd mp4_transcription
poetry install
```

初回実行時にWhisperモデルが自動ダウンロードされます（large-v3は約3GB）。

## 使い方

```bash
poetry run python -m mp4_transcription.main <input.mp4> [オプション]
```

### 基本的な使い方

```bash
# VTTファイルをMP4と同じ場所に同名で保存
poetry run python -m mp4_transcription.main video.mp4

# 出力先を指定
poetry run python -m mp4_transcription.main video.mp4 --output subtitles.vtt
```

### オプション

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--output` | `-o` | 入力と同じ場所・同名 | 出力VTTファイルのパス |
| `--model` | `-m` | `large-v3` | Whisperモデルのサイズ |

### モデルサイズの選択

| モデル | 速度 | 精度 | ダウンロードサイズ |
|--------|------|------|------------------|
| `tiny` | 最速 | 低 | 約75MB |
| `base` | 速い | やや低 | 約145MB |
| `small` | 普通 | 普通 | 約465MB |
| `medium` | やや遅い | 高 | 約1.5GB |
| `large-v2` | 遅い | 非常に高 | 約3GB |
| `large-v3` | 遅い | 最高（デフォルト） | 約3GB |

```bash
# 速度優先（小さいモデル）
poetry run python -m mp4_transcription.main video.mp4 --model small

# 精度優先（デフォルト）
poetry run python -m mp4_transcription.main video.mp4 --model large-v3
```

## 出力形式

生成されるVTTファイルはWebVTT形式です。

```
WEBVTT

00:00:00.000 --> 00:00:09.000
広い

00:00:09.000 --> 00:00:14.600
10年ぶりぐらいのスケートなんで
```

VTTファイルはほとんどの動画プレイヤーや動画編集ソフトで利用できます。

---

## 字幕の翻訳

日本語のVTTファイルを任意の言語に翻訳できます。翻訳には [DeepL API](https://www.deepl.com/pro-api) を使用します（無料版：月間50万文字まで無料）。

### 事前準備

1. [DeepL API](https://www.deepl.com/pro-api) に登録して認証キーを取得
2. 環境変数に設定

```bash
export DEEPL_AUTH_KEY="your-deepl-auth-key"
```

### 使い方

```bash
poetry run python -m mp4_transcription.translate <input.vtt> --lang <言語コード> [オプション]
```

```bash
# 英語に翻訳（input.en.vtt として保存）
poetry run python -m mp4_transcription.translate subtitles.vtt --lang en

# 韓国語に翻訳して出力先を指定
poetry run python -m mp4_transcription.translate subtitles.vtt --lang ko --output korean.vtt
```

### オプション

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--lang` | `-l` | （必須） | 翻訳先の言語コード |
| `--output` | `-o` | `入力名.言語コード.vtt` | 出力VTTファイルのパス |

### 対応言語

| 言語コード | 言語 |
|-----------|------|
| `en` | English（英語） |
| `zh` | Chinese Simplified（中国語簡体字） |
| `zh-TW` | Chinese Traditional（中国語繁体字） |
| `ko` | Korean（韓国語） |
| `fr` | French（フランス語） |
| `de` | German（ドイツ語） |
| `es` | Spanish（スペイン語） |
| `pt` | Portuguese（ポルトガル語） |
| `it` | Italian（イタリア語） |
| `ru` | Russian（ロシア語） |
| `ar` | Arabic（アラビア語） |
| `id` | Indonesian（インドネシア語） |
| `nl` | Dutch（オランダ語） |
| `pl` | Polish（ポーランド語） |
| `sv` | Swedish（スウェーデン語） |
| `tr` | Turkish（トルコ語） |

> **注意:** DeepL はタイ語・ベトナム語には未対応です。

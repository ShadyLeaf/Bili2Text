# Bili2Text

Transcribe Bilibili Video to Text with [Whisper](https://github.com/openai/whisper).

## Quick Start

Clone repo

```shell
git clone git@github.com:ShadyLeaf/Bili2Text.git
```

Install ffmpeg (using [chocolately](https://chocolatey.org/))

```shell
# run as admin
choco install ffmpeg
```

Replace `audio_urls` in `main.py` with list of target URLs, here's an example:

```python
# main.py
audio_urls = [
    "https://www.bilibili.com/video/BV1Fa4y1273F",
    "https://www.bilibili.com/video/BV15N4y1J7CA",
]
```

Run `main.py`

```shell
python main.py
```

Result will be saved in `./result`

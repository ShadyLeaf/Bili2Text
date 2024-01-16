# Bili2Text

Transcribe Bilibili Video to Text with [Whisper](https://github.com/Const-me/Whisper).

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

Replace `audio_url` in `main.py` with target URL, here's an example:

```python
# main.py
audio_url = "https://www.bilibili.com/video/BV1Fa4y1273F"
```

Run `main.py`

```shell
python main.py
```

Result will be saved in `./result`

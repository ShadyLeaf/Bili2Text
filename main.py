import asyncio
import os
import re
import shutil

import torch
import whisper
from bilix.sites.bilibili import DownloaderBilibili


audio_url = "https://www.bilibili.com/video/BV1Fa4y1273F"


async def downloadaudio(url):
    async with DownloaderBilibili() as d:
        await d.get_video(url, path="./temp", only_audio=True)


## prepare environment
print("Preparing......")
audio_folder_path = "./audio"
temp_folder_path = "./temp"
result_folder_path = "./result"
if not os.path.exists(audio_folder_path):
    os.makedirs(audio_folder_path)
if not os.path.exists(temp_folder_path):
    os.makedirs(temp_folder_path)
if not os.path.exists(result_folder_path):
    os.makedirs(result_folder_path)


## download audio to ./temp
print("Downloading audio from", audio_url)
asyncio.run(downloadaudio(audio_url))
print("Audio Downloaded.")
audio_name = os.listdir(temp_folder_path)[0]
temp_path = temp_folder_path + "/" + audio_name
audio_path = audio_folder_path + "/" + audio_name
shutil.move(temp_path, audio_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = whisper.load_model(
    "medium",
    device=device,
    download_root="./.cache/whisper",
)
result = model.transcribe(
    audio_path,
    verbose=True,
    initial_prompt="“生于忧患，死于安乐。岂不快哉？”",
    # prepend_punctuations="“‘¿([{-",
    # append_punctuations="。，！？：”’)]}、",
)
text = result["text"]
text = re.sub(",", "，", text)
with open(result_folder_path + "/" + audio_name + ".txt", "w", encoding="utf-8") as f:
    f.write(text)

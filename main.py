import asyncio
import os
import re
import shutil
from datetime import datetime

import torch
import whisper
from bilix.sites.bilibili import DownloaderBilibili

audio_urls = ["https://www.bilibili.com/video/BV15N4y1J7CA"]


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

## load whisper model
# model_name = "large-v3"
model_name = "medium"
print("Using whisper model", model_name)
print("Loading Model......")
time1 = datetime.now()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = whisper.load_model(
    name=model_name,
    device=device,
    download_root="./.cache/whisper",
)
time2 = datetime.now()
print("Model Loaded in", (time2 - time1).seconds, "seconds")


## download and transcribe
for audio_url in audio_urls:
    ## download audio to ./temp
    print("Downloading audio from", audio_url)
    asyncio.run(downloadaudio(audio_url))
    print("Audio Downloaded.")
    audio_name = os.listdir(temp_folder_path)[0]
    temp_path = temp_folder_path + "/" + audio_name
    audio_path = audio_folder_path + "/" + audio_name
    shutil.move(temp_path, audio_path)

    print("Start Transcribe......")
    time3 = datetime.now()
    result = model.transcribe(
        audio_path,
        verbose=True,
        initial_prompt="“生于忧患，死于安乐。岂不快哉？”简体中文，加上标点。",
    )
    time4 = datetime.now()
    print("Transcribe Finish in", (time4 - time3).seconds, "seconds")

    print("Saving result......")
    text = result["text"]
    text = re.sub(",", "，", text)
    text = re.sub(r"\?", "？", text)
    with open(
        result_folder_path + "/" + audio_name + ".txt", "w", encoding="utf-8"
    ) as f:
        f.write(text)
    print("Result Saved to", result_folder_path + "/" + audio_name + ".txt")

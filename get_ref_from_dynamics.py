import asyncio
import os
import re
import shutil
from datetime import datetime, timezone

import torch
import whisper
from bilibili_api import settings, sync, user
from bilix.sites.bilibili import DownloaderBilibili

uid = 1556651916  # 小黛晨读
u = user.User(uid)

use_proxy = True
if use_proxy:
    settings.proxy = "http://127.0.0.1:7890"


async def get_latest_video_info():
    dynamics = []
    page = await u.get_dynamics(0)
    if "cards" in page:
        dynamics.extend(page["cards"])
    print(f"共获取 {len(dynamics)} 条动态")
    for dynamic in dynamics:
        try:
            bvid = dynamic["desc"]["bvid"]
        except:
            continue
        desc = dynamic["card"]["dynamic"]
        title = dynamic["card"]["title"]
        return bvid, title, desc


async def downloadaudio(url):
    async with DownloaderBilibili() as d:
        await d.get_video(url, path="./temp", only_audio=True)


bvid, title_ori, desc = sync(get_latest_video_info())

if "参考信息" in title_ori:
    title = re.sub(r"【参考信息第(.*?)期】(.*?)", r"【参考信息\1】\2", title_ori)
else:
    quit()

print(bvid)
print(title)
print(desc)

with open("processed.txt", "r", encoding="utf-8") as f:
    processed_video = f.readlines()

if bvid in processed_video:
    print("----------")
    print(bvid, title, "is processed")
    quit()
else:
    with open("processed.txt", "a", encoding="utf-8") as f:
        f.write("\n" + bvid)

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
audio_url = "https://www.bilibili.com/video/" + bvid
print("Downloading audio from", audio_url)
asyncio.run(downloadaudio(audio_url))
print("Audio Downloaded.")
audio_name = os.listdir(temp_folder_path)[0]
temp_path = temp_folder_path + "/" + audio_name
audio_path = audio_folder_path + "/" + audio_name
shutil.move(temp_path, audio_path)


## write basic info
text_path = result_folder_path + "/" + audio_name + ".md"
with open(text_path, "w", encoding="utf-8") as f:
    f.write("---\ntitle: ")
    f.write(title + "\n")
    f.write("description: " + desc + "\n")
    f.write("published: true\n")
    timestr = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"
    f.write("date: " + timestr + "\n")
    f.write("tags: \neditor: markdown\n")
    f.write("dateCreated: " + timestr + "\n---\n")
    text = """
## Tabs {.tabset}
### B站
<div style="position: relative; padding: 30% 45%;">
<iframe style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;" src="//player.bilibili.com/player.html?&bvid="""

    text2 = """&page=1&as_wide=1&high_quality=1&danmaku=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

### YouTube
<div style="position: relative; padding: 30% 45%;">
<iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" src="https://www.youtube-nocookie.com/embed/YouTubeVID" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

##

> 以下文本为音频转录结果，存在一定错误，校对正在进行中。
{.is-warning}

"""
    f.write(text)
    f.write(bvid)
    f.write(text2)

## load whisper model
model_name = "large-v3"
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

## transcribe
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

with open(text_path, "a", encoding="utf-8") as f:
    f.write(text)
print("Result Saved to", text_path)

import io
import re
import glob
import os

with io.open("C:\\Users\\xiaop\\Videos\TVs\\七龙珠\\name.txt",'r',encoding='utf8') as f:
    lines = f.readlines()

nameSet = {}
for line in lines:
    words =  re.split(' ', line)
    episode = words[1]
    name = words[3][:-1]
    nameSet[int(episode)] = name

print(nameSet)

videoPath = "C:\\Users\\xiaop\\Videos\TVs\\七龙珠\\*.mp4"
videos = glob.glob(videoPath)
for video in videos:
    print(video)
    result = re.search("\[(\d{1,3})\]", video)
    episode = int(result.group(1))
    episodeStr = "{:03d}".format(episode)
    newName = "七龙珠.S01.E" + episodeStr + "." + nameSet[episode] + ".mp4"
    print(newName)

    os.rename(video, newName)
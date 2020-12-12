import glob
from random import shuffle # random question sequence
from tinytag import TinyTag # access mp3 title 


QUESTION = glob.glob("media/question/*.mp3")
shuffle(QUESTION)
for i in QUESTION:
    tag = TinyTag.get(i)
    quest_text = tag.title
    quest_time = tag.duration
    print(tag.title,'_', quest_time)
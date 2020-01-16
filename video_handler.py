import json

class VideoHandler(object):
    def __init__(self):
        with open('videos.json') as videos:
                self.data = json.load(videos)

    def giveWeeks(self):
        return self.data["weeks"]

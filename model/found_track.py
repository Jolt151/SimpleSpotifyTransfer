from model.song import Song


class FoundTrack:
    def __init__(self, song: Song, index: int):
        self.song = song
        self.index = index

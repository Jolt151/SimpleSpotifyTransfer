from model.song import Song


class PendingTrack:
    def __init__(self, song: Song, index: int):
        self.song = song
        self.index = index

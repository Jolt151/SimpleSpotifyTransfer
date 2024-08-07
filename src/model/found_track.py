from src.model.local_track import LocalTrack


class FoundTrack:
    def __init__(self, local_track: LocalTrack, index: int):
        self.local_track = local_track
        self.index = index

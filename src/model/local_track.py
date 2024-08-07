from pathlib import Path


class LocalTrack:
    def __init__(self, file: Path, title: str, artist: str):
        self.file = file
        self.title = title
        self.artist = artist

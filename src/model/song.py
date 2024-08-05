from pathlib import Path  # Use Path for file paths


class Song:
    def __init__(self, file: Path, title: str, artist: str):
        self.file = file
        self.title = title
        self.artist = artist

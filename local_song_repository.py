from typing import List, Dict, Optional, Union
from pathlib import Path  # Use Path for file paths
import re  # For regular expressions (formatQuery)
from model.song import Song
from model.found_track import FoundTrack
from model.pending_track import PendingTrack
from fuzzywuzzy import fuzz, process
from tinytag import TinyTag


class LocalSongRepository:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)  # Ensure Path object
        self.filter_words = ["feat", "remix", "mix", "edit"]

        self.library = self.get_songs_as_map()
        self.library_list = self.flatten_library(self.library)
        self.library_filenames = [str(song.file) for song in self.library_list]

    def get_songs_as_map(self) -> Dict[str, List[Song]]:
        songs = self.get_all_songs(self.library_path)
        song_map = {}
        for song in songs:
            song_map.setdefault(song.title, []).append(song)
        return song_map

    def flatten_library(self, library: Dict[str, List[Song]]) -> List[Song]:
        return [song for song_list in library.values() for song in song_list]

    def get_single(self, path: str) -> Optional[Song]:
        try:
            file = Path(path)
            tags = TinyTag.get(file)
            title = tags.title
            artist = tags.artist
            return Song(file, title, artist)
        except Exception:
            return None

    def search_library(self, query: str, size: int) -> List[str]:
        return list(
            map(
                lambda tuple: tuple[0],
                process.extract(query, self.library_filenames, limit=size),
            )
        )

    def order_songs_as_filepaths(self, songs: List[FoundTrack]) -> List[str]:
        ordered_songs = sorted(songs, key=lambda s: s.index)
        return [str(song.song.file) for song in ordered_songs]

    def format_query(self, query: str) -> str:
        mutable_query = query
        for word in self.filter_words:
            mutable_query = re.sub(
                rf"\b{word}\b", " ", mutable_query, flags=re.IGNORECASE
            )
        return re.sub(r"[^\w\d]", "", mutable_query)

    def get_all_songs(self, path: Path) -> List[Song]:
        all_files = self._get_all_files(path)
        return [
            song
            for file in all_files
            if (song := self._try_get_song_info(file)) is not None
        ]

    def _get_all_files(self, path: Path) -> List[Path]:
        all_files = []
        if path.is_file():
            all_files.append(path)
        elif path.is_dir():
            for child in path.iterdir():
                all_files.extend(self._get_all_files(child))
        return all_files

    def _try_get_song_info(self, file: Path) -> Optional[Song]:
        try:
            # Replace with your audio tag library (e.g., mutagen)
            tags = TinyTag.get(file)
            title = tags.title
            artist = tags.artist
            return Song(file, title, artist)
        except Exception:
            return None

import xml.etree.ElementTree as ET
from model.found_track import FoundTrack
from typing import List
from pathlib import Path
import uuid

volumeName = "Macintosh HD"


def write_file(playlistName: str, tracks: List[FoundTrack]):
    root = ET.Element("NML")
    root.set("version", "20")

    head = ET.SubElement(root, "HEAD")
    head.set("COMPANY", "www.native-instruments.com")
    head.set("PROGRAM", "Traktor Pro 4")

    collection = ET.SubElement(root, "COLLECTION")
    collection.set("ENTRIES", f"{len(tracks)}")

    for track in tracks:
        entry = ET.SubElement(collection, "ENTRY")
        location = ET.SubElement(entry, "LOCATION")

        path = Path(track.song.file)
        location.set("DIR", getNmlFormattedPath(str(path)))
        location.set("FILE", path.name)
        location.set("VOLUME", volumeName)
        location.set("VOLUMEID", volumeName)

    playlists = ET.SubElement(root, "PLAYLISTS")
    node = ET.SubElement(playlists, "NODE")
    node.set("TYPE", "FOLDER")
    node.set("NAME", "$ROOT")
    subnodes = ET.SubElement(node, "SUBNODES")
    subnodes.set("COUNT", str("1"))

    node2 = ET.SubElement(subnodes, "NODE")
    node2.set("TYPE", "PLAYLIST")
    node2.set("NAME", playlistName)

    playlist = ET.SubElement(node2, "PLAYLIST")
    playlist.set("ENTRIES", str(len(tracks)))
    playlist.set("TYPE", "LIST")
    playlist.set("uuid", str(uuid.uuid4()))

    for track in tracks:
        entry = ET.SubElement(playlist, "ENTRY")
        primaryKey = ET.SubElement(entry, "PRIMARYKEY")
        primaryKey.set("TYPE", "TRACK")
        primaryKey.set("KEY", volumeName + getNmlFormattedPath(str(track.song.file)))

    # tree = ET.ElementTree(root)
    # tree.write("output.xml")
    return ET.tostring(root).decode("utf-8")


def getNmlFormattedPath(path: str) -> str:
    path = Path(path)
    return '/:' + '/:'.join(path.parts[1:])

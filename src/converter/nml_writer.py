import xml.etree.ElementTree as ET
from typing import List
from pathlib import Path
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
VOLUME_NAME = os.environ["LOCAL_VOLUME_NAME"]
NML_OUTPUT_FOLDER = os.environ["NML_OUTPUT_FOLDER"]


def write_file(playlistName: str, trackPaths: List[str]):
    root = ET.Element("NML")
    root.set("VERSION", "20")

    head = ET.SubElement(root, "HEAD")
    head.set("COMPANY", "www.native-instruments.com")
    head.set("PROGRAM", "Traktor Pro 4")

    # collection = ET.SubElement(root, "COLLECTION")
    # collection.set("ENTRIES", f"{len(tracks)}")

    # for track in tracks:
    #     entry = ET.SubElement(collection, "ENTRY")
    #     location = ET.SubElement(entry, "LOCATION")

    #     path = Path(track.song.file)
    #     location.set("DIR", getNmlFormattedPath(str(path.parent)) + "/:")
    #     location.set("FILE", path.name)
    #     location.set("VOLUME", volumeName)
    #     location.set("VOLUMEID", volumeName)

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
    playlist.set("ENTRIES", str(len(trackPaths)))
    playlist.set("TYPE", "LIST")
    playlist.set("uuid", str(uuid.uuid4()))

    for path in trackPaths:
        entry = ET.SubElement(playlist, "ENTRY")
        primaryKey = ET.SubElement(entry, "PRIMARYKEY")
        primaryKey.set("TYPE", "TRACK")
        primaryKey.set("KEY", VOLUME_NAME + getNmlFormattedPath(path))

    tree = ET.ElementTree(root)

    outputPath = os.path.join(*[NML_OUTPUT_FOLDER, playlistName + ".nml"])
    Path(outputPath).parent.mkdir(parents=True)
    tree.write(outputPath, encoding="utf-8")

    return ET.tostring(root).decode("utf-8")


def getNmlFormattedPath(path: str) -> str:
    path = Path(path)
    return "/:" + "/:".join(path.parts[1:])

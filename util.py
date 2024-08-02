def getTrackNames(tracks):
    return list(map(lambda track: track["track"]["name"], tracks))

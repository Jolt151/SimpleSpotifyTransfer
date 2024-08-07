# Simple Spotify Tranfer Tool

## Local Development

- `pip install -r requirements.txt`
- Create a file named `.env` with the following template at the root of the repository, pulling fields as required from the development console

```
CLIENT_ID=yourclientid
CLIENT_SECRET=yourclientsecret

# Converter tools
LOCAL_REPOSITORY_PATH=/Users/me/Music
# Volume that the local tracks are stored on. Needed for NML conversion
LOCAL_VOLUME_NAME="Macintosh HD"
# Output folder for the converted NML files
NML_OUTPUT_FOLDER=/Users/me/Music/NMLOutput



```

## Remote Development

- Follow all the steps in local development in the remote machine repository
- Use VSCode Remote Development to open the project on the remote machine
- Open the bottom panel, and select "Ports" next to "Terminal"
- Add the port `8080`, forwarded to `localhost:8080`

## Spotify Development Console Setup

- Log into https://developer.spotify.com/dashboard
- Create app, name it whatever you want
- Set the following fields:
  - APIs used: Web API
  - Redirect URIs:
    - http://localhost:8080
    - http://localhost
    - 127.0.0.1
    - https://localhost:8080    
  - User Management: Add all users that will be using the tool (including source and destination accounts)
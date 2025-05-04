
# Drivo Plus


### Drivo Plus is an entier systeme build to help driver to taker care of
* Helth with drive safely
* Car helth with an integrated Diagnostic tool
* Autocalculate damge of the care
### Current Repo
The Current Repository you're seeing is one of the features implimentation **Drive safety** using AI where detecting the drowsiness of the driver and make alert when required!
`



## Setup

* Clone Current Repository Repoisotry

```bash
  git clone https://github.com/mohamed52665838/socket-drivo_plus.git drivo_plus_ai
  cd drivo_plus_ai
```
#### using docker
* build docker image
```bash
docker build -t ai_drivo_plus:1.0 . # change tag name as you want
```
_Note_ : You can change whatever you want and rebuild the image!
* run the image

```bash
export AI_DRIVO_PORT=8085 # change port you want
docker run -p $AI_DRIVO_PORT:8083 ai_drivo_plus:1.0  # change to your tag name
```
That's it!

#### using system interpreter
* Systeme Requirements
```yamel
    python 3.11 | 3.10
```
Install python with version needed in your system [Python 3.11](https://www.python.org/downloads/release/python-3110/) or [python 3.10](https://www.python.org/downloads/release/python-3100/)
* install *virtuaenv* with you systeme interpreter *python 3.x whatever*
```bash
pip install virtualenv
```
or
```bash
python -m pip install virtualenv
```
* create virtual environnement with the selected interpreter
```bash
python -m virtualenv --python=path/to/installed/interpreter .venv
```
command above will create you virtual environnement with the selected interpreter
* activate your environnement

  
for linux
```bash
source .venv/bin/activate
```
for windows
```cmd
.\.venv\Scripts\activate
```



## Run Locally (system interpreter)

* install dependencies
```bash
pip install -r requirements.txt 
```
*Note* : meadiapipe doesn't installed ? you're using the wrong interpreter review our steps
* run the entry point
```bash
python ./websocket/server.py
``` 
That's it !

## 🐍 Python Dependencies

This project requires the following Python packages for WebSocket communication, image processing, media detection, and environment configuration.


| Package         | Version     | Description                                                                 |
| --------------- | ----------- | --------------------------------------------------------------------------- |
| `websockets`    | `15.0`      | WebSocket client/server for asynchronous real-time communication.           |
| `opencv-python` | `4.11.0.86` | OpenCV bindings for Python – used for processing camera frames, video, etc. |
| `mediapipe`     | `0.10.21`   | Google’s framework for real-time face, hand, pose, and object detection.    |
| `dotenv`        | `0.9.9`     | Reads environment variables from a `.env` file for secure configuration.    |
| `aiohttp`       | `3.11.13`   | Async HTTP and WebSocket client/server library based on asyncio.            |







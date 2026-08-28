# Internship
# Real-Time Communication and Video Streaming for a Prototypical Autonomous Driving Setup

This repository contains prototype implementations developed during my research internship at **Chemnitz University of Technology (TU Chemnitz)**.

**Research internship topic:**  
*Development of a Prototypical Autonomous Driving for a Closed Loop Environment*

The overall internship project focused on a prototypical autonomous-driving setup in a closed-loop environment. My work documented in this repository focused primarily on the **communication and video-streaming layer between distributed computing components**, particularly Raspberry Pi and PC environments.

## Project Objectives

The main objective was to investigate and experimentally compare different communication approaches for transferring data and real-time video between distributed systems.

The work included:

- Client-server communication between Raspberry Pi and PC
- TCP socket-based data and video transmission
- WebSocket-based real-time video streaming
- WebRTC-based video communication
- HTTP/Flask-based browser video streaming
- Basic authentication for socket communication
- Video capture and processing with OpenCV
- Experimental performance evaluation using FPS and transmission-time measurements

## Communication Approaches

### TCP Sockets

Several Python prototypes were developed using raw TCP sockets for:

- Client-server communication
- File/video transmission
- Real-time video streaming
- Connection termination handling
- Basic authentication
- Transmission-time and performance measurements

Example files:

- `tcpRawClient.py`
- `tcpRawSocketServer.py`
- `tcpRawClientVdStreamWithFpsOnScreen.py`
- `tcpRawSerVdStreamWithFpsOnScreen.py`
- `tcpSocketClient.py`
- `tcpSocketHost.py`
- `tcpSocketWithAuth.py`
- `tcpSocketwithAuthClient.py`

### WebSocket Streaming

WebSocket-based prototypes were implemented for transmitting encoded video frames between client and server.

OpenCV was used for:

- Video capture
- Frame encoding and decoding
- Video display
- FPS measurement

Relevant files:

- `ClientWebSocketBasicDisplayWithKeyToTerminate.py`
- `ServerWebSocketBasicDisplayWithKeyToTerminate.py`

### WebRTC

WebRTC was investigated as an alternative for real-time media communication.

The implementation uses technologies including:

- `aiortc`
- `aiohttp`
- WebRTC peer connections
- Webcam/video input
- Browser-based media communication

Relevant implementation:

- `webRtc/`
- `webRtcClient.py`
- `webRtcV2.py`

### HTTP / Flask Streaming

A Flask-based implementation was also developed to stream video through a web browser.

The stream can be accessed locally or from another device connected to the same network.

Relevant directory:

- `flaskServerStreamig/`

## Performance Evaluation

Different communication approaches were experimentally evaluated with emphasis on real-time video performance.

Evaluation included:

- Frames per second (FPS)
- Video-stream responsiveness
- Transmission time
- Communication behavior between distributed devices

The repository also contains recorded FPS measurements in:

`FPS.txt`

## Technologies

- Python
- TCP/IP
- Python Socket Programming
- WebSocket
- WebRTC
- HTTP
- Flask
- OpenCV
- aiohttp
- aiortc
- Raspberry Pi
- Raspberry Pi OS
- PC-based client/server systems

## Repository Structure

```text
Internship/
│
├── tcpRawClient.py
├── tcpRawSocketServer.py
├── tcpRawClientVdStreamWithFpsOnScreen.py
├── tcpRawSerVdStreamWithFpsOnScreen.py
│
├── tcpSocketClient.py
├── tcpSocketHost.py
├── tcpSocketWithAuth.py
├── tcpSocketwithAuthClient.py
│
├── ClientWebSocketBasicDisplayWithKeyToTerminate.py
├── ServerWebSocketBasicDisplayWithKeyToTerminate.py
│
├── flaskServerStreamig/
│   ├── server.py
│   ├── templates/
│   └── static/
│
├── webRtc/
│   ├── webcam.py
│   ├── client.js
│   └── index.html
│
├── FPS.txt
└── stopSign.mp4

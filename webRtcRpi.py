import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import aiohttp

class VideoStreamTrackCustom(VideoStreamTrack):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    async def recv(self):
        with open(self.filename, 'rb') as file:
            while True:
                chunk = file.read(16384)
                if not chunk:
                    break
                pts, time_base = await self.next_timestamp()
                frame = {
                    'type': 'video',
                    'data': chunk,
                    'timestamp': pts,
                    'time_base': time_base,
                }
                yield frame

async def generate_offer():
    pc = RTCPeerConnection()
    pc.addTransceiver("video")
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return pc.localDescription

async def send_offer(sdp):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://192.168.178.23:8080/offer', json={'sdp': sdp.sdp, 'type': sdp.type}) as response:
            answer = await response.text()
            print("Received acknowledgment:", answer)

async def main():
    offer = await generate_offer()
    await send_offer(offer)

    track = VideoStreamTrackCustom('stopSign.mp4')

    pc = RTCPeerConnection()
    pc.addTrack(track)

    # Wait for ICE gathering to complete
    await pc.createOffer()
    print("ICE gathering complete")

    # Wait for acknowledgment from the server
    async with aiohttp.ClientSession() as session:
        async with session.get('http://192.168.178.23:8080/ack') as response:
            acknowledgment = await response.text()
            print("Received acknowledgment from server:", acknowledgment)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

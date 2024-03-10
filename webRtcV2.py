import aiohttp
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription

async def index(request):
    return web.Response(text="Server is running")

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])
    pc = RTCPeerConnection()

    @pc.on("track")
    def on_track(track):
        print("Track received from client")
        # Print the received video track instead of saving it to a file
        print(track)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print("Sending answer:", answer.sdp)
    
    # Send acknowledgment response to the client
    return web.Response(text="Offer received and processed")

async def acknowledgment(request):
    # Handle acknowledgment request from the client
    return web.Response(text="Video received successfully")

app = web.Application()
app.router.add_get('/', index)
app.router.add_post('/offer', offer)
app.router.add_get('/ack', acknowledgment)

if __name__ == "__main__":
    web.run_app(app, host='0.0.0.0', port=8080)
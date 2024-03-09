import aiohttp
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription

async def index(request):
    return web.Response(text="Server is running")

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])
    pc = RTCPeerConnection()

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state is", pc.iceConnectionState)

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

web.run_app(app, host='0.0.0.0', port=8080)
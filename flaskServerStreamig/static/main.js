// Function to send an offer request to the server

async function createOffer() {

    console.log("Sending offer request");



    // Fetch the offer from the server

    const offerResponse = await fetch("/offer", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

        },

        body: JSON.stringify({

            sdp: "",

            type: "offer",

        }),

    });



    // Parse the offer response

    const offer = await offerResponse.json();

    console.log("Received offer response:", offer);



    // Set the remote description based on the received offer

    await pc.setRemoteDescription(new RTCSessionDescription(offer));



    // Create an answer and set it as the local description

    const answer = await pc.createAnswer();

    await pc.setLocalDescription(answer);

}



// Function to handle receiving FPS data and updating the display

async function receiveAndDisplayFPS() {

    try {

        const fpsResponse = await fetch("/fps");

        const fpsData = await fpsResponse.json();

        const fpsDisplay = document.getElementById('fpsDisplay');

        fpsDisplay.textContent = `FPS: ${fpsData.fps}`;

    } catch (error) {

        console.error("Error fetching or parsing FPS data:", error);

    }

}



// Create a new RTCPeerConnection instance

let pc = new RTCPeerConnection();



// Trigger the process by creating and sending an offer

createOffer();



// Fetch and display FPS every second

setInterval(receiveAndDisplayFPS, 1000);

let pc = null;
let frameCount = 0;
let startTime = null;
const fpsDisplay = document.getElementById("fps");

function negotiate() {
  pc.addTransceiver("video", { direction: "recvonly" });
  pc.addTransceiver("audio", { direction: "recvonly" });
  return pc
    .createOffer()
    .then((offer) => pc.setLocalDescription(offer))
    .then(
      () =>
        new Promise((resolve) => {
          if (pc.iceGatheringState === "complete") {
            resolve();
          } else {
            const checkState = () => {
              if (pc.iceGatheringState === "complete") {
                pc.removeEventListener("icegatheringstatechange", checkState);
                resolve();
              }
            };
            pc.addEventListener("icegatheringstatechange", checkState);
          }
        })
    )
    .then(() =>
      fetch("/offer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(pc.localDescription),
      })
    )
    .then((response) => response.json())
    .then((answer) => pc.setRemoteDescription(answer))
    .catch((e) => alert(e));
}


function updateFrameRate() {
const currentTime = performance.now();
const elapsedTime = currentTime - startTime;

// Calculate FPS only if at least one second has passed since the last update
if (elapsedTime >= 1000) {
  const fps = (frameCount / elapsedTime) * 1000; // Calculate FPS
  fpsDisplay.textContent = "FPS: " + fps.toFixed(6); // Update FPS display
  console.log("FPS:", fps.toFixed(6));

  // Reset frame count and start time for the next interval
  frameCount = 0;
  startTime = currentTime;
}
}


function startFrameRateMonitoring() {
startTime = performance.now(); // Initialize start time
const video = document.getElementById("video");
video.addEventListener("timeupdate", () => {
  frameCount++; // Increment frame count
  updateFrameRate(); // Update frame rate once per second
});
}

function start() {
  const config = { sdpSemantics: "unified-plan" };
  pc = new RTCPeerConnection(config);

  pc.addEventListener("track", (event) => {
    if (event.track.kind === "video") {
      document.getElementById("video").srcObject = event.streams[0];
      startFrameRateMonitoring(); // Start monitoring frame rate when video track is received
    } else {
      document.getElementById("audio").srcObject = event.streams[0];
    }
  });

  document.getElementById("start").style.display = "none";
  negotiate();
  document.getElementById("stop").style.display = "inline-block";
}

function stop() {
  document.getElementById("stop").style.display = "none";

  // Close peer connection
  setTimeout(() => {
    pc.close();
  }, 500);
}

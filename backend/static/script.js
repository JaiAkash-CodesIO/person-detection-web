document
.getElementById("connectBtn")
.addEventListener("click", async () => {

    const source =
        document.getElementById("cameraSelect").value;

    const response = await fetch("/connect_camera", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            source: source
        })

    });

    const result = await response.json();

    if(result.success){

        document.getElementById("video").src =
            "/video_feed?" + new Date().getTime();

    }else{

        alert("Unable to connect to camera");

    }

});
document.getElementById("disconnectBtn").addEventListener("click", async () => {

    await fetch("/disconnect_camera", {
        method: "POST"
    });

    document.getElementById("video").src = "";

});

setInterval(async()=>{

    try{

        const response = await fetch("/status");

        const data = await response.json();

        document.getElementById("persons").innerHTML = data.persons;

        document.getElementById("fps").innerHTML = data.fps;

        document.getElementById("status").innerHTML =
            data.camera
            ? "🟢 Connected"
            : "🔴 Disconnected";

    }

    catch{

        document.getElementById("status").innerHTML =
            "🔴 Offline";

    }

},500);
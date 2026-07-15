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

setInterval(async()=>{

    try{

        const response = await fetch("/status");

        const data = await response.json();

        document.getElementById("persons").innerHTML =
            "Persons : " + data.persons;

        document.getElementById("status").innerHTML =
            data.camera
            ? "🟢 Camera Connected"
            : "🔴 Camera Disconnected";

    }

    catch{

        document.getElementById("status").innerHTML =
            "🔴 Server Offline";

    }

},1000);
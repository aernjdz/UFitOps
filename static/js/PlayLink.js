
const link = document.getElementById("input");
const audioPlayer = document.getElementById('audio-player');
const audioPlayer_src = document.getElementById('audio-source');
function isValid(text){
    console.log(text);
    if (text.includes("https://") || text.includes("http://")) return true; else return false;
}
link.addEventListener("keyup", async function(event) {
    if (event.key === "Enter") {
        if(isValid(link.value)){
             let res = await GetAudio(link.value)
                console.log(res);
                if (res !==null){
                    
                await Load(res);
             
             
            
             
            }
        }
    
}
})
async function Load(url){
    audioPlayer.src = url;
    audioPlayer.load();
}

async function GetAudio(url)
        {
            try {
            const response = await fetch(`/get_audio_stream_url?song_url=${encodeURIComponent(url)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            return data.audio_stream_url;
        }catch(e){
            console.log(e)  
            return null;
        }
    }
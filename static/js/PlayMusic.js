import AudioMotionAnalyzer from 'https://cdn.skypack.dev/audiomotion-analyzer?min';

document.addEventListener('DOMContentLoaded', function() {
    let lastSong = {
        "isNull" : true,
        "title" : null,
        "thumbnail": null,
        "url" : null,
        "artist" : null,
        "isPlaing": false,
        "currentPlayingItem" : null,
        "data_music": null
    };

    const items = document.querySelectorAll('.item');
    const audioPlayer = document.getElementById('audio-player');
    const currentTime = document.getElementById('current-time');
    const totalTime = document.getElementById('total-time');
    const thumbnail = document.getElementById('thumbnail');
    const name = document.getElementById("song-title");
    const artist = document.getElementById("song-artist");
    const btns = document.getElementById("player");
    const timeRange = document.getElementById('time_range');
    const time_range_volume = document.getElementById('time_range_volume');
    const status = document.getElementById('status');
    const status_title = document.getElementById('status-title');
    const status_artist  = document.getElementById('status-artist');
    const status_views = document.getElementById('status-views');
    const status_thumbnail = document.getElementById('status-thumbnail');
    const volume_info = document.getElementById('volume');
    console.log(lastSong)
    
    btns.addEventListener('click', async () =>{
        if (!lastSong.isNull){
            if (!lastSong.isPlaing) await Play(); else await Pause();
        }
    });

        items.forEach(item => {
            const PlayButton = item.querySelector(".play-button")
            if (PlayButton){
            PlayButton.addEventListener('click', async () => {
                const data = item.getAttribute("data-song")
                console.log(JSON.parse(data));
                console.log(lastSong);

                if (lastSong.isNull){
                console.log("last song is null")
                let res = JSON.parse(data);
                lastSong.isNull = false;
                lastSong.url = res.url;
                lastSong.artist = res.artist;
                lastSong.thumbnail = res.thumbnails;
                lastSong.title = res.title;
                var data_music = await GetAudio(res.url);
                lastSong.data_music = data_music;
                lastSong.currentPlayingItem = PlayButton;
                await Load(lastSong.data_music);

                thumbnail.src = lastSong.thumbnail;
                name.textContent = res.title;
                artist.textContent = lastSong.artist;
                status.textContent = "Is Playing";
                status_artist.textContent = res.artist;
                status_title.textContent = res.title;
                status_views.textContent = res.views;
                status_thumbnail.src = res.thumbnails;
                }else {
                    console.log("last song is not null")
                    if (lastSong.currentPlayingItem != PlayButton){
                        await Pause();
                        let  res  = JSON.parse(data);
                        lastSong.url = res.url;
                        lastSong.artist = res.artist;
                        lastSong.thumbnail = res.thumbnails;
                        lastSong.title = res.title;
                        var data_music = await GetAudio(res.url);
                        lastSong.data_music = data_music;
                        lastSong.currentPlayingItem = PlayButton;
                        
                        thumbnail.src = lastSong.thumbnail;
                        name.textContent = res.title;
                        artist.textContent = lastSong.artist;
                        status.textContent = "Is Playing";
                        status_artist.textContent = lastSong.artist;
                        status_title.textContent = res.title;
                        status_views.textContent = res.views;
                        status_thumbnail.src = res.thumbnails;

                        await Load(lastSong.data_music);
                    }
                }
                if (!lastSong.isPlaing) await Play(); else await Pause();
               


                });
            }
        });

        audioPlayer.addEventListener('timeupdate', () => {
            const Time = formatTime(audioPlayer.currentTime);
            currentTime.textContent = Time;
         
            timeRange.value = audioPlayer.currentTime;
          
        });

    
        timeRange.addEventListener('input', function() {
            audioPlayer.currentTime = timeRange.value;
        });

        time_range_volume.addEventListener('input',()=>{
            audioPlayer.volume = parseFloat(time_range_volume.value);
            volume_info.textContent = `${(time_range_volume.value*100).toFixed(0)}%`;
        });
        audioPlayer.addEventListener('loadedmetadata', () => {
            const duration = formatTime(audioPlayer.duration);
            totalTime.textContent = duration;
            timeRange.max = audioPlayer.duration;
            
        });

        audioPlayer.addEventListener('ended', () => {
            let btn = lastSong.currentPlayingItem; 
            if (lastSong.currentPlayingItem) {
                btn.querySelector('i')?.classList?.remove('bx-pause');
                btn.querySelector('i')?.classList?.add('bxs-right-arrow');
                btns.classList.remove('bx-pause');
                btns.classList.add('bxs-right-arrow');
                lastSong = {
                    "isNull" : true,
                    "title" : null,
                    "thumbnail": null,
                    "url" : null,
                    "artist" : null,
                    "isPlaing": false,
                    "currentPlayingItem" : null,
                    "data_music": null
                };
            }
        });
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
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

    async function GetAudio_from_Title(title)
    {
        try {
        const response = await fetch(`/search_song?title=${title}`);
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

      

        async function Play(){
            let btn = lastSong.currentPlayingItem;
            if (audioPlayer.paused){
                audioPlayer.play();
                lastSong.isPlaing = true;
                btn.querySelector('i')?.classList?.remove('bxs-right-arrow');
                btn.querySelector('i')?.classList?.add('bx-pause');
                btns.classList.remove('bxs-right-arrow');
                btns.classList.add("bx-pause");
               
             
            }
        }
        async function Pause(){
            let btn = lastSong.currentPlayingItem;
            if (!audioPlayer.paused){
                lastSong.isPlaing = false;
                audioPlayer.pause();
                btn.querySelector('i')?.classList?.remove('bx-pause');
                btn.querySelector('i')?.classList?.add('bxs-right-arrow');
                btns.classList.remove('bx-pause');
                btns.classList.add('bxs-right-arrow');
            }
            
        }

 


async function Load(url){
    audioPlayer.src = url;
    audioPlayer.load();
}


const link = document.getElementById("input");




    link.addEventListener("keyup", async function(event) {
        if (event.key === "Enter") {
            const title = event.target.value;
                let r = await GetAudio_from_Title(title);
                let data = await GetAudioInfo(r);
                console.log(data)
                if (r !== null) {
                if (lastSong.isNull){
                    console.log("last song is null")
                    let res = data;
                    lastSong.isNull = false;
                    lastSong.url = r;
                    lastSong.artist = res.artist;
                    lastSong.thumbnail = res.thumbnails;
                    lastSong.title = res.title;
                    var data_music = await GetAudio(r);
                    lastSong.data_music = data_music;
                    lastSong.currentPlayingItem = btns;
          
                    await Load(data_music);
    
                    thumbnail.src = lastSong.thumbnail;
                    name.textContent = res.title;
                    artist.textContent = lastSong.artist;
                    status.textContent = "Is Playing";
                    status_artist.textContent = res.artist;
                    status_title.textContent = res.title;
                    status_views.textContent = res.views;
                    status_thumbnail.src = res.thumbnails;
                    }else {
                        console.log("last song is not null")
                        if (lastSong.currentPlayingItem != btns){
                            await Pause();
                            let  res  = data;
                            lastSong.url = r;
                            lastSong.artist = res.artist;
                            lastSong.thumbnail = res.thumbnails;
                            lastSong.title = res.title;
                            var data_music = await GetAudio(r);
                            lastSong.data_music = data_music;
                            lastSong.currentPlayingItem = btns;
                            
                            thumbnail.src = lastSong.thumbnail;
                            name.textContent = res.title;
                            artist.textContent = lastSong.artist;
                            status.textContent = "Is Playing";
                            status_artist.textContent = lastSong.artist;
                            status_title.textContent = res.title;
                            status_views.textContent = res.views;
                            status_thumbnail.src = res.thumbnails;
    
                            await Load(data_music);
                        }
                    }
                }
            }

        
    });

    
    
    function isValid(text) {
        return text.includes("https://") || text.includes("http://");
    }

    async function GetAudioInfo(url)
    {
        try {
        const response = await fetch(`/get_song_info?song_url=${encodeURIComponent(url)}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
        return data;
    }catch(e){
        console.log(e)  
        return null;
    }
    
}
});

document.addEventListener('DOMContentLoaded', () => {
    const playButton = document.querySelector('.play-button');
    const audioPlayer = document.getElementById('audio-player');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');
    const sourceElement = audioPlayer.querySelector('source');
    let isPlaying = false;
    
    playButton.addEventListener('click', () => {
        if (isPlaying) {
            audioPlayer.pause();
            playButton.classList.remove('bxs-pause');
            playButton.classList.add('bxs-right-arrow');
        } else {
            audioPlayer.play();
            playButton.classList.remove('bxs-right-arrow');
            playButton.classList.add('bxs-pause');
        }
        isPlaying = !isPlaying;
    });
    
    audioPlayer.addEventListener('timeupdate', () => {
        const currentTime = formatTime(audioPlayer.currentTime);
        currentTimeDisplay.textContent = currentTime;
        
        const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        document.querySelector('.active-line').style.width = `${progress}%`;
    });

    audioPlayer.addEventListener('loadedmetadata', () => {
        const duration = formatTime(audioPlayer.duration);
        totalTimeDisplay.textContent = duration;
    });
    
    // Example function to load a song
    function loadSong(songUrl) {
        audioPlayer.src = songUrl;
        audioPlayer.load();
        isPlaying = false;
        playButton.classList.remove('bxs-pause');
        playButton.classList.add('bxs-right-arrow');
    }
    
    // Helper function to format time
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    async function  loadAudio(songUrl) {
    try {
        const response = await fetch(`/get_audio_stream_url?song_url=${encodeURIComponent(songUrl)}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // Optional: Log the fetched data for debugging
        loadSong(data.audio_stream_url);
    } catch (error) {
        console.error('Error loading audio:', error);
        alert('Failed to load audio.');
    }
    }
    
    loadAudio(sourceElement.src);

});

const audioElements = document.querySelectorAll('.audio-control');

audioElements.forEach(audio => {
    audio.addEventListener('play', () => {
        audioElements.forEach(otherAudio => {
            if (otherAudio !== audio && !otherAudio.paused) {
                otherAudio.pause();
            }
        });
    });
});
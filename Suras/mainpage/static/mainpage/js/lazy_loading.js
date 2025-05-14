document.addEventListener("DOMContentLoaded", () => {
    const audios = document.querySelectorAll("audio[data-src]");
    audios.forEach(audio => {
    // Проверяем, активен ли элемент audio
    audio.addEventListener("play", () => {
        if (!audio.src) {
            audio.src = audio.getAttribute("data-src");console.log(`Аудио загружено: ${audio.src}`);
        }
    });

    // Дополнительно можно загрузить аудио при взаимодействии мышкой
    audio.addEventListener("mouseover", () => {
        if (!audio.src) {
            audio.src = audio.getAttribute("data-src");
        }
    });
    });
});
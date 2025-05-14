const audioPlayer = document.getElementById("audioPlayer");
const currentTimeDisplay = document.getElementById("currentTime");

audioPlayer.addEventListener("timeupdate", () => {
    const currentTime = audioPlayer.currentTime; // Текущее время в секундах
    const milliseconds = Math.floor(currentTime * 1000); // Переводим в миллисекунды
    currentTimeDisplay.textContent = `Текущее время: ${milliseconds} мс`;
});
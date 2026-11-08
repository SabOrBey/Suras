(() => {
    const player = document.querySelector("[data-segment-player]");
    if (!player) {
        return;
    }

    const repeatControl = document.querySelector("[data-repeat-control]");
    const status = document.querySelector("[data-audio-status]");
    const initialStart = Number(player.dataset.clipStartMs);
    const initialEnd = Number(player.dataset.clipEndMs);
    let clipStart = Number.isFinite(initialStart) ? Math.max(0, initialStart) / 1000 : 0;
    let clipEnd = player.dataset.clipEndMs !== "" && Number.isFinite(initialEnd)
        ? Math.max(clipStart, initialEnd / 1000)
        : null;
    let repeatsRemaining = 0;
    let repeatForever = false;
    let pendingStart = null;

    const report = (message) => {
        if (status) {
            status.textContent = message;
        }
    };

    const startClip = () => {
        pendingStart = null;
        player.currentTime = clipStart;
        player.play().then(
            () => report("Аудио воспроизводится."),
            () => report("Не удалось воспроизвести аудио. Нажмите кнопку воспроизведения."),
        );
    };

    const playSelection = (button) => {
        const source = button.dataset.audioUrl;
        if (!source) {
            return;
        }

        const startMilliseconds = Number(button.dataset.audioStart);
        const endMilliseconds = Number(button.dataset.audioEnd);
        clipStart = Number.isFinite(startMilliseconds) ? Math.max(0, startMilliseconds) / 1000 : 0;
        clipEnd = button.dataset.audioEnd !== "" && Number.isFinite(endMilliseconds)
            ? Math.max(clipStart, endMilliseconds / 1000)
            : null;

        const repeatCount = repeatControl ? repeatControl.value : "1";
        repeatForever = repeatCount === "infinite";
        repeatsRemaining = repeatForever ? 0 : Math.max(0, Number(repeatCount) - 1);

        if (pendingStart) {
            player.removeEventListener("loadedmetadata", pendingStart);
            pendingStart = null;
        }

        if (player.dataset.activeUrl !== source) {
            player.dataset.activeUrl = source;
            player.src = source;
            player.load();
            pendingStart = startClip;
            player.addEventListener("loadedmetadata", pendingStart, { once: true });
        } else if (player.readyState === 0) {
            pendingStart = startClip;
            player.addEventListener("loadedmetadata", pendingStart, { once: true });
            player.load();
        } else {
            startClip();
        }
    };

    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-audio-url]");
        if (button) {
            playSelection(button);
        }
    });

    const repeatClip = () => {
        if (!repeatForever && repeatsRemaining <= 0) {
            return false;
        }
        if (!repeatForever) {
            repeatsRemaining -= 1;
        }
        player.currentTime = clipStart;
        player.play().catch(() => report("Не удалось продолжить воспроизведение аудио."));
        return true;
    };

    player.addEventListener("timeupdate", () => {
        if (clipEnd !== null && player.currentTime >= clipEnd) {
            if (!repeatClip()) {
                player.pause();
                player.currentTime = clipEnd;
                report("Аят прослушан.");
            }
        }
    });

    player.addEventListener("loadedmetadata", () => {
        if (clipEnd !== null && (player.currentTime < clipStart || player.currentTime >= clipEnd)) {
            player.currentTime = clipStart;
        }
    });

    player.addEventListener("play", () => {
        if (clipEnd !== null && (player.currentTime < clipStart || player.currentTime >= clipEnd)) {
            player.currentTime = clipStart;
        }
    });

    player.addEventListener("seeking", () => {
        if (clipEnd !== null && (player.currentTime < clipStart || player.currentTime >= clipEnd)) {
            player.currentTime = clipStart;
        }
    });

    player.addEventListener("ended", () => {
        if (repeatClip()) {
            return;
        }
        report("Аудио завершено.");
    });

    player.addEventListener("error", () => report("Не удалось загрузить аудиозапись."));
})();

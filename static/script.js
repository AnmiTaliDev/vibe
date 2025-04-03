// Обработчик для загрузки треков из API
const loadMusic = async () => {
    const response = await fetch('/music');
    const tracks = await response.json();
    const trackList = document.getElementById('track-list');
    tracks.forEach(track => {
      const listItem = document.createElement('li');
      listItem.textContent = track;
      listItem.onclick = () => playTrack(track);
      trackList.appendChild(listItem);
    });
  };
  
  // Запуск трека
  const playTrack = async (track) => {
    await fetch('/api/play', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ track })
    });
    const audio = new Audio(`/music/${track}`);
    audio.play();
    document.getElementById('current-track').textContent = `Playing: ${track}`;
  };
  
  // Переключение на следующий трек
  const nextTrack = async () => {
    await fetch('/api/next');
    // Логика для следующего трека (например, обновление UI)
    document.getElementById('current-track').textContent = 'Next track';
  };
  
  // Переключение на предыдущий трек
  const prevTrack = async () => {
    await fetch('/api/prev');
    // Логика для предыдущего трека
    document.getElementById('current-track').textContent = 'Previous track';
  };
  
  // Установка громкости
  const setVolume = (volume) => {
    const audio = document.querySelector('audio');
    if (audio) {
      audio.volume = volume / 100;
    }
    fetch('/api/volume', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ volume })
    });
  };
  
  // Инициализация интерфейса
  document.addEventListener('DOMContentLoaded', () => {
    loadMusic();
    document.getElementById('next-btn').onclick = nextTrack;
    document.getElementById('prev-btn').onclick = prevTrack;
    document.getElementById('volume-slider').oninput = (e) => setVolume(e.target.value);
  });
  
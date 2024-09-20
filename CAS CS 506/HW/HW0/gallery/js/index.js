/* global $ */

// Ailee's birthdate
const birthdate = 010108;
/* counting down */
const config = {
  birthdate: 'Jan 8, 2022',
  name: 'Ailee'
};

const second = 1000,
  minute = second * 60,
  hour = minute * 60,
  day = hour * 24;
  
const confettiSettings = { target: 'confetti' };
const confetti = new window.ConfettiGenerator(confettiSettings);
confetti.render();


let countDown = new Date(`${config.birthdate} 00:00:00`).getTime();
var x = setInterval(function() {
  let now = new Date().getTime(),
  distance = countDown - now;

  document.getElementById('day').innerText = Math.floor(distance / day);
  document.getElementById('hour').innerText = Math.floor((distance % day) / hour);
  document.getElementById('minute').innerText = Math.floor((distance % hour) / minute);
  document.getElementById('second').innerText = Math.floor((distance % minute) / second);
  
  if(distance > 0){
      $("#curtain").show();
      $("#lock").hide();
  }else{
      $("#curtain").hide();
      $("#lock").show();
      clearInterval(x);
  }
}, second);  

const musicContainer = document.getElementById('audio-container');
const playBtn = document.getElementById('play');
const prevBtn = document.getElementById('audio-prev');
const nextBtn = document.getElementById('audio-next');

const audio = document.getElementById('audio');
const progress = document.getElementById('progress');
const progressContainer = document.getElementById('progress-container');
const title = document.getElementById('audio-title');
const cover = document.getElementById('audio-cover');

// Song Titles
const songs = ['John Park - Falling', 'Gracie Abrams - 21', 'Daniel Caesar - Best Part', 'dhruv - double take'];

//keep track of song
var songIndex = 1;

function loadSong(song) {
    title.innerText = song;
    $("#audio").attr('src', "source/music/" + song + ".mp3");
    $("#audio-cover").attr('src', "source/photos/" + song + ".png");
}

//Play song
function playSong() {
    musicContainer.classList.add('play');
    playBtn.querySelector('i.fas').classList.remove('fa-play');
    playBtn.querySelector('i.fas').classList.add('fa-pause');

    audio.play();
}

//pause song
function pauseSong() {
    musicContainer.classList.remove('play');
    playBtn.querySelector('i.fas').classList.add('fa-play');
    playBtn.querySelector('i.fas').classList.remove('fa-pause');

    audio.pause();
}

//Previous song
function prevSong() {
    songIndex--;

    if (songIndex < 0) {
        songIndex = songs.length - 1;
    }

    loadSong(songs[songIndex]);

    playSong();
}

// Next song
function nextSong() {
    songIndex++;

    if (songIndex > songs.length - 1) {
        songIndex = 0;
    }

    loadSong(songs[songIndex]);

    playSong();
}

// Update progress bar
function updateProgress(e) {
    const { duration, currentTime } = e.srcElement;
    const progressPercent = (currentTime / duration) * 100;
    progress.style.width = `${progressPercent}%`;
}

// Set progress bar
function setProgress(e) {
    const width = this.clientWidth;
    const clickX = e.offsetX;
    const duration = audio.duration;

    audio.currentTime = (clickX / width) * duration;
}

// Event listeners
playBtn.addEventListener('click', () => {
    const isPlaying = musicContainer.classList.contains('play');

    if (isPlaying) {
        pauseSong();
    }
    else {
        playSong();
    }
});

// Change song
prevBtn.addEventListener('click', prevSong);
nextBtn.addEventListener('click', nextSong);

// Time/song update
audio.addEventListener('timeupdate', updateProgress);

// Click on progress bar
progressContainer.addEventListener('click', setProgress);

// Song ends
audio.addEventListener('ended', nextSong);





$(document).ready(function() {

    // id 로 input 객체를 가져온다. 
    var inputpw = document.getElementById("pw");

    inputpw.addEventListener('keypress', function(key) {
        // key.key 의 값이 Enter 일 경우 코드 실행 
        // key.keyCode == 13 도 동일한 기능을 한다. 
        if (key.key == 'Enter') {
            var inputValue = inputpw.value;
            if (inputValue == birthdate) {
                $("#lock").toggle();
                $("#unlock").toggle();
            }
            else {
                $("#pw").addClass('blink');
                setTimeout(function() {
                    $("#pw").removeClass('blink');
                }, 2000);
            }
        }
    });
    
    //initially load song details into DOM
    loadSong(songs[songIndex]);


});

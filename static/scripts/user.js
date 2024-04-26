function open_tour() {
  document.getElementById('touriframe').contentWindow.location.reload();
  document.getElementById('backdrop').classList.add('open');
  document.getElementById('tourmodal').classList.add('actived');
}

var latestversion = "0.9.3";

function close_tour() {
  document.cookie = "version=" + latestversion;
  document.getElementById('backdrop').classList.remove('open');
  document.getElementById('tourmodal').classList.remove('actived');
}

var lastversion = get_cookie('version');
if (!lastversion) {
  document.cookie = "version=0";
  lastversion = 0;
}
if (lastversion != latestversion) {
  open_tour();
}

const slides = ["slide1"]
var currentslide = 0;

function gonext() {
  document.getElementById(slides[currentslide]).classList.add('inactive');
  currentslide++;
  document.getElementById(slides[currentslide]).classList.remove('inactive');
  if (currentslide == slides.length - 1) {
    document.getElementById('nextbutton').classList.add('inactive');
    document.getElementById('donebutton').classList.remove('inactive');
    document.getElementById('skipbutton').classList.add('inactive');
  }
  if (currentslide == 1) {
    document.getElementById('prevbutton').disabled = false;
  }
}

function goback() {
  document.getElementById(slides[currentslide]).classList.add('inactive');
  currentslide--;
  document.getElementById(slides[currentslide]).classList.remove('inactive');
  if (currentslide == 0) {
    document.getElementById('prevbutton').disabled = true;
  }
  if (currentslide == slides.length - 2) {
    document.getElementById('nextbutton').classList.remove('inactive');
    document.getElementById('donebutton').classList.add('inactive');
    document.getElementById('skipbutton').classList.remove('inactive');
  }
}
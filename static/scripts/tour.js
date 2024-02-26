const slides = ["slide1", "slide2", "slide3"]
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
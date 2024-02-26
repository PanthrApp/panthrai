var dotMargin = 25;
var numRows = 16;
var numCols = 16;
// Set the colors you want to support in this array
var colors = ["#FFFFFF", "#EEEEEE", "#FAFAFA", "#F0F0F0", "#F5F5F5", "#E9E9E9"];
var directions = ["+", "-"];
var speeds = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];

var canvas = $("canvas.dots");
var context = canvas[0].getContext("2d");
var canvasWidth = canvas.width();
var canvasHeight = canvas.height(); // this one is new
canvas.attr({ height: canvasHeight, width: canvasWidth });

var dotWidth = 5;
var dotHeight = 5;

var xMargin = canvasWidth / numCols;
var yMargin = canvasHeight / numRows;
var dotDiameter = 5;

// if (dotWidth > dotHeight) {
//   var dotDiameter = dotHeight;
//   var xMargin =
//     (canvasWidth - (2 * dotMargin + numCols * dotDiameter)) / numCols;
//   var yMargin = dotMargin;
// } else {
//   var xMargin = dotMargin;
//   var yMargin =
//     (canvasHeight - (2 * dotMargin + numRows * dotDiameter)) / numRows;
// }

// Start with an empty array of dots.
var dots = [];

var dotRadius = dotDiameter * 0.25;

for (var i = 0; i < numRows; i++) {
  for (var j = 0; j < numCols; j++) {
    var x = Math.floor(Math.random() * canvasWidth);
    var y = Math.floor(Math.random() * canvasHeight);
    // Get random color, direction and speed.
    var color = colors[Math.floor(Math.random() * colors.length)];
    var xMove = directions[Math.floor(Math.random() * directions.length)];
    var yMove = directions[Math.floor(Math.random() * directions.length)];
    var speed = speeds[Math.floor(Math.random() * speeds.length)];
    // Set the object.
    var dot = {
      x: x,
      y: y,
      radius: dotRadius,
      xMove: xMove,
      yMove: yMove,
      color: color,
      speed: speed,
    };
    // Save it to the dots array.
    dots.push(dot);
    drawDot(dot);
  }
}

// Draw each dot in the dots array.
for (i = 0; i < dots.length; i++) {
  drawDot(dots[i]);
}

setTimeout(function () {
  window.requestAnimationFrame(moveDot);
}, 100);

function moveDot() {
  context.clearRect(0, 0, canvasWidth, canvasHeight);

  for (i = 0; i < dots.length; i++) {
    if (dots[i].xMove == "+") {
      dots[i].x += dots[i].speed;
    } else {
      dots[i].x -= dots[i].speed;
    }
    if (dots[i].yMove == "+") {
      dots[i].y += dots[i].speed;
    } else {
      dots[i].y -= dots[i].speed;
    }

    drawDot(dots[i]);

    if (dots[i].x + dots[i].radius >= canvasWidth) {
      dots[i].xMove = "-";
    }
    if (dots[i].x - dots[i].radius <= 0) {
      dots[i].xMove = "+";
    }
    if (dots[i].y + dots[i].radius >= canvasHeight) {
      dots[i].yMove = "-";
    }
    if (dots[i].y - dots[i].radius <= 0) {
      dots[i].yMove = "+";
    }
  }

  window.requestAnimationFrame(moveDot);
}

function drawDot(dot) {
  // Set transparency on the dots.
  context.globalAlpha = 0.9;
  context.beginPath();
  context.arc(dot.x, dot.y, dot.radius, 0, 2 * Math.PI, false);
  context.fillStyle = dot.color;
  context.fill();
}

function onResize() {
  canvasWidth = canvas.width();
  canvasHeight = canvas.height();
  canvas.attr({ height: canvasHeight, width: canvasWidth });
  context.clearRect(0, 0, canvasWidth, canvasHeight);
  for (i = 0; i < dots.length; i++) {
    drawDot(dots[i]);
  }
}

window.onresize = onResize;
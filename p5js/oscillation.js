var angle = 0;

function setup() {
  createCanvas(800, 800);
  background(220);
}

function draw() {
  var x = map(cos(angle), -1, 1, 0, width);
  var y = map(sin(angle), -1, 1, 0, height);
  line(width / 5, height / 3, x, y);
  // line(width / 3, height / 3, x, y);
  ellipse(x, y, 10, 10);
  angle += 0.2;
}

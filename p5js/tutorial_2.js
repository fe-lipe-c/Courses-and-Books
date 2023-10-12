function setup() {
  createCanvas(800, 800);
  background(100);
}

function draw() {
  // background(220, 0, 200);
  rectMode(CENTER);
  fill(255, 0, 0);
  stroke(0, 255, 0);
  strokeWeight(10);
  rect(400, 400, 150, 150);

  fill(100, 130, 0, 100);
  stroke(20, 0, 110);
  strokeWeight(1);
  // noStroke();
  circle(mouseX, mouseY, 20);
}

function mousePressed() {
  background(100);
}

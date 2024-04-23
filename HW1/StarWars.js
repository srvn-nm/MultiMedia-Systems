let stars = [];
let spaceshipImage;
let speed = 1;

function preload() {
  // Preload the image
  spaceshipImage = loadImage("spaceship.webp");
  // Preload the sound
  hyperspaceSound = loadSound("Star_Wars_Hyperdrive_Sound_Effect.mp3");
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  for (let i = 0; i < 800; i++) {
    stars.push(new Star());
  }
}

function keyPressed() {
  // Adjust the speed based on UP or DOWN key press
  if (keyCode === UP_ARROW) {
    speed += 0.05;
    speed = min(speed, 4); // Limit the maximum speed
  } else if (keyCode === DOWN_ARROW) {
    speed -= 0.05;
    speed = max(speed, 0.1); // Limit the minimum speed
  }
}

function draw() {
  background(0);
  image(spaceshipImage, 0, 0, width, height); // Display the spaceship image

  // Update and display stars
  push();
  translate(width / 2, height / 2);
  stars.forEach((star) => {
    star.update();
    star.show();
  });
  pop();
}

class Star {
  constructor() {
    this.x = random(-width, width);
    this.y = random(-height, height);
    this.z = random(width);
    this.pz = this.z;
  }

  update() {
    this.z -= speed;
    if (this.z < 1) {
      this.z = width;
      this.x = random(-width, width);
      this.y = random(-height, height);
      this.pz = this.z;
    }
  }

  show() {
    fill(255);
    noStroke();

    let sx = map(this.x / this.z, 0, 1, 0, width);
    let sy = map(this.y / this.z, 0, 1, 0, height);

    let r = map(this.z, 0, width, 16, 0);
    ellipse(sx, sy, r, r);

    let px = map(this.x / this.pz, 0, 1, 0, width);
    let py = map(this.y / this.pz, 0, 1, 0, height);

    stroke(255);
    line(px, py, sx, sy);
  }
}

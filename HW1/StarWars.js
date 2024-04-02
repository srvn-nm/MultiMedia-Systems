let stars = [];
let spaceshipImage;
let hyperspaceSound;
let speed = 1; // Starting speed for hyperspace effect and sound playback rate
let audioStarted = false; // Flag to ensure audio starts correctly

function preload() {
  // Preload the image and sound; ensure these paths are correct
  spaceshipImage = loadImage("http://localhost:8080/spaceship.webp");
  hyperspaceSound = loadSound(
    "http://localhost:8080/Star_Wars_Hyperdrive_Sound_Effect.mp3"
  );
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  for (let i = 0; i < 800; i++) {
    stars.push(new Star());
  }
  // Removed audio playback from setup to comply with browser restrictions
}

function keyPressed() {
  // Use keyPressed to adjust the speed; start audio on first interaction
  if (!audioStarted) {
    hyperspaceSound.loop();
    audioStarted = true; // Prevent further attempts to start audio
  }

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

  // Adjust the playback rate of the sound based on speed
  if (audioStarted) hyperspaceSound.rate(speed);
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

document.addEventListener("DOMContentLoaded", function () {
  const videoList = document.getElementById("video-list");
  const videoPlayer = document.getElementById("player");
  const videoTitle = document.getElementById("video-title");
  const videoDetails = document.getElementById("video-details");
  const commentsList = document.getElementById("comments-list");

  const videos = [
    {
      title: "The Stand Off",
      name: "shaun_the_sheep_s03e01",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e01.mp4",
      comments: [
        { text: "Exciting episode!", sentiment: "positive" },
        { text: "Loved the plot!", sentiment: "positive" },
        { text: "Shaun is a great leader.", sentiment: "positive" },
      ],
    },
    {
      title: "The Coconut",
      name: "shaun_the_sheep_s03e02",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e02.mp4",
      comments: [
        { text: "Hilarious!", sentiment: "positive" },
        { text: "So much fun.", sentiment: "positive" },
        { text: "Great for kids.", sentiment: "positive" },
      ],
    },
    {
      title: "You Missed a Bit",
      name: "shaun_the_sheep_s03e03",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e03.mp4",
      comments: [
        { text: "Very funny!", sentiment: "positive" },
        { text: "Loved Bitzer's antics.", sentiment: "positive" },
        { text: "A must-watch.", sentiment: "positive" },
      ],
    },
    {
      title: "Let's Spray",
      name: "shaun_the_sheep_s03e04",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e04.mp4",
      comments: [
        { text: "Creative and fun!", sentiment: "positive" },
        { text: "Shaun is so mischievous.", sentiment: "positive" },
        { text: "Great episode.", sentiment: "positive" },
      ],
    },
    {
      title: "The Crow",
      name: "shaun_the_sheep_s03e05",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e05.mp4",
      comments: [
        { text: "Loved the crow!", sentiment: "positive" },
        { text: "So entertaining.", sentiment: "positive" },
        { text: "Funny and engaging.", sentiment: "positive" },
      ],
    },
    {
      title: "Shaun the Fugitive",
      name: "shaun_the_sheep_s03e06",
      year: 2012,
      genre: "Animation, Comedy",
      duration: "7:00",
      type: "local",
      file: "videos/shaun_the_sheep_s03e06.mp4",
      comments: [
        { text: "Action-packed!", sentiment: "positive" },
        { text: "Exciting plot.", sentiment: "positive" },
        { text: "Shaun is the best!", sentiment: "positive" },
      ],
    },
  ];

  // Function to update video details and comments
  function updateVideoDetails(video) {
    videoPlayer.src = video.file;
    videoTitle.textContent = video.title;
    videoDetails.textContent = `Duration: ${video.duration}, Genre: ${video.genre}, Year: ${video.year}`;
    commentsList.innerHTML = "";
    video.comments.forEach((comment) => {
      const commentItem = document.createElement("li");
      commentItem.textContent = `${comment.text} (${comment.sentiment})`;
      commentsList.appendChild(commentItem);
    });
  }

  // Create video items dynamically
  videos.forEach((video) => {
    const videoItem = document.createElement("div");
    const thumbnailSrc = `thumbnails/${video.name}.jpg`;

    // Error handling for missing thumbnails
    const img = new Image();
    img.onerror = function () {
      videoItem.innerHTML = `<div class="error-thumbnail">Thumbnail Not Found</div>`;
    };
    img.src = thumbnailSrc;

    videoItem.innerHTML = `<img src="${thumbnailSrc}" alt="${video.title}" />`;
    videoItem.addEventListener("click", () => {
      updateVideoDetails(video);
    });

    videoList.appendChild(videoItem);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const videoList = document.getElementById("video-list");
  const videoPlayer = document.getElementById("player");
  const videoTitle = document.getElementById("video-title");
  const videoDetails = document.getElementById("video-details");
  const commentsList = document.getElementById("comments-list");

  const videos = [
    {
      title: "Video 1",
      duration: "5:00",
      genre: "Genre 1",
      year: 2021,
      type: "local",
      file: "videos/video1.mp4",
      comments: [{ text: "Great video!", sentiment: "positive" }],
    },
    // Add more video objects here
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
    const thumbnailSrc = `thumbnails/${video.file}.jpg`;

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

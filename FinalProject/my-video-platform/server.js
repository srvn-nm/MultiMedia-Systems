const express = require("express");
const path = require("path");
const tf = require("@tensorflow/tfjs-node");
const qna = require("@tensorflow-models/qna");
const use = require("@tensorflow-models/universal-sentence-encoder");
const toxicity = require("@tensorflow-models/toxicity");

const app = express();
const port = 3000;

// Middleware to parse JSON requests
app.use(express.json());

// Serve static files from the parent directory
app.use(express.static(path.join(__dirname, "..")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "index.html"));
});

// Load TensorFlow models
let useModel;
let toxicityModel;

(async () => {
  useModel = await use.load();
  toxicityModel = await toxicity.load(0.9);
})();

// Endpoint for summarization
app.post("/summarize", async (req, res) => {
  const { text } = req.body;
  // Simple summarization: return the first 2 sentences
  const summary = text.split(".").slice(0, 2).join(".") + ".";
  res.json({ summary });
});

// Endpoint for sentiment analysis
app.post("/analyze", async (req, res) => {
  const { comments } = req.body;
  const results = await Promise.all(
    comments.map(async (comment) => {
      const embeddings = await useModel.embed([comment]);
      const toxicityPredictions = await toxicityModel.classify(comment);
      const toxic = toxicityPredictions.some((prediction) =>
        prediction.results.some((result) => result.match)
      );
      const sentiment = toxic ? "negative" : "positive";
      return { text: comment, sentiment };
    })
  );
  res.json(results);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

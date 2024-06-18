from transformers import pipeline

classifier = pipeline('sentiment-analysis')

comments = ["Great video!", "I didn't like it.", "Amazing content!", "Not my type of video."]

for comment in comments:
    result = classifier(comment)
    print(f"Comment: {comment}, Sentiment: {result[0]['label']}")

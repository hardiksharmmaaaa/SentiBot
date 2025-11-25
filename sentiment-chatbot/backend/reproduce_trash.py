import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

text = "Hello, I found that the product is trash, I want to return it"
score = sia.polarity_scores(text)

print(f"Text: '{text}'")
print(f"Score: {score}")

# Check 'trash' specifically
print(f"'trash' score: {sia.polarity_scores('trash')}")

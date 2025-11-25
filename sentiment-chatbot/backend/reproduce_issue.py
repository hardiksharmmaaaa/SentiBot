from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

test_cases = [
    "I am veryy veryy happpy",
    "goood",
    "bad",
    "I am happy"
]

print("Original VADER Results:")
for text in test_cases:
    print(f"'{text}': {sia.polarity_scores(text)}")

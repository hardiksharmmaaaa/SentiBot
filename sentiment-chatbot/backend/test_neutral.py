import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Setup resources
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('corpora/words.zip')
except LookupError:
    nltk.download('words')

sia = SentimentIntensityAnalyzer()
lexicon = sia.lexicon
english_words = set(nltk.corpus.words.words())

def normalize_token(token):
    token_lower = token.lower()
    if token_lower in lexicon or token_lower in english_words:
        return token
    reduced_2 = re.sub(r'(.)\1{2,}', r'\1\1', token)
    if reduced_2.lower() in lexicon or reduced_2.lower() in english_words:
        return reduced_2
    reduced_1 = re.sub(r'(.)\1+', r'\1', token)
    if reduced_1.lower() in lexicon or reduced_1.lower() in english_words:
        return reduced_1
    return token

def preprocess_text(text):
    tokens = text.split()
    normalized_tokens = [normalize_token(t) for t in tokens]
    return ' '.join(normalized_tokens)

test_cases = [
    "The sky is blue",
    "I am sitting here",
    "This is a book",
    "neutral",
    "okay",
    "fine",
    "yes",
    "no"
]

print("Neutral Test Results:")
for text in test_cases:
    normalized = preprocess_text(text)
    score = sia.polarity_scores(normalized)
    print(f"Original: '{text}' -> Normalized: '{normalized}'")
    print(f"Score: {score}")
    
    label = "Neutral"
    if score['compound'] >= 0.05:
        label = "Positive"
    elif score['compound'] <= -0.05:
        label = "Negative"
    print(f"Label: {label}")
    print("-" * 20)

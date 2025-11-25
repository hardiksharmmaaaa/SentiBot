from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
lexicon = sia.lexicon

def normalize_token(token):
    # If token is already in lexicon, return it
    if token.lower() in lexicon:
        return token
    
    # Reduce repeated characters to at most 2
    reduced_2 = re.sub(r'(.)\1{2,}', r'\1\1', token)
    if reduced_2.lower() in lexicon:
        return reduced_2
        
    # Reduce repeated characters to at most 1
    reduced_1 = re.sub(r'(.)\1+', r'\1', token)
    if reduced_1.lower() in lexicon:
        return reduced_1
    
    return token

def preprocess_text(text):
    tokens = text.split()
    normalized_tokens = [normalize_token(t) for t in tokens]
    return ' '.join(normalized_tokens)

test_cases = [
    "I am veryy veryy happpy",
    "goood",
    "bad",
    "I am happy",
    "coool",
    "amazzzing"
]

print("Normalized VADER Results:")
for text in test_cases:
    normalized = preprocess_text(text)
    print(f"Original: '{text}' -> Normalized: '{normalized}'")
    print(f"Score: {sia.polarity_scores(normalized)}")

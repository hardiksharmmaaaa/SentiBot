import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download resources
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
    # Check if already valid
    if token_lower in lexicon or token_lower in english_words:
        return token
    
    # Reduce to 2 chars
    reduced_2 = re.sub(r'(.)\1{2,}', r'\1\1', token)
    if reduced_2.lower() in lexicon or reduced_2.lower() in english_words:
        return reduced_2
        
    # Reduce to 1 char
    reduced_1 = re.sub(r'(.)\1+', r'\1', token)
    if reduced_1.lower() in lexicon or reduced_1.lower() in english_words:
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

print("Normalized VADER Results (with English Dictionary):")
for text in test_cases:
    normalized = preprocess_text(text)
    print(f"Original: '{text}' -> Normalized: '{normalized}'")
    print(f"Score: {sia.polarity_scores(normalized)}")

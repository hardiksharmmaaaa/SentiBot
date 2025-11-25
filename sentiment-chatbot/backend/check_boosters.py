from nltk.sentiment.vader import SentimentIntensityAnalyzer, VaderConstants
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
# Accessing constants might vary by version, but usually they are imported or available
# Let's try to find where BOOSTER_DICT is.
# In NLTK implementation, it's often hardcoded or imported.

print(f"'very' in lexicon: {'very' in sia.lexicon}")

# Let's try to normalize 'veryy' to 'very' manually and see the score
text_corrected = "I am very very happy"
print(f"Corrected manually: '{text_corrected}' -> {sia.polarity_scores(text_corrected)}")

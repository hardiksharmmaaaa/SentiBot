import nltk
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download resources if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('corpora/words.zip')
except LookupError:
    nltk.download('words')

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# In-memory conversation history
conversation_history = []

# Initialize the sentiment analyzer and dictionaries
sia = SentimentIntensityAnalyzer()
lexicon = sia.lexicon
english_words = set(nltk.corpus.words.words())

# Update lexicon with custom words
lexicon.update({
    'trash': -2.0,
    'garbage': -2.0,
    'scam': -2.0,
    'scammers': -2.0,
    'naive': -1.5,
})

def normalize_token(token):
    """
    Normalizes a token by reducing repeated characters to correct spelling.
    """
    token_lower = token.lower()
    # Check if already valid (in VADER lexicon or English dictionary)
    if token_lower in lexicon or token_lower in english_words:
        return token
    
    # Reduce repeated characters to at most 2 (e.g., "happpy" -> "happy")
    reduced_2 = re.sub(r'(.)\1{2,}', r'\1\1', token)
    if reduced_2.lower() in lexicon or reduced_2.lower() in english_words:
        return reduced_2
        
    # Reduce repeated characters to at most 1 (e.g., "veryy" -> "very")
    reduced_1 = re.sub(r'(.)\1+', r'\1', token)
    if reduced_1.lower() in lexicon or reduced_1.lower() in english_words:
        return reduced_1
    
    return token

def preprocess_text(text):
    """
    Preprocesses text by normalizing tokens.
    """
    tokens = text.split()
    normalized_tokens = [normalize_token(t) for t in tokens]
    return ' '.join(normalized_tokens)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles incoming chat messages, performs sentiment analysis,
    and returns a response.
    """
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Preprocess the message to handle typos/informal text
    normalized_message = preprocess_text(user_message)

    # Statement-level sentiment analysis (Tier 2)
    statement_sentiment = sia.polarity_scores(normalized_message)
    
    # Simple chatbot response logic
    if statement_sentiment['compound'] >= 0.05:
        bot_response = "I'm glad to hear that!"
    elif statement_sentiment['compound'] <= -0.05:
        bot_response = "I'm sorry to hear that. How can I help?"
    else:
        bot_response = "Thanks for sharing. Is there anything else?"

    # Store the user message and its sentiment
    conversation_history.append({
        'user_message': user_message,
        'sentiment': statement_sentiment
    })

    return jsonify({
        'bot_response': bot_response,
        'statement_sentiment': statement_sentiment
    })

@app.route('/analyze', methods=['GET'])
def analyze():
    """
    Analyzes the sentiment of the entire conversation.
    """
    if not conversation_history:
        return jsonify({'error': 'No conversation history to analyze'}), 400

    # Conversation-level sentiment analysis (Tier 1)
    # We use the raw messages here, but could normalize too if needed
    full_conversation_text = ' '.join([
        item['user_message'] for item in conversation_history
    ])
    overall_sentiment = sia.polarity_scores(full_conversation_text)

    # Optional: Summarize sentiment trend (Tier 2 Enhancement)
    sentiment_trend = [
        item['sentiment']['compound'] for item in conversation_history
    ]

    return jsonify({
        'overall_sentiment': overall_sentiment,
        'conversation_history': conversation_history,
        'sentiment_trend': sentiment_trend
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
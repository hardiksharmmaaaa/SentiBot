import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# In-memory conversation history
conversation_history = []

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles incoming chat messages, performs sentiment analysis,
    and returns a response.
    """
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Statement-level sentiment analysis (Tier 2)
    statement_sentiment = sia.polarity_scores(user_message)
    
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
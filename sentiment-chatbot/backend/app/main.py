import nltk
import re
from flask import Flask, request, jsonify, Response, stream_with_context
import json
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')

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
    
    # Create a generator for streaming the response
    def generate():
        # Yield sentiment first
        yield json.dumps({'type': 'sentiment', 'data': statement_sentiment}) + '\n'
        
        try:
            prompt = f"""
            You are a helpful and empathetic customer service representative for a company.
            The user has sent the following message: "{user_message}"
            
            The sentiment analysis of this message is: {statement_sentiment}
            (compound score > 0.05 is positive, < -0.05 is negative, else neutral)
            
            Please provide a brief, professional, and appropriate response to the user based on their sentiment.
            If they are unhappy, be apologetic and offer help.
            If they are happy, thank them.
            Keep the response concise (under 50 words).
            """
            
            response = model.generate_content(prompt, stream=True)
            full_response_text = ""
            for chunk in response:
                if chunk.text:
                    full_response_text += chunk.text
                    yield json.dumps({'type': 'chunk', 'content': chunk.text}) + '\n'
            
            # Store conversation history after full generation
            conversation_history.append({
                'user_message': user_message,
                'sentiment': statement_sentiment,
                'bot_response': full_response_text
            })
            
        except Exception as e:
            print(f"Error generating response: {e}")
            error_msg = "I apologize, but I am currently unable to generate a response. Please check my connection."
            yield json.dumps({'type': 'chunk', 'content': error_msg}) + '\n'
            
            conversation_history.append({
                'user_message': user_message,
                'sentiment': statement_sentiment,
                'bot_response': error_msg
            })

    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')

@app.route('/analyze', methods=['GET'])
def analyze():
    """
    Analyzes the sentiment of the entire conversation.
    """
    if not conversation_history:
        return jsonify({'error': 'No conversation history to analyze'}), 400

    # Conversation-level sentiment analysis (Tier 1)
    # Calculate sentiment based on the count of messages in each category
    total_messages = len(conversation_history)
    pos_count = 0
    neg_count = 0
    neu_count = 0
    total_compound = 0

    for item in conversation_history:
        compound = item['sentiment']['compound']
        total_compound += compound
        if compound >= 0.05:
            pos_count += 1
        elif compound <= -0.05:
            neg_count += 1
        else:
            neu_count += 1

    overall_sentiment = {
        'pos': pos_count / total_messages if total_messages > 0 else 0,
        'neg': neg_count / total_messages if total_messages > 0 else 0,
        'neu': neu_count / total_messages if total_messages > 0 else 0,
        'compound': total_compound / total_messages if total_messages > 0 else 0
    }

    # Optional: Summarize sentiment trend (Tier 2 Enhancement)
    sentiment_trend = [
        item['sentiment']['compound'] for item in conversation_history
    ]

    # Generate a comprehensive report using Gemini
    report_text = "Analysis unavailable."
    try:
        prompt = f"""
        Analyze the following conversation history and provide a comprehensive sentiment report.
        
        Conversation History:
        {conversation_history}
        
        Overall Sentiment Scores: {overall_sentiment}
        
        Please provide a detailed summary of:
        1. The user's overall mood and how it evolved.
        2. Key topics discussed.
        3. The effectiveness of the bot's responses.
        4. A final conclusion on the customer's satisfaction.
        
        Format the output clearly with headings.
        """
        response = model.generate_content(prompt)
        report_text = response.text
    except Exception as e:
        print(f"Error generating report: {e}")
        report_text = "Could not generate detailed report due to an error."

    return jsonify({
        'overall_sentiment': overall_sentiment,
        'conversation_history': conversation_history,
        'sentiment_trend': sentiment_trend,
        'report_text': report_text
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
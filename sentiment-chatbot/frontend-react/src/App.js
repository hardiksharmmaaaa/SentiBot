import { useState, useEffect, useRef } from 'react';
import './App.css';
import Navbar from './components/Navbar';

function App() {
  console.log('App rendering');
  const [theme, setTheme] = useState('dark');
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "I'd be happy to help you reschedule. What time works best for you?",
    },
  ]);
  const [userInput, setUserInput] = useState('');
  const messagesEndRef = useRef(null);

  const API_URL = 'http://127.0.0.1:5001';

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'dark' ? 'light' : 'dark'));
  };

  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getSentimentLabel = (compoundScore) => {
    if (compoundScore >= 0.05) return 'Positive 😊';
    if (compoundScore <= -0.05) return 'Negative 😠';
    return 'Neutral 😐';
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const userMessage = { sender: 'user', text: userInput };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    const currentInput = userInput;
    setUserInput('');

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentInput }),
      });
      const data = await response.json();

      if (data.bot_response) {
        const botMessage = { sender: 'bot', text: data.bot_response };
        setMessages((prevMessages) => {
          const lastUserMessageIndex = prevMessages.findLastIndex(
            (m) => m.sender === 'user' && !m.sentiment
          );

          if (lastUserMessageIndex !== -1) {
            const updatedMessages = [...prevMessages];
            const updatedUserMessage = {
              ...updatedMessages[lastUserMessageIndex],
              sentiment: data.statement_sentiment,
            };
            updatedMessages[lastUserMessageIndex] = updatedUserMessage;
            return [...updatedMessages, botMessage];
          }
          return [...prevMessages, botMessage];
        });
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        sender: 'bot',
        text: 'Sorry, something went wrong. Is the backend running?',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className={`App ${theme}`}>
      <Navbar theme={theme} toggleTheme={toggleTheme} />
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.sender}-wrapper`}>
              <div className={`chat-message ${msg.sender}-message`}>
                {msg.text}
              </div>
              {msg.sentiment && msg.sender === 'user' && (
                <div className="sentiment-analysis">
                  {getSentimentLabel(msg.sentiment.compound)} ({msg.sentiment.compound.toFixed(2)})
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;

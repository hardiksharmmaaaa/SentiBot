import { useState, useEffect, useRef } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import SentimentModal from './components/SentimentModal';

function App() {
  console.log('App rendering');
  const [theme, setTheme] = useState('dark');
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hi, User! How may I help you Today!! ",
    },
  ]);
  const [userInput, setUserInput] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);
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

  const getSentiment = (compoundScore) => {
    if (compoundScore >= 0.05) return { label: 'Positive 😊', className: 'sentiment-positive' };
    if (compoundScore <= -0.05) return { label: 'Negative 😠', className: 'sentiment-negative' };
    return { label: 'Neutral 😐', className: 'sentiment-neutral' };
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const messageId = Date.now();
    const userMessage = { id: messageId, sender: 'user', text: userInput };
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

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Create a placeholder bot message immediately
      const botMessageId = Date.now() + 1;
      const botMessage = { id: botMessageId, sender: 'bot', text: '' };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.trim()) continue;

          try {
            const data = JSON.parse(line);

            if (data.type === 'sentiment') {
              // Update user message with sentiment
              setMessages((prevMessages) => {
                return prevMessages.map((msg) => {
                  if (msg.id === messageId) {
                    return { ...msg, sentiment: data.data };
                  }
                  return msg;
                });
              });
            } else if (data.type === 'chunk') {
              // Append text to bot message
              setMessages((prevMessages) => {
                return prevMessages.map((msg) => {
                  if (msg.id === botMessageId) {
                    return { ...msg, text: msg.text + data.content };
                  }
                  return msg;
                });
              });
            }
          } catch (e) {
            console.error("Error parsing JSON chunk", e);
          }
        }
      }

    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now(),
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

  const handleReportClick = async () => {
    setShowModal(true);
    setLoadingReport(true);
    setReportData(null);

    try {
      const response = await fetch(`${API_URL}/analyze`);
      const data = await response.json();
      setReportData(data);
    } catch (error) {
      console.error('Error fetching report:', error);
      // Ideally show an error state in the modal
    } finally {
      setLoadingReport(false);
    }
  };

  return (
    <div className={`App ${theme}`}>
      <Navbar theme={theme} toggleTheme={toggleTheme} onReportClick={handleReportClick} />
      <SentimentModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        isLoading={loadingReport}
        reportData={reportData}
      />
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.sender}-wrapper`}>
              <div className={`chat-message ${msg.sender}-message`}>
                {msg.text}
              </div>
              {msg.sentiment && msg.sender === 'user' && (
                <div className={`sentiment-analysis ${getSentiment(msg.sentiment.compound).className}`}>
                  {getSentiment(msg.sentiment.compound).label} ({msg.sentiment.compound.toFixed(2)})
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

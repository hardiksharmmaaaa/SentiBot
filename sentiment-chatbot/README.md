# Sentiment Chatbot

This project is a chatbot that performs sentiment analysis on a conversation with a user. It meets both Tier 1 and Tier 2 requirements of the assignment.

## How to Run

### Using the Quick-Start Script

The easiest way to run the project is to use the `run.py` script located in the root of the `sentiment-chatbot` directory.

1.  **Navigate to the project directory:**
    ```bash
    cd sentiment-chatbot
    ```

2.  **Run the script:**
    ```bash
    python run.py
    ```
    This will automatically create a virtual environment, install the dependencies, and start the backend server.

3.  **Open the frontend:**
    - Navigate to the `frontend` directory and open `index.html` in your browser.

### Manual Setup

If you prefer to set up the project manually, follow these steps:

#### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd sentiment-chatbot/backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app/main.py
    ```
    The backend will be running at `http://127.0.0.1:5001`.

#### Frontend

1.  **Open the `index.html` file in your browser:**
    - Navigate to the `sentiment-chatbot/frontend` directory.
    - Open the `index.html` file directly in a web browser (e.g., by double-clicking it).

## Chosen Technologies

-   **Backend:**
    -   **Python:** The core programming language.
    -   **Flask:** A lightweight web framework for the backend API.
    -   **NLTK (Natural Language Toolkit):** Used for sentiment analysis, specifically the VADER (Valence Aware Dictionary and sEntiment Reasoner) tool.
-   **Frontend:**
    -   **HTML, CSS, JavaScript:** Standard web technologies for the user interface.

## Explanation of Sentiment Logic

The sentiment analysis is performed using NLTK's VADER sentiment analysis tool. VADER is specifically attuned to sentiments expressed in social media and other short-form text.

-   **Statement-Level Sentiment (Tier 2):** For each user message, VADER calculates a `compound` score, which is a normalized, weighted composite score that ranges from -1 (most negative) to +1 (most positive).
    -   A score `>= 0.05` is classified as **Positive**.
    -   A score `<= -0.05` is classified as **Negative**.
    -   A score between `-0.05` and `0.05` is classified as **Neutral**.

-   **Conversation-Level Sentiment (Tier 1):** At the end of the interaction, all user messages are concatenated into a single string. VADER then analyzes this combined text to produce an overall sentiment score for the entire conversation.

## Status of Tier 2 Implementation

**Completed.** The application performs and displays sentiment analysis for each individual user statement in real-time. It also provides an optional enhancement of summarizing the sentiment trend across the conversation.

## Highlights of Innovations and Enhancements

-   **Real-time Statement-Level Sentiment:** The frontend displays the sentiment of each user message immediately after it is sent, providing instant feedback.
-   **Sentiment Trend Summary:** The conversation analysis includes a list of compound sentiment scores, which can be used to visualize the trend or shift in mood over the course of the conversation.
-   **Modular and Production-Minded Structure:** The code is organized into separate `frontend` and `backend` directories, with a clear separation of concerns.

## Tests

The project includes a set of tests for the backend API. To run the tests, follow these steps:

1.  **Navigate to the backend directory:**
    ```bash
    cd sentiment-chatbot/backend
    ```

2.  **Run the tests:**
    ```bash
    python -m unittest discover -s tests
    ```
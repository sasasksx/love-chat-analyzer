import streamlit as st
from textblob import TextBlob
import re
from datetime import datetime

st.title("💌 Chat-Based Love Calculator")
st.caption("Paste chat in format: [12:30 PM] Name: message")

chat = st.text_area("Paste your chat (with timestamps):", height=300)

if st.button("Calculate Love Score"):
    pattern = r"\[(.*?)\]\s*(\w+):\s*(.+)"
    matches = re.findall(pattern, chat)

    score = 0
    previous_time = None
    total_msgs = 0

    for timestamp, sender, message in matches:
        total_msgs += 1

        # Sentiment
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            score += 5
        elif polarity < -0.3:
            score -= 5

        # Romantic keywords
        if any(word in message.lower() for word in ['love', 'miss', 'baby', 'babe']):
            score += 10

        # Emojis
        if any(e in message for e in ["❤️", "😍", "😘", "💋"]):
            score += 5

        # One-word replies
        if len(message.strip()) < 4:
            score -= 3

        # Reply time analysis
        try:
            msg_time = datetime.strptime(timestamp, "%I:%M %p")
            if previous_time:
                diff = (msg_time - previous_time).total_seconds() / 60
                if diff < 1:
                    score += 5
                elif diff < 5:
                    score += 3
                elif diff < 30:
                    score += 1
                elif diff > 60:
                    score -= 5
            previous_time = msg_time
        except:
            st.warning(f"Could not parse time: {timestamp}")

    final_score = max(0, min(100, int(score / total_msgs * 10)))
    st.success(f"Your Love Score is: 💘 {final_score}%")
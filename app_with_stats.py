import streamlit as st
from textblob import TextBlob
import re
from datetime import datetime
from collections import defaultdict, Counter

st.title("💌 Chat-Based Love Calculator")
st.caption("Upload your exported WhatsApp chat (.txt format only)")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file:
    chat = uploaded_file.read().decode("utf-8")
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} [APMapm]{2}) - (.*?): (.+)"
    matches = re.findall(pattern, chat)

    score = 0
    previous_time = None
    total_msgs = 0
    sender_stats = defaultdict(lambda: {"count": 0, "positive": 0})
    all_words = []
    all_emojis = []

    for date, time_str, sender, message in matches:
        total_msgs += 1
        sender_stats[sender]["count"] += 1

        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            score += 5
            sender_stats[sender]["positive"] += 1
        elif polarity < -0.3:
            score -= 5

        if any(word in message.lower() for word in ['love', 'miss', 'baby', 'babe']):
            score += 10
        if any(e in message for e in ["❤️", "😍", "😘", "💋"]):
            score += 5
            all_emojis.extend([e for e in message if e in "❤️😍😘💋"])

        if len(message.strip()) < 4:
            score -= 3

        # Word frequency
        words = re.findall(r'\b\w+\b', message.lower())
        all_words.extend(words)

        try:
            msg_time = datetime.strptime(time_str, "%I:%M %p")
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
            st.warning(f"Could not parse time: {time_str}")

    final_score = max(0, min(100, int(score / total_msgs * 10))) if total_msgs else 0
    st.success(f"Your Love Score is: 💘 {final_score}%")

    # Most interested sender (most positive messages)
    if sender_stats:
        most_interested = max(sender_stats.items(), key=lambda x: x[1]["positive"])[0]
        st.info(f"💘 The most interested person in this chat seems to be: **{most_interested}**")

    # Most used word
    common_words = Counter(all_words).most_common(1)
    if common_words:
        st.write(f"📌 **Most used word:** `{common_words[0][0]}` ({common_words[0][1]} times)")

    # Most used emoji
    common_emojis = Counter(all_emojis).most_common(1)
    if common_emojis:
        st.write(f"😍 **Most used emoji:** `{common_emojis[0][0]}` ({common_emojis[0][1]} times)")
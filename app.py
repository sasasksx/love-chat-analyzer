import streamlit as st
import re
from collections import Counter
import emoji

# Page settings
st.set_page_config(page_title="Chat-Based Love Calculator", page_icon="💌", layout="centered")

st.title("💌 Chat-Based Love Calculator")
st.caption("Upload your exported WhatsApp chat (.txt format only, max 100KB)")

# Upload file
uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

# Positive keywords and emoji regex
positive_words = ["love", "miss", "baby", "sweet", "dear", "heart", "cute", "kiss", "hug", "😍", "😘", "❤️", "💕", "💖", "💘", "sweetheart"]
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)

# Parse WhatsApp chat
def parse_chat(text):
    messages = []
    for line in text.split("\n"):
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{2,4}),? (\d{1,2}:\d{2})? (AM|PM)? - ([^:]+): (.+)', line)
        if match:
            sender = match.group(4)
            message = match.group(5)
            messages.append((sender, message))
    return messages

# Calculate love score
def calculate_love_score(messages):
    score = 0
    interest = Counter()
    word_counter = Counter()
    emoji_counter = Counter()

    for sender, msg in messages:
        lowered = msg.lower()
        if any(word in lowered for word in positive_words):
            score += 1
            interest[sender] += 1
        word_counter.update(re.findall(r'\b\w+\b', lowered))
        emoji_counter.update(emoji_pattern.findall(msg))

    if messages:
        score = int((score / len(messages)) * 100)

    return score, interest, word_counter, emoji_counter

# File processing
if uploaded_file is not None:
    file_size_kb = len(uploaded_file.read()) / 1024
    uploaded_file.seek(0)

    if file_size_kb > 100:
        st.error("❌ File too large! Please upload a file smaller than 100 KB.")
    else:
        text = uploaded_file.read().decode("utf-8")
        messages = parse_chat(text)

        if not messages:
            st.warning("⚠️ Could not detect any valid messages. Make sure it's an exported WhatsApp chat.")
        else:
            score, interest, word_counter, emoji_counter = calculate_love_score(messages)
            st.success(f"💘 Your Love Score is: {score}%")

            st.subheader("📊 Chat Analysis:")

            if interest:
                most_interested = interest.most_common(1)[0][0]
                st.write(f"**Most Interested Person:** {most_interested}")

            if word_counter:
                most_common_word = word_counter.most_common(1)[0][0]
                st.write(f"**Most Used Word:** {most_common_word}")

            if emoji_counter:
                most_common_emoji = emoji_counter.most_common(1)[0][0]
                st.write(f"**Most Used Emoji:** {most_common_emoji}")
else:
    st.info("Please upload a WhatsApp chat file (.txt). You can export this from WhatsApp → More → Export Chat.")

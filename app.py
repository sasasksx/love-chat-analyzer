import streamlit as st
import re
from collections import Counter
import emoji

st.set_page_config(page_title="Chat-Based Love Calculator", page_icon="💌", layout="centered")

st.title("💌 Chat-Based Love Calculator")
st.caption("Upload your exported WhatsApp chat (.txt format only)")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

positive_words = ["love", "miss", "baby", "sweet", "dear", "heart", "cute", "kiss", "hug", "😍", "😘", "❤️", "💕", "💖", "💘", "sweetheart"]
emoji_pattern = emoji.get_emoji_regexp()

def parse_chat(text):
    messages = []
    for line in text.split("\n"):
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{2,4}),? (\d{1,2}:\d{2})? (AM|PM)? - ([^:]+): (.+)', line)
        if match:
            sender = match.group(4)
            message = match.group(5)
            messages.append((sender, message))
    return messages

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
        emoji_counter.update(char for char in msg if char in emoji.EMOJI_DATA)

    if messages:
        score = int((score / len(messages)) * 100)

    return score, interest, word_counter, emoji_counter

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    messages = parse_chat(text)

    if not messages:
        st.warning("Could not detect chat messages in the file. Make sure it's the exported WhatsApp chat.")
    else:
        score, interest, word_counter, emoji_counter = calculate_love_score(messages)
        st.success(f"Your Love Score is: ❤️ {score}%")

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
    st.info("Please upload a WhatsApp chat file (.txt). You can export this from your chat → More → Export Chat.")


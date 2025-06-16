import streamlit as st
from pinecone_utils import query_index
from groq import Groq
import os
from dotenv import load_dotenv
import asr
import sounddevice as sd
import numpy as np
import translate


# Load environment variables
load_dotenv()
# Setup Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Setup ASR
DURATION = 10 # seconds
SAMPLING_RATE = 16000


st.set_page_config(page_title="Boudhi Chatbot", layout="centered")
st.title("💬 Ask Boudhi – Your Scheme Assistant")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "state" not in st.session_state:
    st.session_state.state = {}

#Store empty transcript string
transcript = ""

if st.button("Start Recording"):
    st.write("Recording... Speak now!")
    audio = sd.rec(int(DURATION * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=1, dtype='float32')
    sd.wait()
    st.write("Transcribing...")

    # Transcribe with your custom ASR function
    transcript = asr.transcribe((SAMPLING_RATE, audio))
    st.success("Transcription:")
    st.write(transcript)


query = st.chat_input("Ask about schemes, benefits, eligibility...", key = "user_input")
user_input = transcript if transcript else query

if user_input:
    # Retrieve relevant schemes
    search_results = query_index(user_input)
    retrieved_info = "\n\n".join(
        f"Scheme: {m.metadata.get('scheme_name', '')}\nDetails: {m.metadata}" for m in search_results.matches
    )

    # System prompt + full chat history
    system_prompt = (
        "You are a helpful assistant for Indian government schemes. "
        "Use the retrieved scheme data to answer questions accurately and clearly."
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages += st.session_state.chat_history
    messages.append({
        "role": "user",
        "content": f"{user_input}\n\nContext:\n{retrieved_info}"
    })

    # Save user query
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call Groq
    with st.spinner("Boudhi is thinking..."):
        try:
            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error from Groq API: {e}"

        # Save assistant reply
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Show messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

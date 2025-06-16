import streamlit as st
from pinecone_utils import query_index
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Boudhi Chatbot", layout="centered")
st.title("💬 Ask Boudhi – Your Scheme Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input("Ask about schemes, benefits, eligibility...")

if query:
    # Retrieve relevant schemes
    search_results = query_index(query)
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
        "content": f"{query}\n\nContext:\n{retrieved_info}"
    })

    # Save user query
    st.session_state.chat_history.append({"role": "user", "content": query})

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
#---
#Translation layer.
#---


# Show messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

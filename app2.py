import os
import json
import requests
import streamlit as st


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set your PaLM API Key
os.environ['PALM_API_KEY'] = "AIzaSyAqL5QXqg1pjVOSNkD58FDtRlfQTZMLALM"

def generate_text(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={os.getenv('PALM_API_KEY')}"

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "prompt": {
            "text": prompt
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        generated_text = response.json()
        return generated_text
    else:
        return f"Failed to generate text. Status code: {response.status_code}"

# Streamlit app with enhanced UI
def main():
    # Set page title and configure layout
    st.set_page_config(
        page_title="AI Text Generation with Streamlit",
        page_icon="🤖",
        layout="wide"
    )

    # Add custom CSS for styling
    st.markdown(
        """
        <style>
            body {
                color: #333;
                background-color: #f8f9fa;
            }
            .sidebar .sidebar-content {
                background-color: #343a40;
                color: #fff;
            }
            .stTextInput, .stTextArea, .stButton {
                margin-top: 10px;
                margin-bottom: 10px;
            }
            .stButton {
                background-color: #007bff;
                color: #fff;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            .stButton:hover {
                background-color: #0056b3;
            }
            .stMarkdown {
                font-size: 18px;
            }
            .chat-container {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
            }
            .user-message {
                background-color: #007bff;
                color: #fff;
                padding: 8px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
            .ai-message {
                background-color: #28a745;
                color: #fff;
                padding: 8px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar with additional options
    st.sidebar.header("Settings")
    user_name = st.sidebar.text_input("Your Name", "User")

    # Main content
    st.title(f"Hello, {user_name}! 🤖 Let's chat:")
    user_prompt = st.text_area("Your Message", "Once upon a time, ")

    if st.button("Send"):
        if user_prompt.lower() == 'exit':
            st.warning("Conversation ended.")
        else:
            result = generate_text(user_prompt)

            if 'candidates' in result and len(result['candidates']) > 0:
                generated_output = result['candidates'][0]['output']
                st.subheader("AI's Response:")
                st.write(generated_output)

                # Display the conversation in a chat-like format
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.markdown(f"<div class='user-message'>{user_name}: {user_prompt}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='ai-message'>AI: {generated_output}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.warning("AI: Unable to generate a response.")

if __name__ == "__main__":
    main()

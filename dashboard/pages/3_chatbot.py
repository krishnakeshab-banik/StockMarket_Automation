import streamlit as st
import openai
from datetime import datetime

def get_ai_response(prompt, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful stock market advisor."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🤖 AI Investment Advisor")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about investments..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get context from portfolio and sentiment data
        context = "Portfolio contains stocks in RELIANCE, TCS, and INFOSYS. Market sentiment is generally positive."
        
        # Get AI response
        response = get_ai_response(prompt, context)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

import streamlit as st
import openai

# Configure OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit App Title
st.title("WebFOCUS to SQL Translator using ChatGPT-4 Turbo")

# Text Area for WebFOCUS Input
webfocus_code = st.text_area("Enter WebFOCUS Code:", height=300, placeholder="Paste your WebFOCUS code here...")

# Button to Trigger Translation
if st.button("Translate to SQL"):
    if not webfocus_code.strip():
        st.error("Please provide WebFOCUS code to translate.")
    else:
        # Prompt Engineering for Translation
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert in database query languages specializing in SQL Server. Your task is to "
                    "translate WebFOCUS code into optimized SQL Server syntax. Handle WHERE clauses, JOINs, "
                    "aggregations, and ensure clean, well-formatted output. Avoid unnecessary complexity."
                )
            },
            {
                "role": "user",
                "content": f"Translate the following WebFOCUS code into SQL Server syntax:\n\n{webfocus_code}"
            }
        ]

        try:
            # OpenAI API Call
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=3000,  # Increase token limit for detailed responses
                temperature=0  # Deterministic output for precise translation
            )
            sql_translation = response["choices"][0]["message"]["content"].strip()

            # Display Result
            st.success("Translation Complete!")
            st.text_area("SQL Translation:", sql_translation, height=300)

        except Exception as e:
            st.error(f"An error occurred during translation: {e}")

# Footer
st.markdown("---")
st.markdown("Powered by Streamlit and OpenAI ChatGPT-4 Turbo")

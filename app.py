import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import openai

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Prompt template for translation
webfocus_to_sql_prompt = """
You are an expert in translating WebFOCUS code into SQL Server queries. 
Follow these guidelines:
1. Handle WHERE, IF, PRINT, and BY keywords from WebFOCUS.
2. Translate 'MISSING' to 'IS NULL'.
3. Translate operators: GT -> >, LT -> <, NE -> <>, EQ -> =.
4. Include JOIN logic where necessary.

Translate the following WebFOCUS code into SQL:
{webfocus_code}
"""

prompt_template = PromptTemplate(
    input_variables=["webfocus_code"], 
    template=webfocus_to_sql_prompt
)

# Initialize the OpenAI LLM through LangChain
llm = OpenAI(temperature=0.2, model="gpt-4")  # You can also use "gpt-3.5-turbo"
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit UI
st.title("WebFOCUS to SQL Translator with Prompt Engineering")
st.markdown("""
This app translates WebFOCUS code into SQL Server syntax using OpenAI's GPT models. 
You can customize the prompt to experiment with different translation outputs.
""")

# Input area for WebFOCUS code
webfocus_code = st.text_area(
    "Enter WebFOCUS Code:",
    height=300,
    placeholder="Paste your WebFOCUS code here..."
)

# Button to trigger translation
if st.button("Translate to SQL"):
    if webfocus_code.strip():
        with st.spinner("Translating WebFOCUS to SQL..."):
            try:
                # Use LangChain chain to translate the WebFOCUS code
                sql_translation = chain.run({"webfocus_code": webfocus_code})
                
                # Display result
                st.success("Translation Complete!")
                st.text_area("SQL Translation:", sql_translation, height=300)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter WebFOCUS code before translating!")

# Prompt customization area
st.markdown("### Customize Prompt")
st.text_area(
    "Prompt Template",
    value=webfocus_to_sql_prompt,
    height=200,
    help="Modify the prompt template to see how the translation changes."
)

st.markdown("---")
st.markdown("Powered by OpenAI and LangChain")


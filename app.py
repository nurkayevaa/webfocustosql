import streamlit as st
import re

# Function to clean WebFOCUS code
def clean_webfocus_code(webfocus_code):
    """
    Cleans WebFOCUS code by:
    - Removing comments and blank lines.
    """
    # Remove WebFOCUS comments (lines starting with -*)
    code_without_comments = re.sub(r"^\s*(-\*.*)$", "", webfocus_code, flags=re.MULTILINE)
    
    # Remove blank lines
    cleaned_code = "\n".join([line for line in code_without_comments.splitlines() if line.strip()])
    return cleaned_code

# Function to translate WebFOCUS to SQL
def translate_webfocus_to_sql(webfocus_code):
    """
    Translates basic WebFOCUS code into SQL Server syntax.
    """
    # Example mapping logic
    sql_lines = []
    for line in webfocus_code.splitlines():
        if "TABLE FILE" in line.upper():
            table_name = line.split()[-1]
            sql_lines.append(f"SELECT")
        elif "SUM" in line.upper():
            columns = line.replace("SUM", "").strip()
            sql_lines.append(f"    SUM({columns})")
        elif "BY" in line.upper():
            group_by_column = line.split()[-1]
            sql_lines.append(f"FROM {table_name}")
            sql_lines.append(f"GROUP BY {group_by_column};")
        elif "END" in line.upper():
            continue
        else:
            sql_lines.append(f"-- Unhandled line: {line}")
    
    return "\n".join(sql_lines)

# Streamlit app setup
st.title("WebFOCUS to SQL Server Translator")
st.markdown("Paste your WebFOCUS code below to translate it into SQL Server language.")

# Text input area for WebFOCUS code
webfocus_code = st.text_area("Enter WebFOCUS Code:", height=300, placeholder="Paste your WebFOCUS code here...")

# Button to trigger translation
if st.button("Translate to SQL Server"):
    if webfocus_code.strip():
        with st.spinner("Translating WebFOCUS to SQL Server..."):
            try:
                # Clean the WebFOCUS code
                cleaned_code = clean_webfocus_code(webfocus_code)
                
                # Translate WebFOCUS to SQL
                sql_translation = translate_webfocus_to_sql(cleaned_code)

                # Display result
                st.success("Translation Complete!")
                st.text_area("SQL Translation:", sql_translation, height=300)
            except Exception as e:
                st.error(f"An error occurred during translation: {str(e)}")
    else:
        st.warning("Please enter WebFOCUS code before translating!")

# Footer
st.markdown("---")
st.markdown("Powered by Streamlit")

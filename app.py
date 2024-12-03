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

# Function to translate WebFOCUS to SQL with enhanced support for WHERE, IF, and JOIN
def translate_webfocus_to_sql(webfocus_code):
    """
    Translates WebFOCUS code into SQL Server syntax.
    """
    select_columns = []
    table_name = None
    where_conditions = []
    join_conditions = None

    for line in webfocus_code.splitlines():
        line_upper = line.upper()
        
        # Detect table declaration
        if "TABLE FILE" in line_upper:
            table_name = line.split()[-1]
        
        # Detect WHERE or IF conditions
        elif line_upper.startswith("WHERE") or line_upper.startswith("IF"):
            condition = line.replace("WHERE", "").replace("IF", "").strip()
            where_conditions.append(condition)
        
        # Detect PRINT for SELECT columns
        elif line_upper.startswith("PRINT"):
            columns = line.replace("PRINT", "").strip()
            select_columns.extend(columns.split())
        
        # Detect ON TABLE for additional clauses (like JOIN or OUTPUT FORMAT)
        elif line_upper.startswith("ON TABLE"):
            if "PCHOLD" in line_upper:
                join_conditions = "DATEOFREC"  # Extracted example; can be adjusted to detect specific joins
        
        # Detect END statement to finalize
        elif "END" in line_upper:
            break

    # Construct the SQL query
    sql_query = "SELECT " + ", ".join(select_columns)
    sql_query += f"\nFROM {table_name}"
    if where_conditions:
        sql_query += "\nWHERE " + " and ".join(where_conditions)
    if join_conditions:
        sql_query += f"\nJOIN ON TABLE PCHOLD {join_conditions};"

    return sql_query

# Streamlit app setup
st.title("WebFOCUS to SQL Server Translator with Enhanced WHERE and JOIN Handling")
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

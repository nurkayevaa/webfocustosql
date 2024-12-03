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
    Translates WebFOCUS code into SQL Server syntax.
    """
    select_columns = []
    table_name = None
    where_conditions = []
    join_condition = None
    group_by_column = None

    for line in webfocus_code.splitlines():
        line_upper = line.upper()
        
        # Detect table declaration
        if "TABLE FILE" in line_upper:
            table_name = line.split()[-1]
        
        # Detect WHERE or IF conditions
        elif line_upper.startswith("WHERE") or line_upper.startswith("IF"):
            condition = line.replace("WHERE", "").replace("IF", "").strip()
            # Replace WebFOCUS operators with SQL operators
            condition = (
                condition.replace("IS MISSING", "IS NULL")
                         .replace("GT", ">")
                         .replace("LT", "<")
                         .replace("EQ", "=")
                         .replace("NE", "<>")
            )
            where_conditions.append(condition)
        
        # Detect PRINT for SELECT columns
        elif line_upper.startswith("PRINT"):
            columns = line.replace("PRINT", "").strip()
            select_columns.extend(columns.split())
        
        # Detect BY for GROUP BY clause
        elif line_upper.startswith("BY"):
            group_by_column = line.split()[-1]
            select_columns.append(group_by_column)  # Ensure it's in SELECT
        
        # Detect ON TABLE for additional clauses (like JOIN)
        elif line_upper.startswith("ON TABLE"):
            if "PCHOLD" in line_upper:
                join_condition = "JRNL_ACTG.DATEOFREC = PCHOLD.DATEOFREC"  # Example condition
        
        # Detect END statement to finalize
        elif "END" in line_upper:
            break

    # Construct the SQL query
    sql_query = f"SELECT {', '.join(select_columns)}"
    sql_query += f"\nFROM {table_name}"
    if where_conditions:
        sql_query += "\nWHERE " + " AND ".join(where_conditions)
    if join_condition:
        sql_query += f"\nJOIN PCHOLD\n  ON {join_condition};"

    return sql_query

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

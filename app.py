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

# Function to translate WebFOCUS to SQL, including joins
def translate_webfocus_to_sql(webfocus_code):
    """
    Translates basic WebFOCUS code into SQL Server syntax, including joins.
    """
    sql_lines = []
    join_condition = None
    table_name = None
    select_columns = []
    group_by_column = None

    for line in webfocus_code.splitlines():
        line_upper = line.upper()
        
        # Detect table declaration
        if "TABLE FILE" in line_upper:
            table_name = line.split()[-1]
        
        # Detect SUM for aggregation
        elif "SUM" in line_upper:
            columns = line.replace("SUM", "").strip()
            select_columns.append(f"SUM({columns})")
        
        # Detect BY for GROUP BY clause
        elif "BY" in line_upper:
            group_by_column = line.split()[-1]
            select_columns.append(group_by_column)
        
        # Detect JOIN statements
        elif "JOIN" in line_upper:
            join_parts = re.split(r"\s+ON\s+", line, flags=re.IGNORECASE)
            if len(join_parts) == 2:
                join_table = join_parts[0].split()[-1]
                join_condition = join_parts[1]
                sql_lines.append(f"JOIN {join_table} ON {join_condition}")
        
        # End statement handling
        elif "END" in line_upper:
            # Finalize the SQL query
            sql_lines.insert(0, f"SELECT {', '.join(select_columns)}")
            sql_lines.insert(1, f"FROM {table_name}")
            if group_by_column:
                sql_lines.append(f"GROUP BY {group_by_column};")
            break

        else:
            sql_lines.append(f"-- Unhandled line: {line}")

    return "\n".join(sql_lines)

# Streamlit app setup
st.title("WebFOCUS to SQL Server Translator with Joins")
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

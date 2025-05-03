import streamlit as st 
import pandas as pd 
from io import BytesIO
import os

st.set_page_config(page_title="File Converter & Cleaner", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload your CSV and Excel files to clean the data and convert formats effortlessly.")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for idx, file in enumerate(files):
        ext = file.name.split(".")[-1].lower()
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}", key=f"fill_{idx}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing values filled successfully")

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns.tolist(), default=df.columns.tolist(), key=f"cols_{idx}")
        df = df[selected_columns]

        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}", key=f"chart_{idx}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, 0])

        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=f"format_{idx}")
        if st.button(f"Download {file.name} as {format_choice}", key=f"download_{idx}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            output.seek(0)
            base_name, _ = os.path.splitext(file.name)
            new_name = f"{base_name}.{format_choice.lower()}"
            st.download_button(label="Download File", file_name=new_name, data=output, mime=mime)
            st.success("Processing complete!")

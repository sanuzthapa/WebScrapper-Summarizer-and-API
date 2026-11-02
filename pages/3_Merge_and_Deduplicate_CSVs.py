import streamlit as st
import pandas as pd

st.title("🧮 Merge and Deduplicate CSV Summary Files")

uploaded_files = st.file_uploader("Upload one or more CSV files", type="csv", accept_multiple_files=True)
if uploaded_files:
    combined_df = pd.concat([pd.read_csv(f) for f in uploaded_files])
    deduped_df = combined_df.drop_duplicates(subset=["Link"])
    st.dataframe(deduped_df)
    csv_filename = "merged_deduped_summaries.csv"
    deduped_df.to_csv(csv_filename, index=False)
    st.download_button("Download Merged CSV", deduped_df.to_csv(index=False), file_name=csv_filename)

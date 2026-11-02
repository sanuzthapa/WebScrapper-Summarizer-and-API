import streamlit as st
import pandas as pd
from rss_parser.parser import summarize_article, extract_content_from_url
import os
import datetime
import time

st.set_page_config(page_title="CSV URL Summarizer", layout="wide")
st.title("📂 Summarize Articles from CSV URLs")

uploaded_file = st.file_uploader("Upload CSV with a 'Link' column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Link' not in df.columns:
        st.error("❌ Uploaded CSV must contain a 'Link' column.")
    else:
        st.info(f"🔎 Found **{len(df)}** links. Starting summarization...")

        summaries = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, row in df.iterrows():
            url = row['Link']
            try:
                status_text.info(f"🔗 Processing ({index + 1}/{len(df)}): {url}")
                full_text = extract_content_from_url(url)
                summary = summarize_article(full_text)
                summaries.append({
                    "Link": url,
                    "Original Content": full_text,
                    "Summary": summary
                })
                st.success(f"✅ Done: {url}")
            except Exception as e:
                st.warning(f"⚠️ Failed to summarize {url}: {e}")
            
            progress_bar.progress((index + 1) / len(df))
            time.sleep(0.2)

        progress_bar.empty()
        status_text.empty()

        if summaries:
            result_df = pd.DataFrame(summaries)
            st.success("🎉 Summarization completed!")
            st.dataframe(result_df, use_container_width=True)

            # Save to CSV with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            csv_filename = f"url_summaries_{timestamp}.csv"
            result_df.to_csv(csv_filename, index=False)
            
            st.download_button(
                "📥 Download Summary CSV",
                result_df.to_csv(index=False),
                file_name=csv_filename,
                mime='text/csv'
            )
        else:
            st.warning("No summaries were generated.")

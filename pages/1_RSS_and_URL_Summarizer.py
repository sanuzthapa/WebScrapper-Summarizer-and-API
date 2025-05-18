import streamlit as st
import pandas as pd
import datetime
import os
from rss_parser.parser import summarize_article, extract_content_from_url, parse_rss

st.set_page_config(page_title="RSS and URL Summarizer", layout="wide")
st.title("📰 RSS Feed and URL Summarizer")

# Session state to persist data
if 'rss_data' not in st.session_state:
    st.session_state.rss_data = pd.DataFrame(columns=['Title', 'Link', 'Published', 'Original Content', 'Summary'])

if 'direct_url_data' not in st.session_state:
    st.session_state.direct_url_data = pd.DataFrame(columns=['Title', 'Link', 'Published', 'Original Content', 'Summary'])

# Tab-like navigation
tab1, tab2 = st.tabs(["RSS Feed URL", "Direct Article URL"])

with tab1:
    # Clear all summaries button for RSS Feed
    col_clear_all, _ = st.columns([1, 5])
    with col_clear_all:
        if not st.session_state.rss_data.empty:
            if st.button("🧹 Clear All", key="clear_rss_all", use_container_width=True):
                st.session_state.rss_data = pd.DataFrame(columns=['Title', 'Link', 'Published', 'Original Content', 'Summary'])
                st.toast("🗑 All RSS articles cleared!", icon="🗑")
                st.rerun()

    rss_url = st.text_input("Enter RSS Feed URL")
    if st.button("Parse RSS", key="parse_rss_button"):
        with st.spinner("Fetching RSS feed and summarizing articles..."):
            try:
                articles = parse_rss(rss_url)
                new_data = []
                progress = st.progress(0)

                for idx, art in enumerate(articles):
                    try:
                        full_content = extract_content_from_url(art['link'])
                        summary = summarize_article(full_content)
                        published = art.get('published', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        new_data.append({
                            'Title': art.get('title', 'No Title'),
                            'Link': art['link'],
                            'Published': published,
                            'Original Content': full_content,
                            'Summary': summary
                        })
                        st.session_state.rss_data = pd.concat([pd.DataFrame([new_data[-1]]), st.session_state.rss_data], ignore_index=True)
                        progress.progress((idx + 1) / len(articles))
                        st.toast(f"✅ Processed: {art.get('title', 'No Title')}", icon="✅")
                    except Exception as inner_e:
                        st.toast(f"⚠️ Skipped article: {inner_e}", icon="⚠️")
                        continue

                st.toast("🎉 RSS articles summarized successfully!", icon="🎉")
            except Exception as e:
                st.error(f"Failed to process RSS feed: {e}")

    # Display summarized RSS data
    if not st.session_state.rss_data.empty:
        st.markdown("## 📄 Summarized RSS Articles")

        # Reverse index for newest on top
        for i in st.session_state.rss_data.index[::-1]:
            row = st.session_state.rss_data.loc[i]
            with st.expander(f"{row['Title']} — {row['Published']}", expanded=False):
                st.markdown(f"### 🔗 [View Article]({row['Link']})")

                st.markdown("**Original Content:**")
                st.text_area("", row['Original Content'], height=200, key=f"rss_original_{i}")

                st.markdown("**Summary:**")
                st.text_area("", row['Summary'], height=200, key=f"rss_summary_{i}")

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("📋 Copy Original", key=f"rss_copy_orig_{i}"):
                        st.toast("Copied Original Content", icon="📋")
                with col2:
                    if st.button("📋 Copy Summary", key=f"rss_copy_sum_{i}"):
                        st.toast("Copied Summary", icon="📋")
                with col3:
                    if st.button("❌ Clear This Post", key=f"rss_clear_{i}"):
                        st.session_state.rss_data.drop(index=i, inplace=True)
                        st.session_state.rss_data.reset_index(drop=True, inplace=True)
                        st.toast("❌ Post cleared", icon="🗑")
                        st.rerun()

    st.markdown("## 🧾 Summary Table")
    display_df = st.session_state.rss_data[['Title', 'Link', 'Summary']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if st.button("💾 Save to CSV", key="save_rss_csv"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"summarized_rss_articles_{timestamp}.csv"
        filepath = os.path.join(os.getcwd(), filename)
        st.session_state.rss_data.to_csv(filepath, index=False)
        st.success(f"Saved to {filename}")

with tab2:
    # Clear all summaries button for Direct Article URL
    col_clear_all, _ = st.columns([1, 5])
    with col_clear_all:
        if not st.session_state.direct_url_data.empty:
            if st.button("🧹 Clear All", key="clear_url_all", use_container_width=True):
                st.session_state.direct_url_data = pd.DataFrame(columns=['Title', 'Link', 'Published', 'Original Content', 'Summary'])
                st.toast("🗑 All Direct articles cleared!", icon="🗑")
                st.rerun()

    direct_url = st.text_input("Enter article URL")
    if st.button("Summarize URL", key="summarize_url_button"):
        with st.spinner("Extracting and summarizing article from URL..."):
            try:
                content = extract_content_from_url(direct_url)
                summary = summarize_article(content)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                entry = pd.DataFrame([{
                    'Title': direct_url,
                    'Link': direct_url,
                    'Published': now,
                    'Original Content': content,
                    'Summary': summary
                }])
                st.session_state.direct_url_data = pd.concat([entry, st.session_state.direct_url_data], ignore_index=True)
                st.toast("✅ Article summarized successfully!", icon="✅")
            except Exception as e:
                st.error(f"Failed to summarize article: {e}")

    # Display summarized Direct Article URL data
    if not st.session_state.direct_url_data.empty:
        st.markdown("## 📄 Summarized Direct Article URLs")

        # Reverse index for newest on top
        for i in st.session_state.direct_url_data.index[::-1]:
            row = st.session_state.direct_url_data.loc[i]
            with st.expander(f"{row['Title']} — {row['Published']}", expanded=False):
                st.markdown(f"### 🔗 [View Article]({row['Link']})")

                st.markdown("**Original Content:**")
                st.text_area("", row['Original Content'], height=200, key=f"url_original_{i}")

                st.markdown("**Summary:**")
                st.text_area("", row['Summary'], height=200, key=f"url_summary_{i}")

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("📋 Copy Original", key=f"url_copy_orig_{i}"):
                        st.toast("Copied Original Content", icon="📋")
                with col2:
                    if st.button("📋 Copy Summary", key=f"url_copy_sum_{i}"):
                        st.toast("Copied Summary", icon="📋")
                with col3:
                    if st.button("❌ Clear This Post", key=f"url_clear_{i}"):
                        st.session_state.direct_url_data.drop(index=i, inplace=True)
                        st.session_state.direct_url_data.reset_index(drop=True, inplace=True)
                        st.toast("❌ Post cleared", icon="🗑")
                        st.rerun()

    st.markdown("## 🧾 Summary Table")
    display_df = st.session_state.direct_url_data[['Title', 'Link', 'Summary']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if st.button("💾 Save to CSV", key="save_url_csv"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"summarized_direct_articles_{timestamp}.csv"
        filepath = os.path.join(os.getcwd(), filename)
        st.session_state.direct_url_data.to_csv(filepath, index=False)
        st.success(f"Saved to {filename}")

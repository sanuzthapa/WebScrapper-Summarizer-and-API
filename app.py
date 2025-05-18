import streamlit as st
from PIL import Image

# Set wide layout and custom title
st.set_page_config(page_title="RSS Summarizer Suite", layout="wide")

# Optional: Add your own logo
# logo = Image.open("logo.png")
# st.image(logo, width=100)

# Header Banner
st.markdown("""
<style>
.big-font {
    font-size: 40px !important;
    font-weight: bold;
    color: #222B5F;
}
.sub-font {
    font-size: 20px !important;
    color: #555;
}
.section {
    background-color: #F8F9FA;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font">🧠 RSS & URL Summarizer Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-font">Smart tools to extract, clean and summarize your content at scale</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-font"> Designed for <a href="https://www.garance-formations.fr" target="_blank">Garance Formations. </a>  </div>', unsafe_allow_html=True)

st.markdown("---")

# Section with links
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("""
### 📂 Available Tools:
- 🔗 **[RSS and URL Summarizer](./1_RSS_and_URL_Summarizer)**: Summarize a single URL or RSS feed.
- 📄 **[Summarize from CSV URLs](./2_Summarize_from_CSV_URLs)**: Upload CSV with URLs and get summaries.
- 🧹 **[Merge CSVs and Remove Duplicates](./3_Merge_and_Deduplicate_CSVs)**: Combine multiple CSVs into one clean file.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('© 2025 Summarizer App | Built with ❤️ by <a href="https://sanuzthapa.github.io/" target="_blank">S</a> using Streamlit', unsafe_allow_html=True)

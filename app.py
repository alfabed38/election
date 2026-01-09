import streamlit as st
import streamlit.components.v1 as components
import os

# Set page config
st.set_page_config(page_title="Türkiye Seçim Simülatörü", layout="wide")

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    st.title("Türkiye Seçim Simülatörü (2025-2027)")
    st.info("Bu uygulama HTML/JS tabanlıdır ve Streamlit üzerinden sunulmaktadır. Tüm simülasyon tarayıcınızda çalışır.")

    try:
        # Read HTML and JS
        html_content = load_file("index.html")
        js_content = load_file("polls.js")

        # Inject JS content directly into HTML to avoid path issues in Streamlit iframe
        # Replace the script tag
        full_html = html_content.replace('<script src="polls.js"></script>', f'<script>{js_content}</script>')

        # Render
        # Adjust height as needed (1200px covers most of the dashboard)
        components.html(full_html, height=1200, scrolling=True)

    except Exception as e:
        st.error(f"Dosyalar yüklenirken hata oluştu: {e}")
        st.warning("Lütfen index.html ve polls.js dosyalarının app.py ile aynı klasörde olduğundan emin olun.")

if __name__ == "__main__":
    main()

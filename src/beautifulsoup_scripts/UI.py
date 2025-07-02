import streamlit as st

def show_header():
    st.title("Wuzzuf Job Scraper")
    st.markdown("Scrape job listings from Wuzzuf based on your search query.")

def get_user_input():
    search_query = st.text_input("Search Keyword", "data science")
    max_jobs = st.slider("Max Jobs to Scrape", min_value=10, max_value=200, value=20, step=10)

    return search_query, max_jobs

def show_results(df):
    st.success(f"Scraped {len(df)} jobs.")
    st.dataframe(df)

    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("Download CSV", csv, "wuzzuf_jobs.csv", "text/csv")

def show_error(error_msg):
    st.error(f" {error_msg}")

import streamlit as st
from beautifulsoup_scripts.job_scraping import scrape_jobs
from beautifulsoup_scripts.UI import show_header, get_user_input, show_results, show_error

def main():
    show_header()

    search_query, max_jobs = get_user_input()

    if st.button("Start Scraping"):
        if not search_query or search_query.strip() == "":
            st.warning("Please enter a search query before scraping.")
            return 
        
        base_url = f"https://wuzzuf.net/search/jobs/?a=navbl%7Cspbl&q={search_query.replace(' ', '%20')}&start"
        try:
            with st.spinner("Scraping jobs..."):
                df = scrape_jobs(base_url=base_url, max_jobs=max_jobs)
                if df.empty:
                    show_error("No jobs found or scraping failed.")
                else:
                    show_results(df)
        except Exception as e:
            show_error(str(e))

if __name__ == "__main__":
    main()

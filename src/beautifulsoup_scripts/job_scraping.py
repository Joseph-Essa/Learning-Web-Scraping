import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os



def scrape_jobs(max_jobs=None, base_url=None):
    
    full_url = base_url + "={}"
    page = 0
    scraped_jobs = 0

    all_titles = []
    all_links = []
    all_companies = []
    all_exp_levels = []
    all_exp_years = []
    all_job_types = []
    all_work_modes = []
    all_skills = []

    while True:
        url = full_url.format(page)
        print(f"Scraping page {page + 1}: {url}")

        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        job_cards = soup.find_all("div", class_="css-1gatmva e1v1l3u10")
        if not job_cards:
            print("No more jobs found. Stopping.")
            break

        for card in job_cards:
            if max_jobs and scraped_jobs >= max_jobs:
                print(f"Reached max requested jobs: {max_jobs}")
                return build_and_save_jobs_csv(
                    all_titles, all_companies, all_exp_levels, all_exp_years,
                    all_job_types, all_work_modes, all_skills, all_links
                )

            title_tag = card.find("h2", class_="css-m604qf")
            title = title_tag.find("a").text.strip() if title_tag else "N/A"
            link = title_tag.find("a")["href"] if title_tag else "N/A"
            company_tag = card.find("a", class_="css-17s97q8")
            company = company_tag.text.strip() if company_tag else "N/A"
            
            experience_level = "N/A"
            level_tags = card.find("div", class_="css-y4udm8")
            if level_tags:
                inner_divs = level_tags.find_all("div")
                if len(inner_divs) > 1:
                    experience_div = inner_divs[1] 
                    first_a = experience_div.find("a")
                    if first_a:
                        experience_level = first_a.text.strip()

            years_of_experience = "N/A"
            exp_spans = card.find_all("span")
            for span in exp_spans:
                if "Yrs of Exp" in span.text:
                    years_of_experience = span.text.strip("· ").strip()
                    break

            job_type = "N/A"
            work_mode = "N/A"
            type_div = card.find("div", class_="css-1lh32fc")
            if type_div:
                spans = type_div.find_all("span")
                if len(spans) >= 1:
                    job_type = spans[0].text.strip()
                if len(spans) >= 2:
                    work_mode = spans[1].text.strip()

            skills = []
            skill_tags = card.find_all("a", class_="css-5x9pm1")
            for tag in skill_tags:
                tag_text = tag.get_text(strip=True).strip("· ")
                skills.append(tag_text)
            skills_text = ",".join(skills) if skills else "N/A"

            all_titles.append(title)
            all_links.append(link)
            all_companies.append(company)
            all_exp_levels.append(experience_level)
            all_exp_years.append(years_of_experience)
            all_job_types.append(job_type)
            all_work_modes.append(work_mode)
            all_skills.append(skills_text)

            scraped_jobs += 1

        page += 1
        time.sleep(2)

    return build_and_save_jobs_csv(
        all_titles, all_companies, all_exp_levels, all_exp_years,
        all_job_types, all_work_modes, all_skills, all_links
    )

def build_and_save_jobs_csv(
    titles, companies, levels, years, job_types, modes, skills, links,
    output_dir="./output", filename="wuzzuf_jobs.csv"
):
    df = pd.DataFrame({
        "Job_Title": titles,
        "Company_Name": companies,
        "Experience_Level": levels,
        "Years_of_Experience": years,
        "Job_Type": job_types,
        "Work Mode": modes,
        "Skills": skills,
        "Link": links
    })

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df
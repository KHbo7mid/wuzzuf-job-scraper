import requests
from bs4 import BeautifulSoup
import csv
import json
from itertools import zip_longest
from datetime import datetime

def scrape_wuzzuf():
    jobs = []
    page_number = 0

    while True:
        try:
            # Fetch the URL
            url = f"https://wuzzuf.net/search/jobs/?filters%5Broles%5D%5B0%5D=IT%2FSoftware%20Development&filters%5Bworkplace_arrangement%5D%5B0%5D=Remote&start={page_number}"
            result = requests.get(url)
            result.encoding = "utf-8"
            soup = BeautifulSoup(result.content, "lxml")

            # Get total pages
            page_limit = int(soup.find("strong").text)
            if page_number > page_limit // 15:
                print("Scraping completed")
                break

            # Extract job data
            job_titles = soup.find_all("h2", {"class": "css-193uk2c"})
            company_names = soup.find_all("a", {"class": "css-ipsyv7"})
            locations = soup.find_all("span", {"class": "css-16x61xq"})
            job_skills = soup.find_all("div", {"class": "css-1rhj4yg"})
            posted_new = soup.find_all("div", {"class": "css-eg55jf"})
            posted_old = soup.find_all("div", {"class": "css-1jldrig"})
            posted = [*posted_new, *posted_old]

            for i in range(len(job_titles)):
                jobs.append({
                    "Job Title": job_titles[i].get_text(strip=True),
                    "Company Name": company_names[i].get_text(strip=True).replace("-","").strip(),
                    "Date Posted": posted[i].get_text() ,
                    "Location": locations[i].get_text(strip=True),
                    "Skills": job_skills[i].get_text(),
                    "Job Link": job_titles[i].find("a")["href"]
                })

            page_number += 1

        except Exception as e:
            print("Error occurred:", e)
            break

    return jobs


def save_to_csv(jobs, filename="remote_jobs.csv"):
    keys = jobs[0].keys() if jobs else []
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)


def save_to_json(jobs, filename="remote_jobs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    jobs_data = scrape_wuzzuf()

    if jobs_data:
       
        save_to_csv(jobs_data, "remote_jobs_scrape_wuzzuf.csv")
        save_to_json(jobs_data, "remote_jobs_scrape_wuzzuf.json")
        print(f"Saved {len(jobs_data)} jobs to CSV and JSON")
    else:
        print("No jobs found")

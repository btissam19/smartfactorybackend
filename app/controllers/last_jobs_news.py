from datetime import datetime
from typing import  Dict
from serpapi import GoogleSearch


def search_google_jobs(job: str,location: str) -> Dict:
    params = {
     "engine": "google_jobs",
    "q":job,
    "location":location,
    "hl": "en",
    "api_key": 'dfb620d599c6a56f50d33bac58238613c68658266d617a2506226273b1f1385e'
  }
    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_results = results["jobs_results"]
    return   jobs_results

# Function to format the response from Indeed
def format_results(data: Dict) -> Dict:
    formatted_output = {
        "count": len(data.get('jobs', [])),
        "hits": [],
        "indeed_final_url": data.get('indeed_final_url', ''),
        "next_page_id": data.get('next_page_id'),
        "suggest_locality": data.get('suggest_locality')
    }

    for job in data.get('jobs', []):
        formatted_job = {
            "company_name": job.get('company_name', ''),
            "formatted_relative_time": job.get('formatted_relative_time', ''),
            "id": job.get('id', ''),
            "link": job.get('url', ''),
            "locality": job.get('locality', ''),
            "location": job.get('location', ''),
            "pub_date_ts_milli": int(datetime.strptime(job.get('pub_date', ''), "%Y-%m-%d").timestamp() * 1000) if job.get('pub_date') else None,
            "salary": {
                "max": job.get('salary_max', 0),
                "min": job.get('salary_min', 0),
                "type": job.get('salary_type', '')
            },
            "title": job.get('title', '')
        }
        formatted_output['hits'].append(formatted_job)

    return formatted_output

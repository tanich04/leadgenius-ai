# enrich.py

import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_bing_link(company_name):
    try:
        query = company_name + " official site"
        url = f"https://www.bing.com/search?q={query}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        link = soup.find("li", {"class": "b_algo"}).find("a")["href"]
        return link
    except Exception as e:
        print(f"[ERROR] {company_name}: {e}")
        return None

def get_website_text(url, max_chars=1000):
    try:
        res = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:max_chars]
    except:
        return "Could not fetch homepage text."

def enrich_company(company_name):
    site = get_bing_link(company_name)
    if site:
        text = get_website_text(site)
        return site, text
    return None, "Website not found"

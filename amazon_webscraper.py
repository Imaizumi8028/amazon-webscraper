import csv
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_amazon_search_results(query, max_pages=1):
    query_string = quote_plus(query)
    results = []

    for page in range(1, max_pages + 1):
        url = f"https://www.amazon.com/s?k={query_string}&page={page}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div[data-component-type='s-search-result']")

        for item in items:
            title_elem = None
            for anchor in item.find_all("a", href=True):
                href = anchor.get("href", "")
                text = anchor.get_text(" ", strip=True)
                if href.startswith("/") and len(text) >= 8 and not text.startswith(("4.", "5.", "See options", "Energy efficiency")):
                    title_elem = anchor
                    break

            link_elem = title_elem
            price_whole = item.select_one("span.a-price span.a-price-whole")
            price_fraction = item.select_one("span.a-price span.a-price-fraction")
            offscreen_price = item.select_one("span.a-price span.a-offscreen")
            rating_elem = item.select_one("span.a-icon-alt")
            review_elem = item.select_one("span.a-size-base")

            image_elem = item.find("img")
            image_url = (image_elem.get("src") or image_elem.get("data-src")) if image_elem else None

            title = title_elem.get_text(" ", strip=True) if title_elem else None
            link = f"https://www.amazon.com{link_elem['href']}" if link_elem and link_elem.get("href") else None
            price = None
            if offscreen_price:
                price = offscreen_price.get_text(strip=True)
            elif price_whole:
                price = price_whole.get_text(strip=True)
                if price_fraction:
                    price += price_fraction.get_text(strip=True)

            if not price:
                for span in item.select("span.a-price"):
                    candidate = span.get_text(" ", strip=True)
                    if re.search(r"[$€£¥₹]|\b(?:USD|EUR|GBP|CAD|AUD|INR)\b", candidate, re.I) and any(ch.isdigit() for ch in candidate):
                        price = candidate
                        break

            if not price:
                text = item.get_text(" ", strip=True)
                match = re.search(r"(?:[$€£¥₹]|\b(?:USD|EUR|GBP|CAD|AUD|INR)\b)\s*\d[\d,]*(?:\.\d{2})?", text, re.I)
                if match:
                    price = match.group(0).strip()
            rating = rating_elem.get_text(strip=True) if rating_elem else None
            reviews = review_elem.get_text(strip=True) if review_elem else None

            if title and link:
                results.append({
                    "title": title,
                    "link": link,
                    "image": image_url,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                })

    return results


def save_results_to_csv(results, filename="amazon_search_results.csv"):
    if not results:
        return

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link", "image", "price", "rating", "reviews"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in results:
            writer.writerow(item)


def main():
    args = sys.argv[1:]

    if args:
        query = args[0].strip()
        try:
            max_pages = int(args[1]) if len(args) > 1 else 1
        except ValueError:
            max_pages = 1
    else:
        query = input("Enter Amazon search query: ").strip()
        if not query:
            print("No query provided.")
            return

        pages = input("Enter number of pages to scrape (default 1): ").strip()
        try:
            max_pages = int(pages) if pages else 1
        except ValueError:
            max_pages = 1

    if not query:
        print("No query provided.")
        return

    results = fetch_amazon_search_results(query, max_pages=max_pages)
    save_results_to_csv(results)

    print(f"Scraped {len(results)} products from Amazon.")
    print("Saved results to amazon_search_results.csv")


if __name__ == "__main__":
    main()

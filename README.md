# Amazon Product Search Scraper

A Python-based Amazon product scraper that extracts product information from Amazon search results and saves the data into a CSV file.

## Features

* Search Amazon products using any keyword.
* Scrape multiple search result pages.
* Extract:

  * Product Title
  * Product Link
  * Product Image URL
  * Product Price
  * Product Rating
  * Number of Reviews
* Export results to a CSV file.
* Simple command-line interface.

---

## Requirements

* Python 3.8+
* Required Python packages:

```bash
pip install requests beautifulsoup4
```

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/amazon-product-scraper.git
```

2. Navigate to the project directory:

```bash
cd amazon-product-scraper
```

3. Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## Usage

### Interactive Mode

Run:

```bash
python amazon_scraper.py
```

You will be prompted to enter:

* Search query
* Number of pages to scrape

Example:

```text
Enter Amazon search query: gaming mouse
Enter number of pages to scrape (default 1): 2
```

---

### Command Line Mode

You can also provide arguments directly:

```bash
python amazon_scraper.py "gaming mouse" 2
```

Where:

* `"gaming mouse"` is the search keyword.
* `2` is the number of pages to scrape.

---

## Output

After execution, the scraper generates:

```text
amazon_search_results.csv
```

CSV columns:

| Column  | Description       |
| ------- | ----------------- |
| title   | Product title     |
| link    | Product URL       |
| image   | Product image URL |
| price   | Product price     |
| rating  | Product rating    |
| reviews | Number of reviews |

Example:

```csv
title,link,image,price,rating,reviews
Gaming Mouse XYZ,https://amazon.com/...,...,$29.99,4.5 out of 5 stars,1250
```

---

## Project Structure

```text
amazon-product-scraper/
│
├── amazon_scraper.py
├── amazon_search_results.csv
├── README.md
└── requirements.txt
```

---

## Notes

* Amazon frequently changes its website structure. If the scraper stops working, selectors may need to be updated.
* Excessive requests may trigger Amazon's anti-bot protections.
* Some products may not display all fields (price, rating, reviews, etc.).
* This project is intended for educational and learning purposes.

---

## Disclaimer

This project is not affiliated with or endorsed by Amazon. Use responsibly and ensure compliance with Amazon's Terms of Service.

---

## Author

Created by Gopesh Krishna.


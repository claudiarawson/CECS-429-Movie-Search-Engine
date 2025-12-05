from absl.logging import exception
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import time

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

driver.get("https://www.fandango.com/90840_movietimes?date=2025-12-20")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

time.sleep(1)

# Extract date
date_el = driver.find_element("css selector", "a.js-fd-carousel-focus-elem.date-picker__button.fd-carousel--last-selected")
date_href = date_el.get_attribute("href")
date = date_href.split("?date=", 1)[1]   # yyyy-mm-dd

# Container for JSON output
results = []

theater_containers = driver.find_elements("css selector","ul.shared-showtimes__wrapper")

for container in theater_containers:

    # Theater name
    name_el = container.find_element("css selector", "a.shared-theater-header__name-link")
    theater_name = name_el.text.strip()

    # Theater address
    address_el = container.find_element("css selector", "address.shared-theater-header__address")
    theater_address = address_el.text.strip()

    # Build theater entry
    theater_data = {
        "theater_name": theater_name,
        "address": theater_address,
        "movies": []
    }

    # Movies in this theater
    movie_containers = container.find_elements("css selector", "li.shared-movie-showtimes")

    for m_container in movie_containers:

        # Movie title
        movie_title_el = m_container.find_element("css selector", "a.shared-movie-showtimes__movie-title-link")
        movie_title = movie_title_el.text.strip()

        # Showtimes
        showtime_els = m_container.find_elements("css selector", "ol.showtimes-btn-list a")
        showtimes = [s.text.strip() for s in showtime_els if s.text.strip()]

        # Convert showtimes to ISO datetime format
        formatted_times = []
        for t in showtimes:
            t = t.lower().strip()

            # Remove spaces like "3:15 p"
            t = t.replace(" ", "")

            # Determine AM/PM
            is_pm = t.endswith("p")
            is_am = t.endswith("a")
            t = t[:-1]  # remove trailing 'a' or 'p'

            # Handle times missing minutes (e.g. "9p")
            if ":" in t:
                hour_str, minute_str = t.split(":")
            else:
                hour_str, minute_str = t, "00"

            hour = int(hour_str)
            minute = int(minute_str)

            # Convert to 24-hour
            if is_pm and hour != 12:
                hour += 12
            if is_am and hour == 12:
                hour = 0

            hhmm = f"{hour:02d}:{minute:02d}"
            iso_dt = f"{date}T{hhmm}"
            formatted_times.append(iso_dt)

        # Add to theater
        theater_data["movies"].append({
            "title": movie_title,
            "showtimes": formatted_times
        })

    results.append(theater_data)
file_name = f"{date}-fandango.json"
# Save to JSON file
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

driver.quit()
print(f"Scraping complete. {file_name} created")

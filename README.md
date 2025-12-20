# Movie Showtime Finder

A Python-based movie showtime aggregation and search system that scrapes Fandango showtimes, stores them as structured JSON, and provides both a web API (Flask) and an interactive CLI chatbot for searching movies and theaters using fuzzy matching.

## Features

### Automated Web Scraping

Scrapes movie showtimes from Fandango for a given ZIP code and multiple dates

Outputs clean, structured JSON files (YYYY-MM-DD-fandango.json)

### Smart Search Engine

Fuzzy search for movies and theaters using RapidFuzz

Filter results by date and time range

Browse all movies or theaters

### Flask Web API

REST endpoints for searching and browsing

Automatically loads the most recent scraped dataset

### CLI Chatbot

Interactive terminal interface

Guided search, filtering, and browsing

## Project Structure
```python
.
├── __pypache__/
├── fandango/
│   ├── 2025-12-14-fandango.json
│   ├── 2025-12-15-fandango.json
│   └── 2025-12-16-fandango.json
├── templates/
│   └── index.html
├── app.py                     # Flask API server
├── chatbot_backend.py         # CLI chatbot interface
├── query_engine.py            # Core search & filtering logic
├── webscraper by theater.py   # Selenium + BeautifulSoup scraper
├── requirements.txt           # Python dependencies
└── README.md
```

## Installation
1. Clone the Repository
git clone https://github.com/your-username/movie-showtime-finder.git
cd movie-showtime-finder

2. Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Install Firefox + Geckodriver

The scraper uses Selenium with Firefox.

```Install Firefox```

```Install geckodriver``` and ensure it’s on your PATH

## Running the Scraper

The scraper pulls showtimes for a specific ZIP code and date range.

```bash
python "webscraper by theater.py"
```


This will generate files like:

```
2025-12-14-fandango.json
2025-12-15-fandango.json
2025-12-16-fandango.json
```

Each file contains:

* Theater name & address

* Movies playing

* Showtime datetimes in ISO format ```(YYYY-MM-DDTHH:MM)```

### Running the Flask API
```bash
python app.py
```


The server will:

* Automatically load the most recent ```*-fandango.json``` file

* Start at ```http://127.0.0.1:5000```

### Available Endpoints
**Search**
```sql
GET /api/search
```

Query parameters:

```mode``` — ```movie``` or ```theater```

```q``` — search string (required)

```date``` — ```YYYY-MM-DD``` (optional)

```start``` — ```HH:MM``` (optional)

```end``` — ```HH:MM``` (optional)

Example:

```sql
/api/search?mode=movie&q=zootopia&date=2025-12-15&start=18:00&end=22:00
```

### Browse Movies
```bash
GET /api/movies
```

Browse Theaters
```bash
GET /api/theaters
```

Running the CLI Chatbot
```bash
python chatbot_backend.py
```

* Chatbot Capabilities

* Search for a movie

* Search for a theater

* Browse all movies

* Browse all theaters

* Filter by date or time range

* Friendly formatted output

### Core Components
```query_engine.py```

* Loads JSON showtime data

* Builds movie & theater indexes

* Performs fuzzy matching using RapidFuzz

* Handles date and time filtering

```chatbot_backend.py```

Terminal-based interactive interface

Uses the same query engine as the API

```app.py```

* Flask REST API

* Auto-detects latest scraped dataset

## Dependencies

Key libraries used:

* ```selenium```

* ```beautifulsoup4```

* ```RapidFuzz```

* ```flask```

* ```trio / websocket stack```

See ```requirements.txt ```for the full list.

## Future Improvements

* Frontend UI for the Flask API

* Configurable ZIP codes and date ranges

* Docker support

* Caching & scheduled scraping

* Support for additional theater providers

## License

This project is for **educational and personal use.**
Be mindful of Fandango’s terms of service when scraping data.

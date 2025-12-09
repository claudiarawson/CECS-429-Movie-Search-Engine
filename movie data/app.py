from flask import Flask, render_template, request, jsonify
from query_engine import MovieQueryEngine
from datetime import datetime

app = Flask(__name__)

# TODO: change this to the actual JSON file you generated
DATA_PATH = "fandango/2025-12-05-fandango.json"
engine = MovieQueryEngine(DATA_PATH)


def apply_filters(results, date_str, start_time, end_time):
    # date_str: "YYYY-MM-DD" or ""
    if date_str:
        results = engine.filter_by_date(results, date_str)
    if start_time and end_time:
        results = engine.filter_by_time_range(results, start_time, end_time)
    return results


@app.route("/")
def index():
    # just serve the HTML page
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    """
    Query params:
      mode: 'movie' | 'theater'
      q: search query string
      date: YYYY-MM-DD (optional)
      start: HH:MM (24h, optional)
      end: HH:MM (24h, optional)
    """
    mode = request.args.get("mode", "movie")
    q = (request.args.get("q") or "").strip()
    date_str = (request.args.get("date") or "").strip()
    start_time = (request.args.get("start") or "").strip()
    end_time = (request.args.get("end") or "").strip()

    if not q:
        return jsonify({"error": "Missing query"}), 400

    if mode == "theater":
        results = engine.search_theater(q)
    else:
        results = engine.search_movie(q)

    results = apply_filters(results, date_str, start_time, end_time)
    return jsonify(results)


@app.route("/api/movies")
def api_movies():
    """Return all movies (for browsing)."""
    movies = engine.get_all_movies()
    return jsonify(movies)


@app.route("/api/theaters")
def api_theaters():
    """Return all theaters (for browsing)."""
    theaters = engine.get_all_theaters()
    return jsonify(theaters)


if __name__ == "__main__":
    app.run(debug=True)

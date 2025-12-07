import json
from datetime import datetime
from typing import List, Dict, Any
from rapidfuzz import fuzz, process


class MovieQueryEngine:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = self._load_data()
        self.movie_index = self._build_movie_index()
        self.theater_index = self._build_theater_index()
    
    def _load_data(self) -> List[Dict]:
        with open(self.data_path, 'r') as f:
            return json.load(f)
    
    def _build_movie_index(self) -> Dict[str, List[Dict]]:
        """Map movie titles to theaters showing them"""
        index = {}
        for theater in self.data:
            for movie in theater['movies']:
                title = movie['title'].lower()
                if title not in index:
                    index[title] = []
                index[title].append({
                    'theater_name': theater['theater_name'],
                    'address': theater['address'],
                    'showtimes': movie['showtimes']
                })
        return index
    
    def _build_theater_index(self) -> Dict[str, Dict]:
        """Map theater names to their full data"""
        index = {}
        for theater in self.data:
            name = theater['theater_name'].lower()
            index[name] = theater
        return index
    
    def search_movie(self, query: str, threshold: int = 70) -> List[Dict]:
        """Search for movies using fuzzy matching"""
        query = query.lower().strip()
        
        # Get all movie titles
        all_titles = list(self.movie_index.keys())
        
        # Fuzzy match
        matches = process.extract(query, all_titles, scorer=fuzz.WRatio, limit=5)
        
        results = []
        for match, score, _ in matches:
            if score >= threshold:
                results.append({
                    'title': match,
                    'score': score,
                    'theaters': self.movie_index[match]
                })
        
        return results
    
    def search_theater(self, query: str, threshold: int = 70) -> List[Dict]:
        """Search for theaters using fuzzy matching"""
        query = query.lower().strip()
        
        all_theaters = list(self.theater_index.keys())
        matches = process.extract(query, all_theaters, scorer=fuzz.WRatio, limit=5)
        
        results = []
        for match, score, _ in matches:
            if score >= threshold:
                theater = self.theater_index[match]
                results.append({
                    'name': theater['theater_name'],
                    'address': theater['address'],
                    'score': score,
                    'movies': [m for m in theater['movies'] if m['showtimes']]
                })
        
        return results
    
    def get_all_movies(self) -> List[str]:
        """Get list of all unique movies"""
        return sorted(set(movie['title'] for theater in self.data 
                         for movie in theater['movies'] if movie['showtimes']))
    
    def get_all_theaters(self) -> List[Dict]:
        """Get list of all theaters"""
        return [{'name': t['theater_name'], 'address': t['address']} 
                for t in self.data]
    
    def filter_by_date(self, results: List[Dict], date_str: str) -> List[Dict]:
        """Filter showtimes by specific date (YYYY-MM-DD)"""
        filtered = []
        for result in results:
            if 'theaters' in result:  # Movie search result
                filtered_theaters = []
                for theater in result['theaters']:
                    filtered_times = [t for t in theater['showtimes'] 
                                    if t.startswith(date_str)]
                    if filtered_times:
                        filtered_theaters.append({
                            **theater,
                            'showtimes': filtered_times
                        })
                if filtered_theaters:
                    filtered.append({
                        **result,
                        'theaters': filtered_theaters
                    })
            elif 'movies' in result:  # Theater search result
                filtered_movies = []
                for movie in result['movies']:
                    filtered_times = [t for t in movie['showtimes'] 
                                    if t.startswith(date_str)]
                    if filtered_times:
                        filtered_movies.append({
                            **movie,
                            'showtimes': filtered_times
                        })
                if filtered_movies:
                    filtered.append({
                        **result,
                        'movies': filtered_movies
                    })
        return filtered
    
    def filter_by_time_range(self, results: List[Dict], start_time: str, end_time: str) -> List[Dict]:
        """Filter by time range (HH:MM format)"""
        filtered = []
        for result in results:
            if 'theaters' in result:
                filtered_theaters = []
                for theater in result['theaters']:
                    filtered_times = []
                    for showtime in theater['showtimes']:
                        time_part = showtime.split('T')[1] if 'T' in showtime else showtime
                        if start_time <= time_part <= end_time:
                            filtered_times.append(showtime)
                    if filtered_times:
                        filtered_theaters.append({
                            **theater,
                            'showtimes': filtered_times
                        })
                if filtered_theaters:
                    filtered.append({
                        **result,
                        'theaters': filtered_theaters
                    })
            elif 'movies' in result:
                filtered_movies = []
                for movie in result['movies']:
                    filtered_times = []
                    for showtime in movie['showtimes']:
                        time_part = showtime.split('T')[1] if 'T' in showtime else showtime
                        if start_time <= time_part <= end_time:
                            filtered_times.append(showtime)
                    if filtered_times:
                        filtered_movies.append({
                            **movie,
                            'showtimes': filtered_times
                        })
                if filtered_movies:
                    filtered.append({
                        **result,
                        'movies': filtered_movies
                    })
        return filtered
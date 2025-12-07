from query_engine import MovieQueryEngine
from datetime import datetime, timedelta


class MovieChatbot:
    def __init__(self, data_path: str):
        self.engine = MovieQueryEngine(data_path)
        self.running = True
    
    def display_menu(self):
        print("\n" + "="*50)
        print("MOVIE SHOWTIME FINDER")
        print("="*50)
        print("1. Search for a movie")
        print("2. Search for a theater")
        print("3. Browse all movies")
        print("4. Browse all theaters")
        print("5. Exit")
        print("="*50)
    
    def format_showtime(self, showtime: str) -> str:
        """Convert ISO format to readable time"""
        try:
            dt = datetime.fromisoformat(showtime)
            return dt.strftime("%I:%M %p")
        except:
            return showtime
    
    def display_movie_results(self, results):
        if not results:
            print("\nNo results found.")
            return
        
        print(f"\nFound {len(results)} result(s):")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title'].title()} (Match: {result['score']}%)")
            print(f"   Showing at {len(result['theaters'])} theater(s):")
            for theater in result['theaters']:
                print(f"\n   📍 {theater['theater_name']}")
                print(f"      {theater['address']}")
                print(f"      Showtimes: {', '.join([self.format_showtime(t) for t in theater['showtimes'][:10]])}")
                if len(theater['showtimes']) > 10:
                    print(f"      ... and {len(theater['showtimes']) - 10} more")
    
    def display_theater_results(self, results):
        if not results:
            print("\nNo results found.")
            return
        
        print(f"\nFound {len(results)} theater(s):")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']} (Match: {result['score']}%)")
            print(f"   📍 {result['address']}")
            print(f"   Showing {len(result['movies'])} movie(s):")
            for movie in result['movies'][:5]:
                print(f"   • {movie['title']}")
                print(f"     Times: {', '.join([self.format_showtime(t) for t in movie['showtimes'][:5]])}")
            if len(result['movies']) > 5:
                print(f"   ... and {len(result['movies']) - 5} more movies")
    
    def search_movie(self):
        movie_name = input("\nEnter movie name: ").strip()
        if not movie_name:
            print("Invalid input.")
            return
        
        results = self.engine.search_movie(movie_name)
        
        # Optional filtering
        if results:
            filter_choice = input("\nFilter results? (1=By date, 2=By time, 3=Display all): ").strip()
            
            if filter_choice == "1":
                date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                if not date_str:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                results = self.engine.filter_by_date(results, date_str)
            
            elif filter_choice == "2":
                start = input("Start time (HH:MM, e.g., 18:00): ").strip()
                end = input("End time (HH:MM, e.g., 22:00): ").strip()
                if start and end:
                    results = self.engine.filter_by_time_range(results, start, end)
        
        self.display_movie_results(results)
    
    def search_theater(self):
        theater_name = input("\nEnter theater name: ").strip()
        if not theater_name:
            print("Invalid input.")
            return
        
        results = self.engine.search_theater(theater_name)
        self.display_theater_results(results)
    
    def browse_movies(self):
        movies = self.engine.get_all_movies()
        print(f"\n{len(movies)} movies available:")
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie}")
        
        choice = input("\nEnter number to see details (or press Enter to skip): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(movies):
            movie_name = movies[int(choice) - 1]
            results = self.engine.search_movie(movie_name)
            self.display_movie_results(results)
    
    def browse_theaters(self):
        theaters = self.engine.get_all_theaters()
        print(f"\n{len(theaters)} theater(s) available:")
        for i, theater in enumerate(theaters, 1):
            print(f"{i}. {theater['name']}")
            print(f"   📍 {theater['address']}")
        
        choice = input("\nEnter number to see details (or press Enter to skip): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(theaters):
            theater_name = theaters[int(choice) - 1]['name']
            results = self.engine.search_theater(theater_name)
            self.display_theater_results(results)
    
    def run(self):
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                self.search_movie()
            elif choice == "2":
                self.search_theater()
            elif choice == "3":
                self.browse_movies()
            elif choice == "4":
                self.browse_theaters()
            elif choice == "5":
                print("\nGoodbye!")
                self.running = False
            else:
                print("\nInvalid choice. Please enter 1-5.")


if __name__ == "__main__":
    # Update this path to your JSON file
    chatbot = MovieChatbot("fandango/2025-12-05-fandango.json")
    chatbot.run()
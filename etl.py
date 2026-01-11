from datetime import datetime
import os
import pandas as pd
import requests

#Retrieves credentials from environment variables to avoid hardcoding secrets
API_KEY = os.environ.get('TMDB_API_KEY')

def extract_transform_load():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    rows = []
    curr_date = datetime.now().strftime('%Y-%m-%d')

    #Flattens JSON response into a consistent schema for tabular storage
    for rank, item in enumerate(data['results'], start = 1):
        row = {'date': curr_date,
               'rank': rank,
               'title': item['title'],
               'popularity': item['popularity'],
               'vote_average': item['vote_average'],
               'release_date': item.get('release_date', 'N/A')}
        rows.append(row)

    df = pd.DataFrame(rows)
    fname = 'daily_movie_trends.csv'
    #Append mode 'a' enables incremental loading
    df.to_csv(fname, mode = 'a', header = not os.path.exists(fname), index = False)

    #Generates a static view for quick consumption
    top_5 = df.head(5)[['rank', 'title', 'vote_average']]
    
    with open('LATEST_UPDATE.md', 'w') as f:
        f.write(f"# Daily Movie Trends: {curr_date}\n\n")
        f.write(top_5.to_markdown(index = False))
    
if __name__ == "__main__":
    if not API_KEY:
        raise ValueError("Missing TMDB API Key.")
    
    extract_transform_load()

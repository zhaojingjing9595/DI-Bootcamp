import pandas as pd
import numpy as np
import zipfile
import urllib.request
import os
import random
import json
from faker import Faker

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MOVIELENS_DIR = os.path.join(DATA_DIR, "ml-latest-small")

ALL_GENRES = ["Action", "Comedy", "Drama", "Thriller", "Sci-Fi",
              "Romance", "Horror", "Animation", "Crime", "Adventure"]

AGE_GENRE_BIAS = {
    "young":  ["Action", "Sci-Fi", "Horror", "Animation", "Adventure"],
    "middle": ["Thriller", "Crime", "Drama", "Comedy"],
    "older":  ["Drama", "Romance", "Comedy"],
}

NUM_USERS = 20


def load_movielens():
    """Download (if needed) and load MovieLens small dataset. Returns (movies, ratings, tags)."""
    url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    zip_path = os.path.join(DATA_DIR, "ml-latest-small.zip")

    if not os.path.exists(MOVIELENS_DIR):
        print("Downloading MovieLens small dataset...")
        os.makedirs(DATA_DIR, exist_ok=True)
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(DATA_DIR)
        os.remove(zip_path)
        print("Done.")
    else:
        print("Dataset already exists, skipping download.")

    movies = pd.read_csv(f"{MOVIELENS_DIR}/movies.csv")
    ratings = pd.read_csv(f"{MOVIELENS_DIR}/ratings.csv")
    tags = pd.read_csv(f"{MOVIELENS_DIR}/tags.csv")

    print(f"Movies:  {movies.shape[0]:,} rows")
    print(f"Ratings: {ratings.shape[0]:,} rows")
    print(f"Tags:    {tags.shape[0]:,} rows")

    return movies, ratings, tags


def _build_genre_index(movies):
    genre_to_movies = {}
    for _, row in movies.iterrows():
        for g in row["genres"].split("|"):
            genre_to_movies.setdefault(g, []).append((row["movieId"], row["title"]))
    return genre_to_movies


def _simulate_rating(genre, preferred_genres):
    base = 4.0 if genre in preferred_genres else 2.8
    noise = np.random.normal(0, 0.7)
    rating = round((base + noise) * 2) / 2
    return float(np.clip(rating, 0.5, 5.0))


def _build_watch_history(preferred_genres, n_watched, genre_to_movies):
    history = []
    for _ in range(n_watched):
        genre = (random.choice(preferred_genres) if random.random() < 0.80
                 else random.choice(ALL_GENRES))
        candidates = genre_to_movies.get(genre, [])
        if not candidates:
            continue
        movie_id, title = random.choice(candidates)
        history.append({
            "movie_id": int(movie_id),
            "title": title,
            "genre_watched": genre,
            "rating": _simulate_rating(genre, preferred_genres),
        })
    # Deduplicate by movie_id
    seen, unique = set(), []
    for item in history:
        if item["movie_id"] not in seen:
            seen.add(item["movie_id"])
            unique.append(item)
    return unique


def simulate_user_profiles(movies, seed=42):
    """Generate synthetic user profiles with realistic noise."""
    np.random.seed(seed)
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)

    genre_to_movies = _build_genre_index(movies)
    user_profiles = []
    names = [fake.first_name() for _ in range(NUM_USERS)]

    for i, name in enumerate(names):
        age = fake.random_int(18, 65)
        age_group = "young" if age < 30 else ("middle" if age < 50 else "older")

        biased_pool = AGE_GENRE_BIAS[age_group] + random.sample(ALL_GENRES, 2)
        n_prefs = random.randint(1, 3)
        preferred_genres = random.sample(biased_pool, min(n_prefs, len(biased_pool)))

        roll = random.random()
        if roll < 0.10:
            n_watched = 0
        elif roll < 0.35:
            n_watched = random.randint(30, 60)
        else:
            n_watched = random.randint(5, 15)

        history = _build_watch_history(preferred_genres, n_watched, genre_to_movies)

        user_profiles.append({
            "user_id": i + 1,
            "name": name,
            "age": age,
            "preferred_genres": preferred_genres,
            "watch_history": history,
        })

    return user_profiles


def save_user_profiles(user_profiles):
    """Save profiles to JSON and a flat ratings CSV under data/."""
    json_path = os.path.join(DATA_DIR, "user_profiles.json")
    csv_path = os.path.join(DATA_DIR, "user_ratings.csv")

    with open(json_path, "w") as f:
        json.dump(user_profiles, f, indent=2)

    rows = []
    for u in user_profiles:
        for m in u["watch_history"]:
            rows.append({
                "user_id": u["user_id"],
                "name": u["name"],
                "age": u["age"],
                "movie_id": m["movie_id"],
                "title": m["title"],
                "genre_watched": m["genre_watched"],
                "rating": m["rating"],
            })

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    print(f"Saved {json_path}  ({len(user_profiles)} users)")
    print(f"Saved {csv_path}    ({len(df)} rating rows)")
    return df


def load_user_profiles():
    """Load previously saved user profiles from data/user_profiles.json."""
    json_path = os.path.join(DATA_DIR, "user_profiles.json")
    with open(json_path) as f:
        return json.load(f)

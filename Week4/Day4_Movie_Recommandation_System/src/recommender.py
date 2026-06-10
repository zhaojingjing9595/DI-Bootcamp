import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from scipy.cluster.vq import kmeans, vq, whiten


def get_top_genres(user_ratings_df, user_id, preferred_genres, min_rating=3.5, top_n=3):
    """
    Step 1: From the flat user_ratings CSV, filter this user's highly-rated rows,
    compute a weighted score per genre (avg_rating * log1p(count)), and return top_n.
    Falls back to stated preferred_genres for cold-start users.
    """
    user_rows = user_ratings_df[user_ratings_df["user_id"] == user_id]

    if user_rows.empty:
        return preferred_genres[:top_n]

    liked = user_rows[user_rows["rating"] >= min_rating]

    if liked.empty:
        return preferred_genres[:top_n]

    genre_stats = (
        liked.groupby("genre_watched")["rating"]
        .agg(avg_rating="mean", count="count")
        .reset_index()
    )
    genre_stats["score"] = genre_stats["avg_rating"] * np.log1p(genre_stats["count"])
    return (
        genre_stats.sort_values("score", ascending=False)
        .head(top_n)["genre_watched"]
        .tolist()
    )


def get_avg_ratings(ratings_df):
    """
    Compute average MovieLens rating and rating count per movie.
    Returns a DataFrame with columns: movieId, avg_rating, rating_count.
    """
    return (
        ratings_df
        .groupby("movieId")["rating"]
        .agg(avg_rating="mean", rating_count="count")
        .reset_index()
    )


def content_based_recommend(user_profile, user_ratings_df, movies_df, ratings_df, top_n=10):
    """
    Content-based recommender using only pandas operations.

    Logic:
    1. Query user_ratings_df for this user's highly-rated genres (get_top_genres)
    2. Filter movies_df to movies that match those genres
    3. Score each movie by how many top genres it matches
    4. Merge with avg MovieLens ratings as a quality tiebreaker
    5. Drop already-watched movies
    6. Return top N sorted by score
    """

    # Step 1 — what genres does this user like?
    top_genres = get_top_genres(
        user_ratings_df,
        user_id=user_profile["user_id"],
        preferred_genres=user_profile["preferred_genres"],
    )

    # Step 2 — count how many of the user's top genres each movie contains
    movies = movies_df.copy()
    movies["genre_match_count"] = movies["genres"].apply(
        lambda g: sum(1 for genre in top_genres if genre in g.split("|"))
    )
    candidates = movies[movies["genre_match_count"] > 0].copy()

    # Step 3 — merge with average MovieLens ratings as a quality tiebreaker
    avg_ratings = get_avg_ratings(ratings_df)
    candidates = candidates.merge(avg_ratings, on="movieId", how="left")
    candidates["avg_rating"] = candidates["avg_rating"].fillna(3.0)
    candidates["rating_count"] = candidates["rating_count"].fillna(0)

    # Step 4 — combined score: normalize both signals to 0-1 then apply explicit weights
    GENRE_WEIGHT = 0.7
    RATING_WEIGHT = 0.3

    candidates["genre_score"] = candidates["genre_match_count"] / candidates["genre_match_count"].max()
    candidates["rating_score"] = candidates["avg_rating"] / candidates["avg_rating"].max()
    candidates["score"] = (
        GENRE_WEIGHT * candidates["genre_score"] +
        RATING_WEIGHT * candidates["rating_score"]
    )

    # Step 5 — remove movies the user has already watched
    watched_ids = set(user_ratings_df[user_ratings_df["user_id"] == user_profile["user_id"]]["movie_id"])
    candidates = candidates[~candidates["movieId"].isin(watched_ids)]

    # Step 6 — sort and return top N
    result = (
        candidates
        .sort_values("score", ascending=False)
        .head(top_n)
        [["movieId", "title", "genres", "genre_match_count", "avg_rating", "genre_score", "rating_score", "score"]]
        .reset_index(drop=True)
    )

    return top_genres, result


# ── Collaborative Filtering: Pearson Correlation ─────────────────────────────

def build_user_movie_matrix(ratings_df):
    """
    Pivot ratings.csv into a matrix: rows = userId, columns = movieId, values = rating.
    Missing values (user hasn't rated that movie) stay as NaN.
    """
    return ratings_df.pivot_table(index="userId", columns="movieId", values="rating")


def pearson_recommend(user_profile, user_ratings_df, ratings_df, movies_df, top_n=10, min_overlap=5):
    """
    Collaborative filtering using Pearson correlation.

    Logic:
    1. Build a user-movie rating matrix from real MovieLens users
    2. Represent the simulated user as a ratings row (movie_id → rating)
    3. For each real user, find overlapping movies with the simulated user
       and compute Pearson correlation on those overlapping ratings
    4. Take the top similar real users
    5. Collect movies those users rated highly → remove already-watched → return top N
    """

    # Step 1 — build the real user-movie matrix
    matrix = build_user_movie_matrix(ratings_df)

    # Step 2 — represent simulated user's ratings as a dict {movie_id: rating}
    user_rows = user_ratings_df[user_ratings_df["user_id"] == user_profile["user_id"]]
    sim_user_ratings = dict(zip(user_rows["movie_id"], user_rows["rating"]))

    if not sim_user_ratings:
        return [], pd.DataFrame()  # cold-start: can't run correlation

    # Step 3 — compute Pearson correlation with each real user
    correlations = []

    for real_user_id, real_user_row in matrix.iterrows():
        # Find movies both the simulated user and this real user have rated
        overlap_movies = [mid for mid in sim_user_ratings if mid in real_user_row.index]
        real_ratings = real_user_row[overlap_movies].dropna()
        overlap_movies = list(real_ratings.index)  # only movies real user actually rated

        if len(overlap_movies) < min_overlap:
            continue  # not enough shared movies to trust the correlation

        sim_ratings_overlap = [sim_user_ratings[mid] for mid in overlap_movies]
        real_ratings_overlap = real_ratings.tolist()

        corr, _ = pearsonr(sim_ratings_overlap, real_ratings_overlap)

        if not np.isnan(corr):
            correlations.append({"userId": real_user_id, "correlation": corr})

    if not correlations:
        return [], pd.DataFrame()

    corr_df = pd.DataFrame(correlations).sort_values("correlation", ascending=False)
    top_similar_users = corr_df.head(10)["userId"].tolist()

    # Step 4 — collect highly-rated movies from those similar users
    watched_ids = set(user_rows["movie_id"])

    similar_ratings = (
        ratings_df[
            (ratings_df["userId"].isin(top_similar_users)) &
            (~ratings_df["movieId"].isin(watched_ids)) &
            (ratings_df["rating"] >= 4.0)
        ]
        .groupby("movieId")["rating"]
        .agg(avg_rating="mean", voted_by="count")
        .reset_index()
        .sort_values(["voted_by", "avg_rating"], ascending=False)
    )

    # Step 5 — merge with movie titles and return top N
    result = (
        similar_ratings
        .merge(movies_df[["movieId", "title", "genres"]], on="movieId")
        .head(top_n)
        .reset_index(drop=True)
    )

    return top_similar_users, result


# ── Collaborative Filtering: K-Means Clustering ───────────────────────────────

ALL_GENRES = ["Action", "Comedy", "Drama", "Thriller", "Sci-Fi",
              "Romance", "Horror", "Animation", "Crime", "Adventure"]


def build_genre_vectors(ratings_df, movies_df, genre_list=ALL_GENRES):
    """
    For each real user, build a genre preference vector:
    each element = average rating they gave to movies of that genre.
    Returns a DataFrame: rows = userId, columns = genres.
    """
    # Explode movies into one row per genre
    movies_exploded = movies_df.copy()
    movies_exploded["genre"] = movies_exploded["genres"].str.split("|")
    movies_exploded = movies_exploded.explode("genre")
    movies_exploded = movies_exploded[movies_exploded["genre"].isin(genre_list)]

    # Join with ratings to get (userId, genre, rating)
    merged = ratings_df.merge(movies_exploded[["movieId", "genre"]], on="movieId")

    # Average rating per user per genre
    genre_matrix = (
        merged.groupby(["userId", "genre"])["rating"]
        .mean()
        .unstack(fill_value=0)          # missing genre → 0 (user hasn't watched it)
    )

    # Make sure all genres are present as columns even if no user rated them
    for g in genre_list:
        if g not in genre_matrix.columns:
            genre_matrix[g] = 0.0

    return genre_matrix[genre_list]     # consistent column order


def kmeans_recommend(user_profile, user_ratings_df, ratings_df, movies_df,
                     k=5, top_n=10, genre_list=ALL_GENRES):
    """
    K-Means clustering recommendation.

    Logic:
    1. Build a genre preference vector for every real MovieLens user
    2. Whiten (normalize) the vectors so no genre dominates just by scale
    3. Run k-means to group users into k clusters
    4. Build the simulated user's genre vector and assign them to the nearest cluster
    5. Find the top-rated movies among real users in that cluster → return top N
    """

    # Step 1 — genre vectors for all real users
    genre_matrix = build_genre_vectors(ratings_df, movies_df, genre_list)
    user_ids = genre_matrix.index.tolist()
    vectors = genre_matrix.values.astype(float)

    # Step 2 — whiten: scale each genre column to unit variance
    # (so a genre with naturally high ratings doesn't dominate clustering)
    whitened = whiten(vectors)

    # Step 3 — run k-means: find k cluster centroids
    centroids, _ = kmeans(whitened, k)

    # Step 4 — build the simulated user's genre vector
    user_rows = user_ratings_df[user_ratings_df["user_id"] == user_profile["user_id"]]

    if user_rows.empty:
        # Cold-start: give equal weight to stated preferred genres
        sim_vector = np.array([
            3.5 if g in user_profile["preferred_genres"] else 0.0
            for g in genre_list
        ])
    else:
        sim_vector = np.array([
            user_rows[user_rows["genre_watched"] == g]["rating"].mean()
            if g in user_rows["genre_watched"].values else 0.0
            for g in genre_list
        ])

    # Whiten the simulated user's vector using the same scale factors
    scale = vectors.std(axis=0)
    scale[scale == 0] = 1               # avoid division by zero
    sim_whitened = sim_vector / scale

    # Assign simulated user to the nearest cluster
    cluster_labels, _ = vq(whitened, centroids)
    sim_label, _ = vq(sim_whitened.reshape(1, -1), centroids)
    assigned_cluster = sim_label[0]

    # Step 5 — find real users in the same cluster
    users_in_cluster = [user_ids[i] for i, label in enumerate(cluster_labels)
                        if label == assigned_cluster]

    watched_ids = set(user_rows["movie_id"]) if not user_rows.empty else set()

    cluster_top = (
        ratings_df[
            (ratings_df["userId"].isin(users_in_cluster)) &
            (~ratings_df["movieId"].isin(watched_ids))
        ]
        .groupby("movieId")["rating"]
        .agg(avg_rating="mean", voted_by="count")
        .reset_index()
        .sort_values(["voted_by", "avg_rating"], ascending=False)
        .merge(movies_df[["movieId", "title", "genres"]], on="movieId")
        .head(top_n)
        .reset_index(drop=True)
    )

    return assigned_cluster, len(users_in_cluster), cluster_top

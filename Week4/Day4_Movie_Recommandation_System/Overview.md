This project is to create a python-based movie recommendation system based on user preferences and viewing history to mimic personalized GEN AI application in the media and entertainment industry.

# Core Components to Consider
## 1. Data Layer
    - Movie dataset: use public datasets, MovieLens ml-latest-small (100K ratings, easy to start).

    - User profiles: name, age, preferences, watch_history
        Example:
        {
            "name": "John",
            "age": 25,
            "preferences": ["action", "thriller"],
            "watch_history": [{"movie_id": "seer100102", "movie": "Inception", "genre": "sci-fi", "rating": 5}]
        }
        Cold start: new users with no history are asked for 3–5 favorite movies or genres on first run.

    - Storage: csv file (simple; no database needed for this scope)

## 2. Recommendation Approaches (pick one or combine)
    - Collaborative filtering:
        user-based: "Users like you also liked..." — cosine similarity on user rating vectors
        item-based: "Because you liked ..., you might also like..." — cosine similarity on item rating vectors

    - Content-based filtering: Match movies by genre, director, cast, description embeddings

    - Hybrid (collaborative + content-based):
        Weight both signals and merge results — most production systems (Netflix, Spotify) do this; reduces weaknesses of each approach alone

    - Popularity / Trending-Based:
        "What's hot right now" — fallback when user history is thin. Filter by genre so it's not completely generic ("Top 10 sci-fi of the decade").

## 3. GenAI Integration Points (Phase 2)
    - Natural language input: User describes mood/preference → LLM extracts structured filters
    - Explanation generation: "We recommend this because you liked X and enjoy Y genre"
    - Conversational interface: Chat-style interaction instead of just a form
    - Free-text preference queries: "I want something like Inception but more emotional"

## 4. Build Order (suggested)
    Phase 1:
    1. Load and explore MovieLens data
    2. Build a basic content-based recommender (genre + description similarity)
    3. Add collaborative filtering using ratings
    4. Simple Jupyter notebook interface to demo it (no web server needed for prototyping)

    Phase 2:
    5. Wrap with Claude API for NL query parsing and recommendation explanations
    6. Add conversational interface via Claude

## 5. Key Libraries
    pandas, numpy — data wrangling
    scikit-learn — TF-IDF, cosine similarity
    anthropic — Claude API for GenAI layer (Phase 2)
    sentence-transformers (Phase 2) — semantic embeddings for movie descriptions

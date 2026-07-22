# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems like Spority or YoutTube typically combine two approaches: collaborative filtering, which predicts what a user will like based on patterns across other users' behavior, and content-based filtering, which predicts what a user will like based on the attributes of the tiems themselves. Collaborative filtering can surgace surpsing recommendations but strggles with brand-new items that have no interaction history yet. Content-based filtering solves that "cold start" roblem and produces explainable recommendations, but can't easily suggest things outside a user's establichsed attribute preferences. This simulation priotizes content-based approach only, it has no concept of other users, and works purley by matching song attributes against an explicit user preference profile.

Some prompts to answer:

- What features does each `Song` use in your system
  - genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- What information does your `UserProfile` store
  - preferred target values for energy, tempo_bpm, valence, danceability, and acousticness, plus a preferred genre and preferred mood
- How does your `Recommender` compute a score for each song
  - For each numeric feature, use: `score = 1 - |song_value - user_preferred_value|`
  - This rewards songs *closer* to the user's preference, not just higher or lower values
  - Categorical features (genre, mood) score 1 for a match, 0 otherwise
  - Combine all feature scores into one weighted total:
    - `song_score = (w_energy × energy_score) + (w_valence × valence_score) + (w_tempo × tempo_score) + (w_danceability × danceability_score) + (w_acousticness × acousticness_score) + (w_genre × genre_match) + (w_mood × mood_match)`
  - Weights sum to 1
  - Genre is weighted higher than mood (0.15 vs 0.05), since genre is a harder, more stable preference, while mood overlaps with what energy/valence/acousticness already capture

- How do you choose which songs to recommend
  - Score every song in `songs.csv` against the `UserProfile`
  - Sort songs by `song_score`, descending
  - Filter out songs already in the user's recent listening history
  - Return the top N as the recommendation list
  - Scoring and ranking are kept as separate steps: the scoring rule only ever looks at one song and one profile, while the ranking rule can later add things like diversity (avoiding an all-same-artist list) or freshness — without ever changing how individual songs are scored


## Algorithm Recipe

The recommender scores each song against a `UserProfile` using the following point system:

- **+2.0 points** — genre match (`song.genre == user.favorite_genre`)
- **+1.0 point** — mood match (`song.mood == user.favorite_mood`)
- **Similarity points**, based on `1 - |song_value - user_target|` for each numeric feature, scaled to a max value:
  - **+1.5 max** — energy similarity
  - **+1.0 max** — valence similarity
  - **+1.0 max** — tempo similarity (tempo normalized to 0–1 first)
  - **+0.75 max** — danceability similarity
  - **+0.75 max** — acousticness similarity

**Total possible score per song: 8.0**

Songs are scored one at a time (independent of every other song), then sorted descending and sliced to the top K to produce the final recommendation list.

### Potential biases

- **Genre dominance**: at 2.0 points, a genre match alone is worth more than any single numeric feature. A song that's a near-perfect mood and energy fit but in a different genre could still be outranked by a song that merely matches genre and nothing else — potentially burying great cross-genre recommendations.
- **Mid-range preference blind spot**: because the similarity formula rewards *closeness* to a target, a user profile with a target sitting near the middle of a feature's range (e.g. `target_energy: 0.55`) won't clearly favor either high- or low-energy songs, weakening the system's ability to distinguish genuinely different vibes for "moderate" users.
- **No novelty or exploration**: the recipe always returns the closest possible matches to the stated profile, so it will never surface a song outside the user's usual pattern — even if, as discussed earlier, the user sometimes wants to be surprised. That behavior isn't representable in a pure content-based scoring rule.
- **Static profile assumption**: the recipe treats `favorite_genre` and `favorite_mood` as single fixed values, so a listener with two or three distinct listening modes (e.g. workout vs. wind-down) will get recommendations blended toward an average that may not strongly satisfy either mode.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this




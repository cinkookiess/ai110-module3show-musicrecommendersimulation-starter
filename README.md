# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version of the project represents each song as a set of attributes (genre, mood, energy, tempo, valence, danceability, acousticness), represents a user as an explicit `UserProfile` of target preferences, and uses a weighted point-based scoring rule (the Algorithm Recipe below) to rank the full song catalog for that one user.

---

## How The System Works

Real-world recommendation systems like Spority or YoutTube typically combine two approaches: collaborative filtering, which predicts what a user will like based on patterns across other users' behavior, and content-based filtering, which predicts what a user will like based on the attributes of the tiems themselves. Collaborative filtering can surgace surpsing recommendations but strggles with brand-new items that have no interaction history yet. Content-based filtering solves that "cold start" roblem and produces explainable recommendations, but can't easily suggest things outside a user's establichsed attribute preferences. This simulation priotizes content-based approach only, it has no concept of other users, and works purley by matching song attributes against an explicit user preference profile.

Some prompts to answer:


- **What features does each `Song` use in your system**
  - genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- **What information does your `UserProfile` store**
  - preferred target values for energy, tempo_bpm, valence, danceability, and acousticness, plus a preferred genre and preferred mood
- **How does your `Recommender` compute a score for each song**
  - See the Algorithm Recipe section below — it's the single source of truth for the exact point values and formula used.
- **How do you choose which songs to recommend**
  - Score every song in `songs.csv` against the `UserProfile`
  - Sort songs by `song_score`, descending
  - Return the top K as the recommendation list
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


### PHASE 2
```
Loaded 20 songs from data/songs.csv

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City — Neon Echo
   Score: 7.82 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.47)
     • valence similarity (+0.91)
     • tempo similarity (+0.98)
     • danceability similarity (+0.72)
     • acousticness similarity (+0.73)

2. Gym Hero — Max Pulse
   Score: 6.48 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.30)
     • valence similarity (+0.98)
     • tempo similarity (+0.91)
     • danceability similarity (+0.65)
     • acousticness similarity (+0.64)

3. Rooftop Lights — Indigo Parade
   Score: 5.68 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.44)
     • valence similarity (+0.94)
     • tempo similarity (+0.97)
     • danceability similarity (+0.70)
     • acousticness similarity (+0.64)

4. Night Drive Loop — Neon Echo
   Score: 4.56 / 8.0
   Because:
     • energy similarity (+1.42)
     • tempo similarity (+0.92)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.73)

5. Warehouse 3AM — Kilotronic
   Score: 4.54 / 8.0
   Because:
     • energy similarity (+1.38)
     • valence similarity (+0.92)
     • tempo similarity (+0.94)
     • danceability similarity (+0.68)
     • acousticness similarity (+0.63)

==================================================
```

### PHASE 4
```
Loaded 20 songs from data/songs.csv                                        

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City — Neon Echo
   Score: 7.82 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.47)
     • valence similarity (+0.91)
     • tempo similarity (+0.98)
     • danceability similarity (+0.72)
     • acousticness similarity (+0.73)

2. Gym Hero — Max Pulse
   Score: 6.48 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.30)
     • valence similarity (+0.98)
     • tempo similarity (+0.91)
     • danceability similarity (+0.65)
     • acousticness similarity (+0.64)

3. Rooftop Lights — Indigo Parade
   Score: 5.68 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.44)
     • valence similarity (+0.94)
     • tempo similarity (+0.97)
     • danceability similarity (+0.70)
     • acousticness similarity (+0.64)

4. Night Drive Loop — Neon Echo
   Score: 4.56 / 8.0
   Because:
     • energy similarity (+1.42)
     • tempo similarity (+0.92)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.73)

5. Warehouse 3AM — Kilotronic
   Score: 4.54 / 8.0
   Because:
     • energy similarity (+1.38)
     • valence similarity (+0.92)
     • tempo similarity (+0.94)
     • danceability similarity (+0.68)
     • acousticness similarity (+0.63)

==================================================
PS C:\Users\cynth\Documents\Projects\ai110-module3show-musicrecommendersimulation-starter> python src/main.py
Loaded 20 songs from data/songs.csv

==================================================
PROFILE: High-Energy Pop
==================================================

1. Sunrise City — Neon Echo
   Score: 7.85 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.46)
     • valence similarity (+0.96)
     • tempo similarity (+0.97)
     • danceability similarity (+0.74)
     • acousticness similarity (+0.73)

2. Gym Hero — Max Pulse
   Score: 6.64 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.38)
     • valence similarity (+0.97)
     • tempo similarity (+0.92)
     • danceability similarity (+0.69)
     • acousticness similarity (+0.68)

3. Rooftop Lights — Indigo Parade
   Score: 5.67 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.36)
     • valence similarity (+0.99)
     • tempo similarity (+0.98)
     • danceability similarity (+0.74)


==================================================
PROFILE: Chill Lofi
==================================================

1. Library Rain — Paper Lanterns
   Score: 7.84 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.46)
     • valence similarity (+0.98)
     • tempo similarity (+0.97)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.71)

2. Midnight Coding — LoRoom
   Score: 7.82 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.44)
     • valence similarity (+0.98)
     • tempo similarity (+0.98)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.68)

3. Focus Flow — LoRoom
   Score: 6.91 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.47)
     • valence similarity (+0.99)
     • tempo similarity (+0.97)
     • danceability similarity (+0.75)
     • acousticness similarity (+0.73)


==================================================
PROFILE: Deep Intense Rock
==================================================

1. Storm Runner — Voltline
   Score: 7.84 / 8.0
   Because:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+1.48)
     • valence similarity (+0.92)
     • tempo similarity (+0.98)
     • danceability similarity (+0.70)
     • acousticness similarity (+0.75)

2. Glass Ceiling — Riot Kilo
   Score: 5.80 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.47)
     • valence similarity (+0.95)
     • tempo similarity (+1.00)
     • danceability similarity (+0.69)
     • acousticness similarity (+0.69)

3. Gym Hero — Max Pulse
   Score: 5.23 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.48)
     • tempo similarity (+0.86)
     • acousticness similarity (+0.71)


==================================================
PROFILE: Adversarial: Conflicting Signals
==================================================

1. Gym Hero — Max Pulse
   Score: 5.24 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.46)
     • tempo similarity (+0.94)

2. Sunrise City — Neon Echo
   Score: 5.15 / 8.0
   Because:
     • genre match (+2.0)
     • energy similarity (+1.38)
     • tempo similarity (+0.83)

3. Marble Halls — Elias Voss
   Score: 3.97 / 8.0
   Because:
     • tempo similarity (+0.89)
     • danceability similarity (+0.71)
     • acousticness similarity (+0.68)


==================================================
PROFILE: Adversarial: Nonexistent Genre
==================================================

1. Rooftop Lights — Indigo Parade
   Score: 5.01 / 8.0
   Because:
     • mood match (+1.0)
     • energy similarity (+1.26)
     • tempo similarity (+0.82)
     • acousticness similarity (+0.64)

2. Sunrise City — Neon Echo
   Score: 4.83 / 8.0
   Because:
     • mood match (+1.0)
     • tempo similarity (+0.86)

3. Dust Roads — June Carverly
   Score: 4.54 / 8.0
   Because:
     • energy similarity (+1.26)
     • valence similarity (+0.92)
     • tempo similarity (+1.00)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.62)


==================================================
PROFILE: Adversarial: Empty Profile
==================================================

1. Dust Roads — June Carverly
   Score: 4.75 / 8.0
   Because:
     • energy similarity (+1.41)
     • valence similarity (+0.98)
     • tempo similarity (+1.00)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.62)

2. Island Wind — Solar Tide
   Score: 4.42 / 8.0
   Because:
     • energy similarity (+1.47)
     • tempo similarity (+0.89)
     • danceability similarity (+0.61)
     • acousticness similarity (+0.69)

3. Midnight Coding — LoRoom
   Score: 4.40 / 8.0
   Because:
     • energy similarity (+1.38)
     • valence similarity (+0.94)
     • tempo similarity (+0.83)
     • danceability similarity (+0.66)


==================================================
PROFILE: Adversarial: Dead Center
==================================================

1. Dust Roads — June Carverly
   Score: 4.63 / 8.0
   Because:
     • energy similarity (+1.41)
     • valence similarity (+0.98)
     • tempo similarity (+0.88)
     • danceability similarity (+0.73)
     • acousticness similarity (+0.62)

2. Island Wind — Solar Tide
   Score: 4.30 / 8.0
   Because:
     • energy similarity (+1.47)
     • danceability similarity (+0.61)
     • acousticness similarity (+0.69)

3. Midnight Coding — LoRoom
   Score: 4.29 / 8.0
   Because:
     • energy similarity (+1.38)
     • valence similarity (+0.94)
     • danceability similarity (+0.66)

==================================================
```
### Mood Ablation Experiment

| Profile | Mood ON — #1 | Mood OFF — #1 | Did the ranking change? |
|---|---|---|---|
| High-Energy Pop | Sunrise City (7.85) | Sunrise City (6.85) | No — same winner, just 1.0 lower |
| Chill Lofi | Library Rain (7.84) | Focus Flow (6.91) | Yes — order flipped |


Mood's influence isn't uniform — it matters most in close races, where a handful of songs are neck-and-neck on genre and numeric similarity. In a landslide case like "Sunrise City," mood is just extra confirmation, not the deciding vote. That's a useful, general finding about weighted scoring systems: a feature's real-world impact depends on how contested the specific decision is, not just its point value in isolation.

### TESTING
```
=========================================== test session starts ===========================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\cynth\Documents\Projects\ai110-module3show-musicrecommendersimulation-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\cynth\Documents\Projects\ai110-module3show-musicrecommendersimulation-starter
collected 9 items                                                                                          

tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED                       [ 11%]
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED               [ 22%]
tests/test_recommender.py::test_recommend_flips_order_for_opposite_profile PASSED                    [ 33%]
tests/test_recommender.py::test_recommend_respects_k_limit PASSED                                    [ 44%]
tests/test_recommender.py::test_recommend_k_larger_than_catalog_does_not_crash PASSED                [ 55%]
tests/test_recommender.py::test_recommend_does_not_mutate_original_songs_list PASSED                 [ 66%]
tests/test_recommender.py::test_likes_acoustic_true_favors_high_acousticness_song PASSED             [ 77%]
tests/test_recommender.py::test_explain_recommendation_mentions_genre_when_matched PASSED            [ 88%]
tests/test_recommender.py::test_explain_recommendation_no_false_genre_claim_on_mismatch PASSED       [100%]

============================================ 9 passed in 0.08s ============================================
(.venv) 
```

### FINAL OUTPUT

```
Loaded 20 songs from data/songs.csv

==================================================
PROFILE: High-Energy Pop
==================================================

+-----+----------------+---------------+------------+---------------------------------+
|   # | Title          | Artist        | Score      | Reasons                         |
+=====+================+===============+============+=================================+
|   1 | Sunrise City   | Neon Echo     | 7.85 / 8.0 | genre match (+2.0)              |
|     |                |               |            | mood match (+1.0)               |
|     |                |               |            | energy similarity (+1.46)       |
|     |                |               |            | valence similarity (+0.96)      |
|     |                |               |            | tempo similarity (+0.97)        |
|     |                |               |            | danceability similarity (+0.74) |
|     |                |               |            | acousticness similarity (+0.73) |
+-----+----------------+---------------+------------+---------------------------------+
|   2 | Gym Hero       | Max Pulse     | 6.64 / 8.0 | genre match (+2.0)              |
|     |                |               |            | energy similarity (+1.38)       |
|     |                |               |            | valence similarity (+0.97)      |
|     |                |               |            | tempo similarity (+0.92)        |
|     |                |               |            | danceability similarity (+0.69) |
|     |                |               |            | acousticness similarity (+0.68) |
+-----+----------------+---------------+------------+---------------------------------+
|   3 | Rooftop Lights | Indigo Parade | 5.67 / 8.0 | mood match (+1.0)               |
|     |                |               |            | energy similarity (+1.36)       |
|     |                |               |            | valence similarity (+0.99)      |
|     |                |               |            | tempo similarity (+0.98)        |
|     |                |               |            | danceability similarity (+0.74) |
+-----+----------------+---------------+------------+---------------------------------+

==================================================
PROFILE: Chill Lofi
==================================================

+-----+-----------------+----------------+------------+---------------------------------+
|   # | Title           | Artist         | Score      | Reasons                         |
+=====+=================+================+============+=================================+
|   1 | Library Rain    | Paper Lanterns | 7.84 / 8.0 | genre match (+2.0)              |
|     |                 |                |            | mood match (+1.0)               |
|     |                 |                |            | energy similarity (+1.46)       |
|     |                 |                |            | valence similarity (+0.98)      |
|     |                 |                |            | tempo similarity (+0.97)        |
|     |                 |                |            | danceability similarity (+0.73) |
|     |                 |                |            | acousticness similarity (+0.71) |
+-----+-----------------+----------------+------------+---------------------------------+
|   2 | Midnight Coding | LoRoom         | 7.82 / 8.0 | genre match (+2.0)              |
|     |                 |                |            | mood match (+1.0)               |
|     |                 |                |            | energy similarity (+1.44)       |
|     |                 |                |            | valence similarity (+0.98)      |
|     |                 |                |            | tempo similarity (+0.98)        |
|     |                 |                |            | danceability similarity (+0.73) |
|     |                 |                |            | acousticness similarity (+0.68) |
+-----+-----------------+----------------+------------+---------------------------------+
|   3 | Focus Flow      | LoRoom         | 6.91 / 8.0 | genre match (+2.0)              |
|     |                 |                |            | energy similarity (+1.47)       |
|     |                 |                |            | valence similarity (+0.99)      |
|     |                 |                |            | tempo similarity (+0.97)        |
|     |                 |                |            | danceability similarity (+0.75) |
|     |                 |                |            | acousticness similarity (+0.73) |
+-----+-----------------+----------------+------------+---------------------------------+

==================================================
PROFILE: Deep Intense Rock
==================================================

+-----+---------------+-----------+------------+---------------------------------+
|   # | Title         | Artist    | Score      | Reasons                         |
+=====+===============+===========+============+=================================+
|   1 | Storm Runner  | Voltline  | 7.84 / 8.0 | genre match (+2.0)              |
|     |               |           |            | mood match (+1.0)               |
|     |               |           |            | energy similarity (+1.48)       |
|     |               |           |            | valence similarity (+0.92)      |
|     |               |           |            | tempo similarity (+0.98)        |
|     |               |           |            | danceability similarity (+0.70) |
|     |               |           |            | acousticness similarity (+0.75) |
+-----+---------------+-----------+------------+---------------------------------+
|   2 | Glass Ceiling | Riot Kilo | 5.80 / 8.0 | mood match (+1.0)               |
|     |               |           |            | energy similarity (+1.47)       |
|     |               |           |            | valence similarity (+0.95)      |
|     |               |           |            | tempo similarity (+1.00)        |
|     |               |           |            | danceability similarity (+0.69) |
|     |               |           |            | acousticness similarity (+0.69) |
+-----+---------------+-----------+------------+---------------------------------+
|   3 | Gym Hero      | Max Pulse | 5.23 / 8.0 | mood match (+1.0)               |
|     |               |           |            | energy similarity (+1.48)       |
|     |               |           |            | tempo similarity (+0.86)        |
|     |               |           |            | acousticness similarity (+0.71) |
+-----+---------------+-----------+------------+---------------------------------+

==================================================
PROFILE: Adversarial: Conflicting Signals
==================================================

+-----+--------------+------------+------------+---------------------------------+
|   # | Title        | Artist     | Score      | Reasons                         |
+=====+==============+============+============+=================================+
|   1 | Gym Hero     | Max Pulse  | 5.24 / 8.0 | genre match (+2.0)              |
|     |              |            |            | energy similarity (+1.46)       |
|     |              |            |            | tempo similarity (+0.94)        |
+-----+--------------+------------+------------+---------------------------------+
|   2 | Sunrise City | Neon Echo  | 5.15 / 8.0 | genre match (+2.0)              |
|     |              |            |            | energy similarity (+1.38)       |
|     |              |            |            | tempo similarity (+0.83)        |
+-----+--------------+------------+------------+---------------------------------+
|   3 | Marble Halls | Elias Voss | 3.97 / 8.0 | tempo similarity (+0.89)        |
|     |              |            |            | danceability similarity (+0.71) |
|     |              |            |            | acousticness similarity (+0.68) |
+-----+--------------+------------+------------+---------------------------------+

==================================================
PROFILE: Adversarial: Nonexistent Genre
==================================================

+-----+----------------+---------------+------------+---------------------------------+
|   # | Title          | Artist        | Score      | Reasons                         |
+=====+================+===============+============+=================================+
|   1 | Rooftop Lights | Indigo Parade | 5.01 / 8.0 | mood match (+1.0)               |
|     |                |               |            | energy similarity (+1.26)       |
|     |                |               |            | tempo similarity (+0.82)        |
|     |                |               |            | acousticness similarity (+0.64) |
+-----+----------------+---------------+------------+---------------------------------+
|   2 | Sunrise City   | Neon Echo     | 4.83 / 8.0 | mood match (+1.0)               |
|     |                |               |            | tempo similarity (+0.86)        |
+-----+----------------+---------------+------------+---------------------------------+
|   3 | Dust Roads     | June Carverly | 4.54 / 8.0 | energy similarity (+1.26)       |
|     |                |               |            | valence similarity (+0.92)      |
|     |                |               |            | tempo similarity (+1.00)        |
|     |                |               |            | danceability similarity (+0.73) |
|     |                |               |            | acousticness similarity (+0.62) |
+-----+----------------+---------------+------------+---------------------------------+

==================================================
PROFILE: Adversarial: Empty Profile
==================================================

+-----+-----------------+---------------+------------+---------------------------------+
|   # | Title           | Artist        | Score      | Reasons                         |
+=====+=================+===============+============+=================================+
|   1 | Dust Roads      | June Carverly | 4.75 / 8.0 | energy similarity (+1.41)       |
|     |                 |               |            | valence similarity (+0.98)      |
|     |                 |               |            | tempo similarity (+1.00)        |
|     |                 |               |            | danceability similarity (+0.73) |
|     |                 |               |            | acousticness similarity (+0.62) |
+-----+-----------------+---------------+------------+---------------------------------+
|   2 | Island Wind     | Solar Tide    | 4.42 / 8.0 | energy similarity (+1.47)       |
|     |                 |               |            | tempo similarity (+0.89)        |
|     |                 |               |            | danceability similarity (+0.61) |
|     |                 |               |            | acousticness similarity (+0.69) |
+-----+-----------------+---------------+------------+---------------------------------+
|   3 | Midnight Coding | LoRoom        | 4.40 / 8.0 | energy similarity (+1.38)       |
|     |                 |               |            | valence similarity (+0.94)      |
|     |                 |               |            | tempo similarity (+0.83)        |
|     |                 |               |            | danceability similarity (+0.66) |
+-----+-----------------+---------------+------------+---------------------------------+

==================================================
PROFILE: Adversarial: Dead Center
==================================================

+-----+-----------------+---------------+------------+---------------------------------+
|   # | Title           | Artist        | Score      | Reasons                         |
+=====+=================+===============+============+=================================+
|   1 | Dust Roads      | June Carverly | 4.63 / 8.0 | energy similarity (+1.41)       |
|     |                 |               |            | valence similarity (+0.98)      |
|     |                 |               |            | tempo similarity (+0.88)        |
|     |                 |               |            | danceability similarity (+0.73) |
|     |                 |               |            | acousticness similarity (+0.62) |
+-----+-----------------+---------------+------------+---------------------------------+
|   2 | Island Wind     | Solar Tide    | 4.30 / 8.0 | energy similarity (+1.47)       |
|     |                 |               |            | danceability similarity (+0.61) |
|     |                 |               |            | acousticness similarity (+0.69) |
+-----+-----------------+---------------+------------+---------------------------------+
|   3 | Midnight Coding | LoRoom        | 4.29 / 8.0 | energy similarity (+1.38)       |
|     |                 |               |            | valence similarity (+0.94)      |
|     |                 |               |            | danceability similarity (+0.66) |
+-----+-----------------+---------------+------------+---------------------------------+
==================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- **Removed the mood-match bonus** to isolate its actual effect on rankings (see "Mood Ablation Experiment" above). Result: mood only changed the #1 result in close races, not in landslide profiles.
- **Ran three coherent user profiles** (High-Energy Pop, Chill Lofi, Deep Intense Rock) to confirm genuinely different stated tastes produce genuinely different, non-overlapping top results.
- **Ran four adversarial profiles** (Conflicting Signals, Nonexistent Genre, Empty Profile, Dead Center) to probe edge cases — see `model_card.md` section 7 for the full breakdown of what each one revealed.

---

## Limitations and Risks

Summarize some limitations of your recommender.

- It only works on a small, 20-song catalog, so users with niche or extreme preferences have a much smaller effective pool than the total count suggests.
- It does not understand lyrics, language, artist identity, or cultural context — only the seven numeric/categorical attributes in `songs.csv`.
- It can over-favor genre and energy matches over mood, and songs near the dataset's numeric "center" can rank artificially high for vague or empty user profiles regardless of genre.
You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:


Building this project made it concrete how a recommender turns raw data into a prediction: every song attribute (genre, mood, energy, tempo, valence, danceability, acousticness) gets compared against a target the user stated, each comparison produces a small number, and all of those numbers get added into one final score per song. There's no magic in that step — it's just weighted arithmetic, repeated once per song in the catalog, then sorted. What surprised me is how much a single feature's real influence depends on context rather than its point value alone. When I disabled the mood-match bonus as an experiment, it barely changed anything for a profile with one dominant, landslide winner (High-Energy Pop), but it flipped the #1 result for a closer race (Chill Lofi). A fixed weight doesn't guarantee a fixed amount of real-world influence — it only guarantees a fixed number of points, and how much those points actually matter depends on how contested the specific decision already is.
 
Bias and unfairness in a system like this don't show up as a dramatic failure — they show up quietly, in the choices baked into the scoring rule itself. Genre and mood are treated as strict binary matches (2.0 or 0, 1.0 or nothing), so users whose taste sits between categories get no partial credit there at all, even though the numeric features get to reward "close enough." Missing data creates a subtler problem: an empty preference profile and a profile that explicitly asks for "everything average" produce nearly identical recommendations, because both fall back to the same hardcoded default values — the system can't tell "we know nothing about this person" apart from "this person genuinely wants the most average song in the catalog." And because the numeric similarity terms outweigh genre and mood combined, users with moderate, average-ish preferences quietly get funneled toward whichever song sits closest to the dataset's numeric center, regardless of genre — which is exactly the kind of invisible, well-intentioned design choice that could make a real recommendation system feel "off" to a user without ever throwing an error or looking obviously broken.


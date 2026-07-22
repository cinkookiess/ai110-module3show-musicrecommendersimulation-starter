"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Three distinct, coherent user profiles
    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
            "target_valence": 0.8,
            "target_tempo_bpm": 122,
            "target_danceability": 0.8,
            "target_acousticness": 0.15,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.38,
            "target_valence": 0.58,
            "target_tempo_bpm": 76,
            "target_danceability": 0.6,
            "target_acousticness": 0.8,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "target_valence": 0.4,
            "target_tempo_bpm": 150,
            "target_danceability": 0.6,
            "target_acousticness": 0.1,
        },
 
        # --- Adversarial / edge-case profiles ---
        # Tests whether contradictory signals (high energy + sad mood)
        # produce a coherent ranking or a confused, averaged-out one.
        "Adversarial: Conflicting Signals": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "target_valence": 0.15,
            "target_tempo_bpm": 140,
            "target_danceability": 0.3,
            "target_acousticness": 0.85,
        },
 
        # Tests whether a genre with zero matches in the catalog still
        # returns sane, numeric-similarity-driven results (score never
        # errors out, genre bonus contributes 0 for every song).
        "Adversarial: Nonexistent Genre": {
            "favorite_genre": "opera",
            "favorite_mood": "happy",
            "target_energy": 0.6,
            "target_valence": 0.6,
            "target_tempo_bpm": 100,
            "target_danceability": 0.5,
            "target_acousticness": 0.5,
        },
 
        # Tests default fallback behavior in score_song's .get() calls
        # when the profile supplies nothing at all.
        "Adversarial: Empty Profile": {},
 
        # Tests the "too vague to differentiate" failure mode: every
        # numeric target sits at the exact midpoint of its range, so
        # no song should stand out clearly from any other.
        "Adversarial: Dead Center": {
            "favorite_genre": "none",
            "favorite_mood": "none",
            "target_energy": 0.5,
            "target_valence": 0.5,
            "target_tempo_bpm": 115,
            "target_danceability": 0.5,
            "target_acousticness": 0.5,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)
 
        print("\n" + "=" * 50)
        print(f"PROFILE: {profile_name}")
        print("=" * 50 + "\n")
 
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} — {song['artist']}")
            print(f"   Score: {score:.2f} / 8.0")
            print("   Because:")
            for reason in explanation.split("; "):
                print(f"     • {reason}")
            print()
 
    print("=" * 50)


if __name__ == "__main__":
    main()

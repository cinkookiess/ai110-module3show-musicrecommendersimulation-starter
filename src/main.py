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

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.75,
        "target_tempo_bpm": 120,
        "target_danceability": 0.75,
        "target_acousticness": 0.2,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("TOP RECOMMENDATIONS")
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

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs


    @staticmethod
    def _user_to_prefs(user: UserProfile) -> Dict:
        """
        Converts a UserProfile dataclass into the dict shape score_song
        expects. UserProfile only carries favorite_genre, favorite_mood,
        target_energy, and likes_acoustic, so the other numeric targets
        (valence, tempo, danceability) fall back to score_song's own
        neutral defaults. likes_acoustic maps to a concrete acousticness
        target rather than a neutral default, since it's an explicit
        yes/no signal, not a missing one.
        """
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "target_acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
 
    @staticmethod
    def _song_to_dict(song: Song) -> Dict:
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

    
    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = self._user_to_prefs(user)
        scored = [
            (song, score_song(user_prefs, self._song_to_dict(song))[0])
            for song in self.songs
        ]
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = self._user_to_prefs(user)
        _, reasons = score_song(user_prefs, self._song_to_dict(song))
        return "; ".join(reasons) if reasons else "no strong matches, but closest available"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py


    Reads data/songs.csv using csv.DictReader and returns a list of
    dictionaries, one per song. Numeric columns are explicitly converted
    to int/float so later scoring math (e.g. abs(song["energy"] - target))
    doesn't fail or silently misbehave on string values.
    """
    songs = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs
 
MIN_TEMPO = 50.0
MAX_TEMPO = 180.0


def _normalize_tempo(tempo_bpm: float) -> float:
    """Scales tempo_bpm to a 0-1 range so it's comparable to the other features."""
    clamped = max(MIN_TEMPO, min(MAX_TEMPO, tempo_bpm))
    return (clamped - MIN_TEMPO) / (MAX_TEMPO - MIN_TEMPO)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
   Scores a single song against user preferences using the Algorithm Recipe:
      +2.0  genre match
      +1.0  mood match
      +1.5 max  energy similarity
      +1.0 max  valence similarity
      +1.0 max  tempo similarity (normalized)
      +0.75 max danceability similarity
      +0.75 max acousticness similarity
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []
 
    if song["genre"] == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")
 
    if song["mood"] == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")
 
    energy_sim = 1 - abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    energy_points = 1.5 * energy_sim
    score += energy_points
    if energy_sim > 0.8:
        reasons.append(f"energy similarity (+{energy_points:.2f})")
 
    valence_sim = 1 - abs(song["valence"] - user_prefs.get("target_valence", 0.5))
    valence_points = 1.0 * valence_sim
    score += valence_points
    if valence_sim > 0.8:
        reasons.append(f"valence similarity (+{valence_points:.2f})")
 
    user_tempo_norm = _normalize_tempo(user_prefs.get("target_tempo_bpm", 100.0))
    song_tempo_norm = _normalize_tempo(song["tempo_bpm"])
    tempo_sim = 1 - abs(song_tempo_norm - user_tempo_norm)
    tempo_points = 1.0 * tempo_sim
    score += tempo_points
    if tempo_sim > 0.8:
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")
 
    dance_sim = 1 - abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))
    dance_points = 0.75 * dance_sim
    score += dance_points
    if dance_sim > 0.8:
        reasons.append(f"danceability similarity (+{dance_points:.2f})")
 
    acoustic_sim = 1 - abs(song["acousticness"] - user_prefs.get("target_acousticness", 0.5))
    acoustic_points = 0.75 * acoustic_sim
    score += acoustic_points
    if acoustic_sim > 0.8:
        reasons.append(f"acousticness similarity (+{acoustic_points:.2f})")
 
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores every song, sorts by score descending, and returns the top K
    along with a human-readable explanation for each.
    Required by src/main.py
    """
    scored = [
        (song, score, "; ".join(reasons) if reasons else "no strong matches, but closest available")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
 
    # sorted() (not .sort()) is used deliberately: it returns a new list
    # rather than mutating `songs` in place, so the caller's original
    # song list is never silently reordered as a side effect.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]

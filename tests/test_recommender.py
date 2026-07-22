from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""

    
def test_recommend_flips_order_for_opposite_profile():
    """The lofi/chill profile should rank the lofi song above the pop song —
    the mirror image of the existing pop test. This confirms the ranking
    actually responds to the profile, rather than always returning songs
    in their original list order."""
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=True,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert results[0].genre == "lofi"
    assert results[0].mood == "chill"


def test_recommend_respects_k_limit():
    """k=1 should return exactly one song, not the full list."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=1)

    assert len(results) == 1
    assert results[0].genre == "pop"


def test_recommend_k_larger_than_catalog_does_not_crash():
    """Asking for more recommendations than songs exist should return
    everything available, not raise an IndexError."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=10)

    assert len(results) == 2


def test_recommend_does_not_mutate_original_songs_list():
    """recommend() should not reorder rec.songs as a side effect —
    calling it twice with different profiles should give different
    top results without the underlying list order changing."""
    rec = make_small_recommender()
    original_order = [s.title for s in rec.songs]

    pop_user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec.recommend(pop_user, k=2)

    assert [s.title for s in rec.songs] == original_order


def test_likes_acoustic_true_favors_high_acousticness_song():
    """A user who likes_acoustic=True should score the high-acousticness
    lofi song (0.9) noticeably higher than a user with likes_acoustic=False,
    all else being equal. This locks in the likes_acoustic -> acousticness
    target mapping as an actual behavior, not just an unused field."""
    rec = make_small_recommender()
    lofi_song = rec.songs[1]

    acoustic_lover = UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.4, likes_acoustic=True)
    acoustic_hater = UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.4, likes_acoustic=False)

    explanation_lover = rec.explain_recommendation(acoustic_lover, lofi_song)
    explanation_hater = rec.explain_recommendation(acoustic_hater, lofi_song)

    assert "acousticness" in explanation_lover.lower()
    # The acoustic lover's explanation should reflect a stronger acousticness match
    assert explanation_lover != explanation_hater


def test_explain_recommendation_mentions_genre_when_matched():
    """When genre actually matches, the explanation should say so explicitly —
    not just be some non-empty string (the current test's weakest point)."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    pop_song = rec.songs[0]

    explanation = rec.explain_recommendation(user, pop_song)
    assert "genre" in explanation.lower()


def test_explain_recommendation_no_false_genre_claim_on_mismatch():
    """When genre does NOT match, the explanation should not falsely claim
    a genre match — guards against a copy-paste bug in the reasons list."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    lofi_song = rec.songs[1]  # genre="lofi", doesn't match user's "pop"

    explanation = rec.explain_recommendation(user, lofi_song)
    assert "genre match" not in explanation.lower()
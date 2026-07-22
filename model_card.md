# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**GetIntoTheMood 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

This recommender generates a ranked list of songs from a fixed catalog, matched to a single stated user profile — it's a content-based recommender, not a collaborative one, so it never looks at other users' behavior, only the attributes of the songs themselves compared to what one user says they want.
 
It assumes a user's taste can be captured as a small set of explicit numbers and categories: a favorite genre, a favorite mood, and target values for energy, valence, tempo, danceability, and acousticness. It does not assume the user has any listening history — the whole advantage of a content-based approach is that it works from a stated profile alone, with no cold-start problem. It also assumes a user has roughly one stable "type" of taste at a time; a single profile can't represent someone who wants completely different things depending on mood or context (workout vs. wind-down) without running the recommender twice with two separate profiles.
 
This is a classroom exploration project, not a production system for real listeners. It's built to demonstrate and interrogate how a simple scoring/ranking recommender behaves — including its edge cases and biases — using a small, hand-curated dataset kept intentionally simple enough that every recommendation can be traced back to a specific rule.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

Every song has a handful of attributes attached to it: what genre it is, what mood it's tagged with, how energetic it feels, how happy or sad it sounds (valence), how fast it is (tempo), how danceable it is, and how acoustic versus electronic it sounds. Every user also has a profile describing what they want on those same dimensions — their favorite genre, favorite mood, and a target value for each of the numeric attributes.
 
To turn that into a recommendation, the model goes through every single song in the catalog, one at a time, and gives it a score — like a report card with several subjects. It gets full points if the genre matches exactly, and separate full points if the mood matches exactly. For everything else — energy, valence, tempo, danceability, acousticness — it doesn't just check "is this high or low," it checks "how close is this song's value to what the user actually asked for," so a user who wants moderate energy isn't penalized for a song not being the most extreme option available. All those points get added together into one final number per song. Once every song has a score, the songs are sorted from highest to lowest, and the top handful are handed back to the user, each with a plain-language list of exactly which parts of its score came from where (e.g. "genre match," "energy similarity").
 
The starter logic only returned the first few songs in the file, with no scoring or sorting at all, and its explanation function returned a hardcoded placeholder sentence regardless of the song. Everything about the actual scoring recipe — the point values, the closeness-based math for numeric features, the human-readable reasons — was built from scratch on top of that starting skeleton.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

The catalog contains 20 songs. The original starter file had 10 songs across 7 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop) and 6 moods (happy, chill, intense, relaxed, moody, focused). I added 10 more songs to expand the range, bringing in 7 new genres (folk, metal, r&b, reggae, classical, edm, country) and 7 new moods (nostalgic, aggressive, romantic, triumphant, melancholic, euphoric, dreamy) — so the full dataset now spans 14 genres and 13 moods across 20 songs.
 
Nothing was removed from the original file; the 10 new songs were added alongside it.
 
There's a lot of musical taste this dataset can't represent. It has no lyrical content or subject matter, no vocal style or language, no cultural or era-specific context (a song "feels like a specific summer" for reasons no attribute here captures), and no notion of production quality, instrumentation, or artist reputation. It's also thin at the extremes — very few songs sit above 0.9 energy or below 0.1 acousticness, so a user with an intense preference profile has a much smaller effective pool to draw recommendations from than a user with a moderate one, even though the catalog looks like it has 20 options overall.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

The system works best for users whose stated preferences are internally coherent and land near an actual cluster of songs in the data — the three "type" profiles I tested (High-Energy Pop, Chill Lofi, Deep Intense Rock) each produced a top result that a human would immediately recognize as the right vibe, with genre, mood, and every numeric similarity term pointing the same direction at once.
 
The scoring recipe correctly captures the idea that a song can be a strong match without matching everything — a song missing a mood tag but nailing genre and energy still ranks reasonably rather than being thrown out, which mirrors how people actually judge whether a recommendation "sort of" fits.
 
The clearest case where the recommendations matched my intuition was Deep Intense Rock versus Chill Lofi: their top picks, "Storm Runner" and "Library Rain," sit near-opposite ends of the energy and acousticness scale, and the two profiles shared zero overlap in their top 3 results. That's exactly what you'd want from a working content-based recommender — genuinely different stated tastes produce genuinely different, non-overlapping recommendations, not a vague convergence toward the same "safe" songs regardless of what was asked for.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

**Features it does not consider**: the model has no concept of lyrics, subject matter, vocals, language, artist identity, production quality, or cultural/personal context (a song "feels like summer" for reasons no attribute here captures). It also has no listening-history or feedback mechanism — it can't learn from skips, repeats, or explicit likes, since it's purely content-based and stateless between runs.
 
**Genres and moods that are underrepresented**: the dataset has only 1-2 songs for several genres (e.g. classical, reggae, r&b), so a user whose stated genre falls into one of these sparsely-populated categories has almost no fallback options if their numeric targets don't happen to align well with that one or two songs. The dataset is also thin at the energy extremes — very few songs sit above 0.9 energy or below 0.1 acousticness — so users with intense preference profiles are effectively choosing from a much smaller pool than the "20 songs" total suggests.
 
**Cases where the system overfits to one preference**: the "Conflicting Signals" test (high energy + sad mood) showed that when a user's stated preferences don't correspond to any real combination in the dataset, the system doesn't recognize the contradiction — it just returns whatever song happens to be least bad, with a noticeably lower score as the only hint something was off. It has no way to say "I don't have a good answer for this" versus "here's a strong match."
 
**Ways the scoring might unintentionally favor some users**: two concrete biases surfaced during testing:
- *Genre and energy can outweigh mood.* In the "High-Energy Pop" test, "Gym Hero" (mood: intense, not happy) still ranked #2 by scoring well on genre and energy alone — a user who cares most about mood may see songs that miss on the dimension they value most, simply because other dimensions matched strongly enough to compensate.
- *Users with "average" or default-adjacent preferences get funneled toward whichever song is statistically closest to the dataset's center*, regardless of genre. The "Empty Profile" and "Dead Center" tests both surfaced "Dust Roads" as the top pick, despite being designed to represent two different situations (no information at all, versus an explicit average preference) — the numeric similarity terms currently can't tell those two cases apart, so both get the same generic answer rather than something tailored to what the user actually meant.


Weakness: the numeric similarity terms structurally out-weigh categorical matches, which quietly erases genre diversity for users with common "middle-of-the-road" targets. Since the five similarity terms sum to a 5.0-point ceiling versus 3.0 for genre+mood combined, two songs from completely different genres can score almost identically as long as their energy, valence, tempo, danceability, and acousticness happen to cluster near the same values — which is exactly what happened with "Dust Roads" (country) topping both the empty and dead-center profiles ahead of every lofi, pop, or ambient track. In practice, this means any user whose stated preferences sit near the dataset's numeric center gets funneled toward whichever song is statistically "most average," regardless of genre, rather than seeing the genre variety the catalog actually contains.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

### Which user profiles you tested  

I tested seven profiles against the 20-song dataset: three "coherent" profiles representing realistic listeners (High-Energy Pop, Chill Lofi, Deep Intense Rock), and four adversarial/edge-case profiles designed to probe weaknesses (Conflicting Signals, Nonexistent Genre, Empty Profile, Dead Center).

### What you looked for in the recommendations  

For each profile, I checked whether the #1 recommendation actually matched the "vibe" a real person with that profile would expect, whether the point breakdown ("Because: ...") told a believable story for why that song won, and whether different profiles produced meaningfully different top results rather than converging on the same few songs.
 
#### Comparisons between profile pairs
 
- **High-Energy Pop vs. Chill Lofi**: High-Energy Pop surfaces "Sunrise City" (energy 0.82, tempo 118) at the top, while Chill Lofi surfaces "Library Rain" (energy 0.35, tempo 72). This makes sense — these two profiles have opposite `target_energy` and `target_tempo_bpm` values, so the energy and tempo similarity terms alone would be enough to separate them even without genre. The genre match on top of that just reinforces the same direction the numeric features were already pointing.
- **Deep Intense Rock vs. Chill Lofi**: Deep Intense Rock's top pick, "Storm Runner" (energy 0.91, acousticness 0.10), is close to the exact opposite of Chill Lofi's top pick, "Library Rain" (energy 0.35, acousticness 0.86) on every numeric axis. This is the clearest "does the system actually differentiate opposite vibes" check, and it passed — the two profiles share no songs in their top 3 at all.
- **High-Energy Pop vs. Adversarial: Conflicting Signals** (energy 0.9 + mood "sad"): High-Energy Pop's winner scores 7.85; the Conflicting Signals winner only scores 5.24. The drop in score is the system's only way of "flagging" that the request was internally contradictory — it can't say "this doesn't make sense," it can only fail to find anything that scores well, since no song in the catalog is genuinely both high-energy and sad-sounding at once.
- **Adversarial: Empty Profile vs. Adversarial: Dead Center**: these two were designed to test different things (no data at all vs. an explicit average) but produced nearly the same top pick ("Dust Roads" in both cases). This was the biggest surprise of the evaluation — see below.

### What surprised you  
The most surprising result was that an **empty preferences dictionary and an explicit "everything is average" profile behave identically**. I expected "no preferences given" to produce something like a neutral, popularity-based fallback, or at least a different result than a profile that deliberately set every target to 0.5. Instead, because `score_song` uses `.get(key, 0.5)` as the default for missing keys, an empty dict silently becomes the same as typing in 0.5 for every field. That's not a crash or an obviously wrong answer — it's a quiet design gap where two conceptually different situations ("we know nothing about this user" vs. "this user genuinely wants average music") produce the exact same recommendations.

### Any simple tests or comparisons you ran  

- Beyond the two starter tests, I added tests that check the ranking actually responds to different profiles rather than just returning songs in list order — e.g. a lofi/chill profile correctly ranks the lofi song above the pop song, mirroring the existing pop test in reverse. I also added boundary tests (k=1, and k larger than the whole catalog) to make sure the top-k slicing doesn't crash or silently drop songs, a test confirming recommend() doesn't mutate the original song list as a side effect, and tests that check explain_recommendation()'s text actually says "genre match" when genre matches and does not say it when genre doesn't match — tightening the original test, which only checked that some non-empty string came back.
- Manual comparison across profiles: ran all seven profiles (three coherent, four adversarial) through main.py and manually inspected each (score, reasons) breakdown, confirming the reasons matched what a human would expect from the song's actual attributes in songs.csv.
- Mood-ablation experiment: temporarily commented out the mood-match bonus in score_song and re-ran the same profiles, to directly measure how much mood actually changes the final ranking rather than assuming its effect from the point weight alone. Result: mood only changed the #1 pick in close races (Chill Lofi), not in landslide cases (High-Energy Pop) — see the "What surprised me" discussion above for the full comparison.
- No formal numeric metrics (precision/recall, etc.) were computed, since there's no ground-truth "correct" answer for a simulated taste profile — evaluation here relied on manual inspection plus the automated tests above, not statistical scoring.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

**Additional features or preferences**: two features suggested during dataset expansion — instrumentalness (vocal vs. instrumental) and dynamic range (how much a track swings between quiet and loud sections) — were never actually wired into the scoring recipe. Adding them would let the system distinguish tracks that currently look identical on every existing attribute but feel different (e.g. two "intense" metal tracks with and without vocals). I'd also want to let a profile express *multiple* favorite genres or moods instead of exactly one, since forcing a single value is part of why the "Dead Center" and sparse-genre problems showed up.
 
**Better ways to explain recommendations**: right now, "reasons" are only shown for terms that cross a similarity threshold, and they list every qualifying feature with equal visual weight. A clearer version would rank the reasons by how much they actually contributed to the score (e.g. lead with genre match before a marginal 0.81 danceability similarity), and explicitly say when a song was recommended *despite* missing something important — e.g. "closest available match, but mood does not match" — rather than silently omitting the negative.
 
**Improving diversity among the top results**: the current ranking rule is a pure sort by score, so a user with a narrow, dominant preference (like Deep Intense Rock) risks getting a top-5 list clustered around one artist or one narrow attribute range. A next step would be adding a de-duplication rule (e.g. no more than one song per artist in the top-k) and the exploration-slot idea discussed earlier — deliberately reserving one recommendation slot for a lower-scored but different song, so users who occasionally want to be surprised get that option built in rather than always receiving the "safest" possible list.
 
**Handling more complex user tastes**: the biggest structural gap is that one profile can only represent one "mode" of listening. A real next step would be supporting multiple named profiles per user (e.g. "workout" vs. "wind-down") and letting the app ask which mode applies before recommending, rather than forcing every context into a single static target. Longer-term, this is also where the Phase 1 discussion of collaborative filtering becomes relevant again — real interaction data (skips, replays, explicit feedback) could eventually replace or supplement the static profile, letting the system learn a user's actual taste rather than relying entirely on what they're able to articulate up front.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

What I learned from building this recommender is how many difficult tradeoffs go into trying to predict what a user will actually prefer, once you reduce a song down to a handful of numbers. Humans aren't machines, so getting a scoring system to match what a human is actually thinking is genuinely hard. Adding up multiple weighted preferences at once is an interesting problem, and going through this process made me understand a lot more about why some companies don't always get it right, based on my own experience as a listener.

Something interesting I discovered was how uneven mood's actual impact turned out to be. When I disabled the mood-match bonus as an experiment, it barely changed anything for a profile with a clear, dominant preference (High-Energy Pop) — the same song won either way. But for a closer, more ambiguous profile (Chill Lofi), removing mood was enough to flip which song ranked #1. That surprised me, because I expected a single point-weight to matter the same amount every time. Instead, a feature's real influence depends on how close the competition already is — it's a bigger deal in a close race than a landslide. I don't think that fully accounts for every real listener, though; someone who cares about mood above everything else would probably want it weighted much more heavily regardless of how "close" the other songs are, and this system doesn't let a user express that kind of priority.

This changed the way I think about music recommendation apps. Spotify DJ, for example, is an AI-trained model, but it sometimes plays songs I don't like at all. Building this project helped me understand why that might happen: it's possible the app is deliberately nudging me away from over-indexing on one genre, similar to how this system will sometimes rank a song highly on strong genre and energy matches alone, even when mood is off. It could also be that artists and labels are pushing certain songs into rotation, which adds a layer of business incentive that has nothing to do with matching my actual taste. Either way, this project made it much clearer that a recommendation I don't like isn't necessarily a "broken" system — it might be the system correctly optimizing for something other than my own narrow, stated preference.


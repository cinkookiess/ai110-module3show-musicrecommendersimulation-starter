# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  


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

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

#!/usr/bin/env python3
"""Generate all Week 7 Edge TTS audio files using en-US-AnaNeural voice."""
import asyncio
import os
import edge_tts

VOICE = "en-US-AnaNeural"
RATE = "-10%"
OUTPUT_DIR = "assets/audio/week7"

AUDIO_MAP = {
    # === SHARED ===
    "star": "Yay! You earned a star!",

    # === ELA: SYLLABLES (All Week) ===
    "syl-intro": "Welcome to Syllables! Syllables are the beats in words. Clap and count the beats! Let's learn about syllables!",
    "syl-correct": "Yes! You counted the syllables correctly! Great job!",
    "syl-wrong": "Hmm, not quite. Try clapping the word and counting each beat!",
    "syl-complete": "Amazing! You are a syllable superstar! You can count the beats in any word!",
    "syl-h1-intro": "Let's count syllables! Clap out the beats in each word. How many claps do you hear?",
    "syl-h2-intro": "Which word has more syllables? Listen carefully and compare the words!",
    "syl-h3-intro": "Let's sort words by their syllables! One beat, two beats, or three beats?",
    "syl-h4-intro": "Welcome to compound words! Two little words make one big word! Like rain plus bow makes rainbow!",

    # === MATH: COUNTING PICTURES (All Week) ===
    "count-intro": "Welcome to Counting Pictures! Let's count objects in pictures! Use your finger to count each one!",
    "count-correct": "Yes! You counted correctly! Great counting!",
    "count-wrong": "Hmm, not quite. Try counting each picture one by one!",
    "count-complete": "Wonderful! You are an amazing counter! You can count any number of pictures!",
    "count-ee1-intro": "Let's count up to fifteen! Count the pictures carefully. How many do you see?",
    "count-ee2-intro": "Let's count in arrays! Arrays are rows and columns. Count each row to find the total!",
    "count-ee3-intro": "Let's count stickers! Count all the stickers on the page. How many stickers are there?",
    "count-ee4-intro": "Let's count up to twenty! These are bigger numbers. Take your time and count carefully!",

    # === SCIENCE: COMPARING (All Week) ===
    "comp-intro": "Welcome to Comparing! Scientists compare things to understand the world. Let's compare long and short, heavy and light, hot and cold, and fast and slow!",
    "comp-correct": "Yes! Great comparing! You are thinking like a scientist!",
    "comp-wrong": "Hmm, look again. Compare the two objects carefully!",
    "comp-complete": "Amazing! You can compare like a real scientist! Long and short, heavy and light, hot and cold, fast and slow!",
    "comp-c1-intro": "Let's compare long and short! Which object is longer? Which is shorter? Look carefully!",
    "comp-c2-intro": "Let's compare light and heavy! Which object is heavier? Which is lighter? Think about how they would feel!",
    "comp-c3-intro": "Let's compare hot and cold! Which is hotter? Which is colder? Think about temperature!",
    "comp-c4-intro": "Let's compare fast and slow! Which moves faster? Which moves slower? Think about speed!",
}


async def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(AUDIO_MAP)
    done = 0

    for key, text in AUDIO_MAP.items():
        filepath = os.path.join(OUTPUT_DIR, f"{key}.mp3")
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            done += 1
            print(f"[{done}/{total}] SKIP (exists): {key}")
            continue

        try:
            communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
            await communicate.save(filepath)
            done += 1
            size = os.path.getsize(filepath)
            print(f"[{done}/{total}] OK: {key} ({size} bytes)")
        except Exception as e:
            done += 1
            print(f"[{done}/{total}] ERROR: {key} - {e}")

    print(f"\nDone! Generated audio files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    asyncio.run(generate_all())

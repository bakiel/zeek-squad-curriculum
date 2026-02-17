#!/usr/bin/env python3
"""Generate all Week 4 Edge TTS audio files using en-US-AnaNeural voice."""
import asyncio
import os
import edge_tts

VOICE = "en-US-AnaNeural"
RATE = "-10%"
OUTPUT_DIR = "assets/audio/week4"

# All audio files needed for Week 4 games
AUDIO_MAP = {
    # === SHARED ===
    "star": "Yay! You earned a star!",

    # === TYCS: PATIENCE (Monday) ===
    "patience-intro": "Welcome to Patience! Patience means waiting for your turn nicely. Let's learn about being patient!",
    "patience-story1": "Story one. I waited my turn to go down the slide. I was so patient!",
    "patience-story2": "Story two. I waited for my food without whining. Good patience!",
    "patience-story3": "Story three. I counted to ten while waiting for my friend. That helped me be patient!",
    "patience-story4": "Story four. I took deep breaths while waiting in line. Breathing helps me wait!",
    "patience-story5": "Story five. I sang a song in my head while waiting. Being patient can be fun!",
    "patience-correct": "Great job! That's right! You are so patient!",
    "patience-wrong": "Hmm, not quite. Let's think about patience again!",
    "patience-complete": "Amazing! You are a patience superstar! You learned all about waiting nicely!",

    # === TYCS: COOPERATION (Tuesday) ===
    "coop-intro": "Welcome to Cooperation! Cooperation means working together as a team. Let's learn about teamwork!",
    "coop-story1": "Story one. We all helped clean up the classroom together. Teamwork!",
    "coop-story2": "Story two. My friend and I built a tower together. It was taller than we could build alone!",
    "coop-story3": "Story three. We took turns playing with the ball. Everyone got a chance!",
    "coop-story4": "Story four. We helped each other carry the heavy box. Together we are strong!",
    "coop-story5": "Story five. We worked together to solve a puzzle. Many hands make light work!",
    "coop-correct": "Yes! That's great cooperation! Working together is wonderful!",
    "coop-wrong": "Hmm, that's not cooperation. Let's think about teamwork!",
    "coop-complete": "Fantastic! You understand cooperation! Remember, we are stronger together!",

    # === TYCS: HONESTY (Wednesday) ===
    "honest-intro": "Welcome to Honesty! Honesty means telling the truth. When we are honest, people trust us!",
    "honest-story1": "Story one. I told my mom I broke the cup, even though I was scared. She was proud I told the truth!",
    "honest-story2": "Story two. I said sorry when I made a mistake. Being honest about mistakes is brave!",
    "honest-story3": "Story three. I told my friend the truth about their drawing. I was kind and honest!",
    "honest-story4": "Story four. I found a toy that wasn't mine and returned it. That's being honest!",
    "honest-story5": "Story five. I told the teacher what really happened. The truth is always the best choice!",
    "honest-correct": "Yes! That's honest! The truth is always the best choice!",
    "honest-wrong": "Hmm, that's not honest. Remember, we always tell the truth!",
    "honest-complete": "Wonderful! You learned about honesty! Always tell the truth and people will trust you!",

    # === TYCS: PERSEVERANCE (Thursday) ===
    "persev-intro": "Welcome to Perseverance! Perseverance means never giving up, even when things are hard!",
    "persev-story1": "Story one. I tried to tie my shoes five times before I got it. I never gave up!",
    "persev-story2": "Story two. The puzzle was hard, but I kept trying. Finally I finished it!",
    "persev-story3": "Story three. I fell off my bike but got back on and tried again. I am strong!",
    "persev-story4": "Story four. Reading was hard at first, but I practiced every day. Now I can read!",
    "persev-story5": "Story five. I couldn't reach the top, but I kept climbing. I made it!",
    "persev-correct": "Yes! That's perseverance! Never give up!",
    "persev-wrong": "Hmm, that's not perseverance. Remember, we never give up!",
    "persev-complete": "You are amazing! You understand perseverance! You can do hard things!",

    # === ELA: UPPERCASE LETTER HUNT (Monday) ===
    "ela-up-intro": "Welcome to Letter Hunt! Let's find letters in the alphabet! Can you find the uppercase letters?",
    "ela-up-correct": "Yes! You found the right letter! Great job!",
    "ela-up-wrong": "Oops! That's not the right letter. Try again!",
    "ela-up-complete": "Amazing! You found all the letters! You are a letter detective!",

    # === ELA: TRICKY LETTERS (Tuesday) ===
    "tricky-intro": "Welcome to Tricky Letters! Some letters look very similar. Let's learn to tell them apart! Like b and d, and p and q!",
    "tricky-correct": "Yes! You got the tricky letter right! Great eyes!",
    "tricky-wrong": "Oops! Those letters are tricky. Look carefully and try again!",
    "tricky-complete": "Wonderful! You can tell all the tricky letters apart! You have super sharp eyes!",

    # === ELA: UPPERCASE-LOWERCASE MATCH (Wednesday) ===
    "match-intro": "Welcome to Letter Matching! Every uppercase letter has a lowercase friend. Let's match them up!",
    "match-correct": "Perfect match! Those letters go together!",
    "match-wrong": "Hmm, those letters don't match. Try a different one!",
    "match-complete": "You matched all the letters! Uppercase and lowercase are best friends!",

    # === ELA: HARD LETTER MATCHES (Thursday) ===
    "hard-intro": "Welcome to the Hardest Letter Matches! These are the trickiest ones. Can you match a to A, b to B, d to D, and more?",
    "hard-correct": "Yes! That's the right match! You're so smart!",
    "hard-wrong": "Hmm, that's not quite right. These letters are tricky. Try again!",
    "hard-complete": "Incredible! You matched all the hardest letters! You are a letter matching champion!",

    # === MATH: SUBTRACTION INTRO (Monday) ===
    "sub-intro": "Welcome to Subtraction! When we take away, we subtract! Five cubes take away two equals three!",
    "sub-correct": "Yes! That's the right answer! Great subtraction!",
    "sub-wrong": "Hmm, not quite. Count what's left after taking away!",
    "sub-complete": "Amazing! You understand subtraction! You can take away like a math star!",

    # === MATH: SUBTRACTION MODELS (Tuesday) ===
    "submod-intro": "Welcome to Subtraction Models! Let's read subtraction stories from pictures! Look at the model and figure out the subtraction!",
    "submod-correct": "Yes! You read the model correctly! Great job!",
    "submod-wrong": "Hmm, look at the model again. Count what was there, then what was taken away!",
    "submod-complete": "Wonderful! You can read all the subtraction models!",

    # === MATH: CUBE TRAIN SUBTRACTION (Wednesday) ===
    "subcube-intro": "Welcome to Cube Train Subtraction! Let's break cube trains apart to learn subtraction! Break the train and count!",
    "subcube-correct": "Yes! You broke the cube train correctly!",
    "subcube-wrong": "Hmm, try breaking the train differently! Count carefully!",
    "subcube-complete": "Fantastic! You are a cube train subtraction expert!",

    # === MATH: SUBTRACTION SENTENCES (Thursday) ===
    "subsent-intro": "Welcome to Writing Subtraction Sentences! Look at the picture and write the subtraction! Like five minus two equals three!",
    "subsent-correct": "Yes! You wrote the subtraction sentence correctly!",
    "subsent-wrong": "Hmm, look at the picture again. How many are there? How many go away?",
    "subsent-complete": "Amazing! You can write subtraction sentences! You are a math writer!",

    # === SCIENCE: WEATHER WORDS (Monday) ===
    "weather-intro": "Welcome to Weather Words! Weather can be sunny, cloudy, rainy, snowy, or windy! Let's learn about weather!",
    "weather-correct": "Yes! That's the right weather! Great job!",
    "weather-wrong": "Hmm, that's not quite right. Look at the weather again!",
    "weather-complete": "Wonderful! You know all about weather! You are a weather expert!",

    # === SCIENCE: SUNLIGHT & SHADE (Tuesday) ===
    "sun-intro": "Welcome to Sunlight and Shade! The sun gives us light and warmth. Shade is where sunlight is blocked! Let's explore!",
    "sun-correct": "Yes! That's right! You understand sunlight and shade!",
    "sun-wrong": "Hmm, think again. Is it in the sun or in the shade?",
    "sun-complete": "Amazing! You know all about sunlight and shade!",

    # === SCIENCE: PRECIPITATION (Wednesday) ===
    "precip-intro": "Welcome to Precipitation! Water falls from the sky in different ways. Rain, snow, hail, and sleet! Let's learn about them!",
    "precip-correct": "Yes! That's the right type of precipitation!",
    "precip-wrong": "Hmm, that's not quite right. Think about what falls from the sky!",
    "precip-complete": "Wonderful! You know all about precipitation! Rain, snow, hail, and sleet!",

    # === SCIENCE: WEATHER PATTERNS (Thursday) ===
    "pattern-intro": "Welcome to Weather Patterns! Weather follows patterns. Spring is warm, summer is hot, fall is cool, and winter is cold!",
    "pattern-correct": "Yes! That's the right weather pattern!",
    "pattern-wrong": "Hmm, think about the seasons. What weather goes with each one?",
    "pattern-complete": "Amazing! You understand weather patterns! You are a weather scientist!",

    # === HEBREW: REVIEW WRITING (Monday) ===
    "heb-intro": "Shalom! Welcome to Hebrew letter review! Let's practice writing Aleph, Bet, and Vet! Ani Yachol! I can do it!",
    "heb-aleph": "This is Aleph! The first letter of the Hebrew alphabet! It makes a quiet sound, like a breath.",
    "heb-bet": "This is Bet! It makes the sound Buh! Like the word Bayit, which means house!",
    "heb-vet": "This is Vet! It looks like Bet but with no dot! It makes the sound Vuh!",
    "heb-correct": "Nachon! That's correct! Kol hakavod! Great honor!",
    "heb-wrong": "Lo nachon. Not correct. Let's try again! Ani Yachol!",
    "heb-complete": "Metzuyan! Excellent! You reviewed all three Hebrew letters! Ani Chazak! I am strong!",

    # === HEBREW: SOUNDS REVIEW (Tuesday) ===
    "hebsnd-intro": "Shalom! Let's review the sounds of our Hebrew letters! Listen carefully and match the sounds!",
    "hebsnd-correct": "Nachon! You matched the sound correctly!",
    "hebsnd-wrong": "Lo nachon. Listen to the sound again carefully!",
    "hebsnd-complete": "Metzuyan! You know all the Hebrew letter sounds! Kol hakavod!",

    # === HEBREW: MEMORY GAME (Wednesday) ===
    "hebmem-intro": "Shalom! Let's play a memory game with Hebrew letters! Flip the cards and find the matching pairs!",
    "hebmem-correct": "Nachon! You found a match! Great memory!",
    "hebmem-wrong": "Lo nachon. Those cards don't match. Try to remember where they are!",
    "hebmem-complete": "Metzuyan! You matched all the cards! What a great memory! Ani Yachol!",

    # === HEBREW: FINAL REVIEW (Thursday) ===
    "hebfin-intro": "Shalom! This is the final review! Show what you know about Aleph, Bet, and Vet! You can do it! Ani Yachol!",
    "hebfin-correct": "Nachon! Excellent! You really know your letters!",
    "hebfin-wrong": "Lo nachon. Don't give up! Try again! Perseverance!",
    "hebfin-complete": "Metzuyan! You passed the final review! You are a Hebrew letter champion! Shabbat Shalom!",
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

    print(f"\nDone! Generated {total} audio files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    asyncio.run(generate_all())

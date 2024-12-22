import os
import random
import time
import pygame
from datetime import datetime
import json
import threading

# Load settings from config.json
def load_settings():
    with open("config.json", "r") as f:
        settings = json.load(f)
    return settings

# Settings loaded from config.json
settings = load_settings()

AUDIO_FOLDER = settings["AUDIO_FOLDER"]
START_TIME = settings["START_TIME"]
END_TIME = settings["END_TIME"]
START_CHANCE = settings["START_CHANCE"]
AUDIO_LOAD_COUNT = settings["AUDIO_LOAD_COUNT"]
BREAK_TIME_MIN = settings["BREAK_TIME_MIN"]
BREAK_TIME_MAX = settings["BREAK_TIME_MAX"]

def find_audio_files(folder):
    audio_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                audio_files.append(os.path.join(root, file))
    return audio_files

def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_random_audios(audio_files):
    # Use the configured number of files to randomly select and play
    selected_files = random.sample(audio_files, k=min(AUDIO_LOAD_COUNT, len(audio_files)))  # Select AUDIO_LOAD_COUNT files
    for audio_file in selected_files:
        print(f"Playing: {audio_file}")
        play_audio(audio_file)
        time.sleep(1)  # Small delay to ensure smooth transition

def is_time_to_play():
    current_time = datetime.now()
    current_minutes = current_time.hour * 60 + current_time.minute
    return START_TIME <= current_minutes <= END_TIME  # Check if within the allowed time range

def start_playing():
    audio_files = find_audio_files(AUDIO_FOLDER)
    started = False  # Flag to track if the audio has started
    while not started:
        if is_time_to_play():
            # Random chance to start within the time window (chance = 1%)
            chance = random.randint(1, 100)
            print(f"Checking chance: {chance}% (00:00 to 04:45)")
            if chance <= START_CHANCE:
                print("Chance succeeded! Starting playback...")
                play_random_audios(audio_files)
                print("Finished playing. Taking a short break...")

                # Random break duration between BREAK_TIME_MIN and BREAK_TIME_MAX (in minutes)
                break_duration = random.randint(BREAK_TIME_MIN, BREAK_TIME_MAX) * 60  # Convert to seconds
                print(f"Taking a break for {break_duration // 60} minutes...")
                time.sleep(break_duration)  # Take a random-length break
                started = True  # Set the flag to True to stop the loop
            else:
                print(f"Chance failed, retrying in 1 minute... (chance: {START_CHANCE}%)")
                time.sleep(60)  # Wait for the next minute check
        else:
            print("Not in the allowed timeframe (00:00 to 04:45). Waiting for the next minute.")
            time.sleep(60)  # Wait for the next minute check

def run_in_background():
    background_thread = threading.Thread(target=start_playing, daemon=True)
    background_thread.start()

if __name__ == "__main__":
    run_in_background()

    while True:
        time.sleep(1)

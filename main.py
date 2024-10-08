import os
import requests
import base64
from bs4 import BeautifulSoup
import mimetypes
import logging

# Configure logging
logging.basicConfig(filename="script_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Gravity Falls-related word list
word_list = [
    "Arc", "Beam", "Blade", "Blaze", "Bolt", "Burst", 
    "Charm", "Chill", "Clash", "Clue", "Crux", "Crypt", 
    "Dive", "Drift", "Echo", "Fang", "Fate", "Flick", 
    "Flux", "Fury", "Grit", "Haze", "Hint", "Hollow", 
    "Hush", "Jinx", "Key", "Loom", "Mask", "Maze", 
    "Mist", "Myth", "Node", "Omen", "Orb", "Pact", 
    "Peak", "Phase", "Pierce", "Pine", "Pluck", "Prism", 
    "Quake", "Rift", "Riddle", "Rift", "Rune", "Shard", 
    "Shift", "Shine", "Shroud", "Sleek", "Smite", "Snipe", 
    "Snare", "Soar", "Sonic", "Spell", "Spire", "Sting", 
    "Stone", "Stray", "Surge", "Thorn", "Thrust", "Trail", 
    "Trek", "Veil", "Vex", "Void", "Warp", "Whip", 
    "Wisp", "Wish", "Wraith", "Writ", "Zeal", "Zap", 
    "Zap", "Zone", "Zoom", "Bolt", "Brand", "Brave", 
    "Brisk", "Burn", "Calm", "Charm", "Chase", "Chill", 
    "Claw", "Cloak", "Crest", "Crown", "Crypt", "Dawn", 
    "Daze", "Dread", "Duel", "Edge", "Ember", "Fable", 
    "Fate", "Fawn", "Faze", "Fist", "Flame", "Flare", 
    "Flint", "Flux", "Foe", "Fury", "Gale", "Gaze", 
    "Gleam", "Glimpse", "Glow", "Grit", "Grove", "Haze", 
    "Hush", "Jade", "Jet", "Jolt", "Loom", "Lush", 
    "Muse", "Nexus", "Nova", "Nudge", "Oath", "Onyx", 
    "Pact", "Pike", "Pine", "Ploy", "Plume", "Poise", 
    "Prowl", "Quake", "Quartz", "Quest", "Raze", "Reap", 
    "Rift", "Rime", "Roam", "Rush", "Rune", "Rust", 
    "Sage", "Shade", "Shift", "Shine", "Shock", "Shroud", 
    "Sleek", "Snare", "Soar", "Spine", "Sprout", "Stark", 
    "Sting", "Stone", "Surge", "Thorn", "Thrust", "Tide", 
    "Trail", "Trek", "Veil", "Vex", "Vibe", "Wane", 
    "Wisp", "Wish", "Wit", "Writ", "Zeal", "Zap"
]


# URL and headers
url = "https://codes.thisisnotawebsitedotcom.com/"
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7,es;q=0.6",
    "origin": "https://thisisnotawebsitedotcom.com",
    "referer": "https://thisisnotawebsitedotcom.com/",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

# Function to save a file with a validated extension, skipping if it already exists
def save_file(directory_name, content_url, file_type=None, file_data=None):
    try:
        if content_url.startswith("data:"):
            # Handle base64-encoded data
            header, encoded = content_url.split(",", 1)
            file_data = base64.b64decode(encoded)
            file_name = f"file.{file_type}"
        else:
            # Handle regular URLs
            file_name = os.path.basename(content_url).split("?")[0]
            file_path = os.path.join(directory_name, file_name)
            if os.path.exists(file_path):
                logging.info(f"File {file_name} already exists in directory {directory_name}, skipping download.")
                print(f"File {file_name} already exists in directory {directory_name}, skipping download.")
                return
            if not file_data:
                response = requests.get(content_url, headers=headers)
                file_data = response.content
        
        with open(os.path.join(directory_name, file_name), "wb") as file:
            file.write(file_data)
        logging.info(f"Saved {file_name} in directory: {directory_name}")
        print(f"Saved {file_name} in directory: {directory_name}")
    except Exception as e:
        logging.error(f"Failed to save file from {content_url}: {e}")
        print(f"Failed to save file from {content_url}: {e}")

# Function to send the POST request and save successful responses
def send_post_request_and_save(code):
    boundary = "----WebKitFormBoundaryyj53iqAdUls31sGh"
    data = f"--{boundary}\r\nContent-Disposition: form-data; name=\"code\"\r\n\r\n{code}\r\n--{boundary}--\r\n"
    custom_headers = headers.copy()
    custom_headers["content-type"] = f"multipart/form-data; boundary={boundary}"
    
    try:
        response = requests.post(url, headers=custom_headers, data=data)
        
        # Only process if the response status code is 200
        if response.status_code == 200:
            # Determine content type
            content_type = response.headers.get('Content-Type', '').lower()
            directory_name = code.replace(" ", "_")
            os.makedirs(directory_name, exist_ok=True)

            if 'image/' in content_type:
                # Handle if the content is an image but was not in an <img> tag
                extension = mimetypes.guess_extension(content_type.split(";")[0])
                file_name = f"image{extension}"
                save_file(directory_name, content_url=file_name, file_data=response.content)
            else:
                # Save the raw content in a text file
                response_text_path = os.path.join(directory_name, "response.txt")
                with open(response_text_path, "wb") as file:
                    file.write(response.content)  # Write the raw binary content
                print(f"Saved response content as response.txt in directory: {directory_name}")
                logging.info(f"Saved response content as response.txt in directory: {directory_name}")

                # Parse HTML to find images, videos, and audio
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find all <img> tags
                for img_tag in soup.find_all("img"):
                    img_url = img_tag.get("src")
                    if img_url:
                        save_file(directory_name, img_url, "png")
                
                # Find all <video> tags
                for video_tag in soup.find_all("video"):
                    source_tag = video_tag.find("source")
                    if source_tag:
                        video_url = source_tag.get("src")
                        if video_url:
                            save_file(directory_name, video_url, "mp4")
                
                # Find all <audio> tags
                for audio_tag in soup.find_all("audio"):
                    source_tag = audio_tag.find("source")
                    if source_tag:
                        audio_url = source_tag.get("src")
                        if audio_url:
                            save_file(directory_name, audio_url, "mp3")
                
                # Append the name to a main text file listing successful responses
                with open("successful_responses.txt", "a", encoding="utf-8") as main_file:
                    main_file.write(f"{code}\n")
                
                logging.info(f"Saved response for word: {code}")
                print(f"Saved response for word: {code}")
        else:
            logging.warning(f"Non-200 status code {response.status_code} for word: {code}. Skipping save.")
            print(f"Non-200 status code {response.status_code} for word: {code}. Skipping save.")
    except Exception as e:
        logging.error(f"Failed to process word {code}: {e}")
        print(f"Failed to process word {code}: {e}")

# Iterate over the word list and send requests
for word in word_list:
    send_post_request_and_save(word)

# Gravity Falls Code Checker

This project is designed to interact with the website `thisisnotawebsitedotcom.com`. The website contains a place to enter codes that yield different outcomes. This script sends POST requests with specific Gravity Falls-related codes to the website and saves the content returned by the server. The content may include images, videos, audio files, or plain text, which could contain hidden secrets and resources related to the show.

## Features

- Sends POST requests with predefined Gravity Falls-related codes.
- Automatically saves any returned images, videos, or audio files.
- Logs all successful responses and errors.
- Saves the raw response content in a text file if no media files are detected.
- Skips downloading files that already exist.
- Customizable Word List: Allows users to easily modify the list of words or phrases for which the script searches.

## Prerequisites

- Python 3.6 or later
- pip (Python package installer)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AsafMeizner/gravity-falls-autofetcher.git
   cd gravity-falls-code-checker
   ```

2. Install the required libraries:
   ```bash
   python install_libraries.py
   ```

   This script will automatically install the required packages: requests, beautifulsoup4, and mimetypes.

## Usage
1. Run the script:
   After installing the necessary libraries, run the main script:
   ```bash
   python main.py
   ```
2. What the script does:
   * The script iterates through a predefined list of Gravity Falls-related words (e.g., "dipper," "mabel," "bill cipher").
   * For each word, it sends a POST request to the website `thisisnotawebsitedotcom.com`.
If the response status is 200 OK, the script checks the content type of the response:
        * Images: The script saves the images to a folder named after the code.
        * Videos: The script saves videos to the same folder.
        * Audio Files: The script saves audio files to the folder.
        * Plain Text or HTML: The script saves the raw response content in a text file.
   * The script logs all successful responses in a file named `successful_responses.txt`.

3. Check the results:
    * The script uses a list of predefined Gravity Falls-related words to send POST requests. If you want to search for different codes or add new ones, you can easily modify the word_list in the main.py file. Simply edit the list with your desired words or phrases.

4. Check the results:
    * After the script has finished running, you can find the saved files in directories named after each code word. The successful_responses.txt file will contain a list of all the codes that received a successful response.

## Logging
* All logs, including errors and information about saved files, are stored in `script_log.txt`.

## Troubleshooting
* If you encounter issues with missing dependencies, ensure that all required libraries are installed by rerunning the install_libraries.py script.
* Make sure you have a stable internet connection as the script sends requests to an external website.
* If the website is down or not responding, you may see errors in the log file indicating failed requests.
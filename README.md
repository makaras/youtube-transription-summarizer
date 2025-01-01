# YouTube Transcript Summarizer

This Python script allows you to download, clean, and summarize transcripts from YouTube videos. It leverages `yt-dlp` for downloading subtitles, Python's `re` library for cleaning text, and OpenAI's API for generating detailed summaries.

## Features

1. **Download Transcript**: Fetch subtitles (in `.vtt` format) automatically from a YouTube video using `yt-dlp`.
2. **Clean Transcript**: Remove timestamps, tags, and duplicate lines for easier readability.
3. **Summarize with OpenAI**: Generate a detailed summary of the cleaned transcript using OpenAI's GPT-4 API.

---

## Prerequisites

To use this script, ensure the following dependencies and tools are installed:

### System Requirements
- Python 3.8 or later
- `yt-dlp` (YouTube downloader tool)
    - Install with: `pip install yt-dlp`

### Python Dependencies
- Install required Python packages:
  ```bash
  pip3 install openai

# YouTube Transcript Summarizer

This Python script allows you to download, clean, and summarize transcripts from YouTube videos. It leverages `yt-dlp` for downloading subtitles, Python's `re` library for cleaning text, and OpenAI's API for generating detailed summaries.

## Features

1. **Download Transcript**: Fetch subtitles (in `.vtt` format) automatically from a YouTube video using `yt-dlp`.
2. **Clean Transcript**: Remove timestamps, tags, and duplicate lines for easier readability.
3. **Summarize with OpenAI**: Generate a detailed summary of the cleaned transcript using OpenAI's GPT-4 API.

---

## Prerequisites

To use this script, ensure the following dependencies and tools are installed:

### System Requirements
- Python 3.8 or later
- `yt-dlp` (YouTube downloader tool)
    - Install with: `pip install yt-dlp`

### Python Dependencies
- Install required Python packages:
  ```bash
  pip install openai

### Usage
- Setup OpenAI API Key: Replace api_key in the main() function with your OpenAI API key.

- Run the Script: Execute the script with:

  ```bash
    python3 print_summary.py

- Provide Video URL: Update the video_url variable in the main() function with the URL of the YouTube video.

### Outputs

- Cleaned Transcript: A .txt file with cleaned content (e.g., example_clean.txt).
- AI Summary: A .txt file with the OpenAI-generated summary (e.g., example_openai_summary.txt).

### Notes
- Ensure the video has auto-generated subtitles in Polish (pl) or adjust the --sub-lang flag in the download_transcript function to match your preferred language.
- The OpenAI API key must be valid, and your account should have access to GPT-4 for optimal performance.
- Large transcripts might exceed the token limit of GPT-4; consider summarizing them in smaller sections.

### Disclaimer
- The script is provided as is and may require additional adjustments for specific use cases. Ensure your use of YouTube content complies with copyright laws.
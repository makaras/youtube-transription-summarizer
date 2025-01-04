import glob
import os
import re
import shutil
import subprocess
import config

from openai import OpenAI


def move_vtt_and_txt_files_if_exist():
    # Use the current working directory as the source folder
    source_folder = os.getcwd()

    # Path to the 'archive' folder
    archive_folder = os.path.join(source_folder, "archive")

    # Create the 'archive' folder if it does not exist
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Iterate through the files in the source folder
    for file_name in os.listdir(source_folder):
        # Full path to the file
        file_path = os.path.join(source_folder, file_name)

        # Check if the file is a .vtt or .txt file
        if os.path.isfile(file_path) and file_name.endswith(('.vtt', '.txt')):
            # Move the file to the 'archive' folder
            shutil.move(file_path, archive_folder)
            print(f"Moved: {file_name}")


def download_transcript(video_url):
    # Use yt-dlp with subprocess
    command = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--sub-format", "vtt",
        "--sub-lang", "pl",
        "-o", "%(title)s.%(ext)s",  # Video title will be used as filename
        video_url
    ]
    subprocess.run(command)

    # Fetch VTT filename
    vtt_files = glob.glob("*.vtt")
    if vtt_files:
        return vtt_files[0]
    else:
        raise FileNotFoundError("File with transcription not found")


def clean_transcript(file_name):
    # Read file content
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Delete tags
    content = re.sub(r'<[^>]+>', '', content)

    # Delete timestamps
    content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n", '', content)

    # Delete duplicates
    lines = content.split('\n')
    unique_lines = list(dict.fromkeys(lines))

    # Save to file without duplicates and tags
    clean_file_name = file_name.replace('.vtt', '_clean.txt')
    with open(clean_file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(unique_lines))

    return clean_file_name


def openai_fetch_summary(input_text, openai_api_key):
    client = OpenAI(
        api_key=openai_api_key
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Jesteś pomocnym asystentem.",
            },
            {
                "role": "user",
                "content": f"Napisz szczegółowe streszczenie z transkrypcji wygenerowanej z filmu youtube, im więcej wątków tym lepiej, możesz podzielić chronologicznie na części :\n{input_text}",
            }
        ],
        model="gpt-4o",
        max_tokens=16383,
        temperature=1
    )

    return response.choices[0].message.content


def main():
    video_url = input("Please enter youtube video URL to summarize: ")
    openai_api_key = config.OPENAI_API_KEY

    move_vtt_and_txt_files_if_exist()

    transcript_file = download_transcript(video_url)
    print(f"Fetched transcription to file: {transcript_file}")

    clean_file = clean_transcript(transcript_file)

    with open(clean_file, 'r', encoding='utf-8') as file:
        text = file.read()

    openai_summary = openai_fetch_summary(text, openai_api_key)
    print("Summary by OpenAI:", openai_summary)

    # Save summary to file
    openai_summary_file_name = transcript_file.replace('.vtt', '_openai_summary.txt')
    with open(openai_summary_file_name, 'w', encoding='utf-8') as file:
        file.write(openai_summary)


if __name__ == "__main__":
    main()

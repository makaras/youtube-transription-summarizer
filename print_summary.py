import glob
import re
import subprocess

from openai import OpenAI


def download_transcript(video_url):
    # Użycie yt-dlp za pomocą subprocess
    command = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--sub-format", "vtt",
        "--sub-lang", "pl",
        "-o", "%(title)s.%(ext)s",  # Tytuł zostanie użyty jako nazwa pliku
        video_url
    ]
    subprocess.run(command)

    # Pobranie nazwy pliku VTT; zakładam, że jest jeden plik o rozszerzeniu .vtt
    vtt_files = glob.glob("*.vtt")
    if vtt_files:
        return vtt_files[0]
    else:
        raise FileNotFoundError("Nie odnaleziono pliku z transkrypcją.")


def clean_transcript(file_name):
    # Czytanie zawartości pliku
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Usuwanie tagów używając regex
    content = re.sub(r'<[^>]+>', '', content)

    # Usuwanie znaczników czasu
    content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n", '', content)

    # Usuwanie duplikatów linii
    lines = content.split('\n')
    unique_lines = list(dict.fromkeys(lines))

    # Zapisanie do pliku bez duplikatów i tagów
    clean_file_name = file_name.replace('.vtt', '_clean.txt')
    with open(clean_file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(unique_lines))

    return clean_file_name


def openai_fetch_summary(input_text, api_key):
    client = OpenAI(
        api_key=api_key
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
        max_tokens=16383
    )

    return response.choices[0].message.content


def main():
    video_url = "PASTE_URL_HERE"
    api_key = "PASTE_OPENAI_KEY_HERE"

    transcript_file = download_transcript(video_url)
    print(f"Pobrano transkrypcję do pliku: {transcript_file}")

    clean_file = clean_transcript(transcript_file)

    with open(clean_file, 'r', encoding='utf-8') as file:
        text = file.read()

    openai_summary = openai_fetch_summary(text, api_key)
    print("Streszczenie OpenAI:", openai_summary)

    # Zapisanie summary do pliku
    openai_summary_file_name = transcript_file.replace('.vtt', '_openai_summary.txt')
    with open(openai_summary_file_name, 'w', encoding='utf-8') as file:
        file.write(openai_summary)


if __name__ == "__main__":
    main()

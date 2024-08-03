Title: Easy subtitle translation using google api
Date: 2024-07-13
Tags: Python, translate, subtitles, Nima Moradi
Category: Guide
Summary: Easy subtitle translation using google api

## Breaking Language Barriers: Translating Subtitles with Google API

Sometimes ago, I wanted to watch a movie with my mother, but she doesn't have the best English. I thought of machine translation and decided to use Google Translate to translate the subtitles into her preferred language. Here's how I did it.

### Setting Up Google Translate API

To use the Google Translate API, you need to set up a Google Cloud project and authenticate your requests. Follow the instructions [here](https://translatepress.com/docs/automatic-translation/generate-google-api-key/#:~:text=Enable%20Google%20Cloud%20Translation%20API,-With%20the%20new&text=From%20here%20you%20need%20to,select%20it%20and%20click%20Enable.).

### The Script

Here's a simple Python script that uses the Google Translate API to translate subtitles.

   
```python
from google.cloud import translate_v2 as translate
import re


def parse_srt_to_array(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = content.split('\n\n')
    subtitles = []
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = lines[0]
            time_range = lines[1]
            text = '\n'.join(lines[2:])
            subtitles.append({'index': index, 'time_range': time_range, 'text': text})
    return subtitles


def parse_subtitle_block(block):
    index = int(block[0])
    time_range = block[1]
    text_lines = block[2:]
    text = " ".join(text_lines)
    return {'index': index, 'time_range': time_range, 'text': text}


def translate_text_with_google(text, target_language, source_language):
    translate_client = translate.Client()
    # The API automatically handles HTML tags if you pass the format as 'html'
    result = translate_client.translate(text, source_language=source_language, target_language=target_language,
                                        format_='html')
    return result['translatedText']


def reverse_text(text):
    text = clean_html_tags(text)
    # Reverse each line in the subtitle text separately
    return '\n'.join(line[::-1] for line in text.split('\n'))


def clean_html_tags(text):
    # Remove HTML-like tags
    clean_text = re.sub(r'<[^>]*>', '', text)
    return clean_text


translated = []


def write_translated_subtitles(subtitles, output_path, target_language, source_language):
    with open(output_path, 'w', encoding='utf-8') as file:
        for subtitle in subtitles:
            translated_text = translate_text_with_google(subtitle['text'], target_language, source_language)
            print(translated_text)
            translated.append(translated_text)
            file.write(f"{subtitle['index']}\n")
            file.write(f"{subtitle['time_range']}\n")
            file.write(f"{translated_text}\n\n")


# Example usage
input_srt_path = './sub/input.srt'  # Update this path
output_srt_path = './sub/output.srt'  # Update this path

# Parse the .srt file to an array of subtitle blocks
subtitles = parse_srt_to_array(input_srt_path)

# Translate the subtitles (mock translation in this case) and write to a new file
write_translated_subtitles(subtitles, output_srt_path, target_language='fa', source_language='en')


```
Title: Building a Local AI Audiobook Pipeline with Python and Kokoro
Date: 2025-12-28 10:00
Category: Engineering
Tags: Python, AI, MLX, PDF, Audio
Slug: building-local-ai-audiobook-pipeline
Summary: How I used PyMuPDF and the Kokoro-82M model to create a high-quality, local text-to-speech engine for converting PDFs to audiobooks.

During the holidays, I wanted to listen to a specific book series. However, I found myself in a common predicament: there were no official audiobooks available, and the existing mobile text-to-speech accessibility tools sounded too robotic for a novel.

So I decided to engineer a solution myself. I built a Python pipeline that ingests a PDF, parses the structure, and uses a high-quality local AI model to generate audio files.

Here is the technical breakdown of how I built it using **PyMuPDF** and **Kokoro-82M**.

## The Architecture

The pipeline consists of three main stages:
1.  **Extraction:** Reading the raw text from the PDF file.
2.  **Structuring:** Using Regular Expressions to split the continuous text into logical chapters.
3.  **Synthesis:** Feeding the text into the Kokoro-82M model to generate WAV files.

## Step 1: Text Extraction with PyMuPDF

I chose `PyMuPDF` (imported as `fitz`) for this task because of its speed and accuracy in preserving text order.

```python
import fitz

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"
    return full_text
```
## Step 2: Intelligent Chapter Splitting
The raw text from a PDF is a single continuous stream. To make the audiobook navigable, I needed to split it by chapter. I used Python's `re` module to identify chapter headings (e.g., "Chapter 1" or "Chapter IV").

This function splits the text and returns a list of dictionaries, allowing me to process one chapter at a time.

```python
import re

def split_into_chapters(full_text):
    # Split by "Chapter X" or "Chapter RomanNum"
    pattern = r"(?i)(Chapter\s+\d+|Chapter\s+[IVX]+)"
    parts = re.split(pattern, full_text)
    
    chapters = []
    
    # Check for Intro (text before the first "Chapter 1")
    if parts[0].strip():
        chapters.append({"title": "Intro", "content": parts[0]})
    
    # Group the rest (Title + Content)
    for i in range(1, len(parts), 2):
        header = parts[i]
        content = parts[i+1] if i+1 < len(parts) else ""
        chapters.append({"title": header, "content": content})
        
    return chapters
```

## Step 3: Audio Generation with Kokoro
For the audio generation, I used `Kokoro-82M (specifically the prince-canuma/Kokoro-82M implementation)`. This model is highly efficient and optimized for local inference, offering voice quality that rivals commercial cloud APIs without the cost or latency.

I configured the pipeline to save each chapter as a distinct WAV file.
```python
def process_chapter(chapter, output_folder="output_audio"):
    """
    Generates audio for the section.
    """
    if not chapter:
        print("No text found.")
        return

    title = chapter['title'].strip()
    content = chapter['content']
    
    print(f"Processing: {title}...")
    
    # MLX-Audio generation
    # Using 'af_heart' voice profile for a natural tone
    generate_audio(
        text=content,
        model_path="prince-canuma/Kokoro-82M", 
        voice="af_heart",
        output_file=f"{output_folder}/{title}.wav"
    )
    
    print(f"Done. Saved to {output_folder}/{title}.wav")
```
## Conclusion

I built this simply because I wanted to listen to a book and no audio version existed.

It serves as a reminder that we don't always have to wait for official tools or features. With the current state of Python libraries and local AI, building your own custom automation is often easier than it seems.
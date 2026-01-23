#!/usr/bin/env python3
"""
Audio Transcription Tool
Transcribes audio files using Google Gemini API.

Usage:
    audio-transcribe.py recording.m4a
    audio-transcribe.py recording.m4a --timestamps
    audio-transcribe.py recording.m4a --output transcript.md
    audio-transcribe.py recording.m4a --json

Requirements:
    - GEMINI_API_KEY environment variable
    - pip install google-generativeai

Get an API key at: https://makersuite.google.com/app/apikey
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed")
    print("Run: pip install google-generativeai")
    sys.exit(1)


def get_api_key():
    """Get Gemini API key from environment."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("\nTo set up:")
        print("1. Get an API key at: https://makersuite.google.com/app/apikey")
        print("2. Set the environment variable:")
        print("   export GEMINI_API_KEY='your-key-here'  # Mac/Linux")
        print("   $env:GEMINI_API_KEY='your-key-here'   # Windows PowerShell")
        sys.exit(1)
    return api_key


def transcribe_audio(audio_path: str, include_timestamps: bool = False) -> str:
    """Transcribe audio file using Gemini."""

    api_key = get_api_key()
    genai.configure(api_key=api_key)

    # Upload the audio file
    audio_file = genai.upload_file(path=audio_path)

    # Create the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Build the prompt
    if include_timestamps:
        prompt = """Transcribe this audio file. Include timestamps at the start of each
        major section or when the speaker changes topics. Format as:

        [MM:SS] Transcribed text here...
        [MM:SS] More transcribed text...

        Be accurate and include all spoken content."""
    else:
        prompt = """Transcribe this audio file accurately. Include all spoken content.
        Format as clean, readable paragraphs."""

    # Generate transcription
    response = model.generate_content([audio_file, prompt])

    return response.text


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio files using Google Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Transcribe a voice memo:
    audio-transcribe.py ~/Documents/memo.m4a

  Transcribe with timestamps:
    audio-transcribe.py recording.m4a --timestamps

  Save to file:
    audio-transcribe.py recording.m4a --output transcript.md

  Output as JSON:
    audio-transcribe.py recording.m4a --json
        """
    )

    parser.add_argument('audio_file', help='Path to audio file (m4a, mp3, wav, etc.)')
    parser.add_argument('--timestamps', '-t', action='store_true',
                        help='Include timestamps in transcript')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output as JSON instead of plain text')
    parser.add_argument('--output', '-o', help='Save transcript to file')

    args = parser.parse_args()

    # Validate input file
    audio_path = Path(args.audio_file).expanduser()
    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    # Transcribe
    try:
        transcript = transcribe_audio(str(audio_path), args.timestamps)
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

    # Output
    if args.json:
        result = {
            "file": str(audio_path),
            "transcript": transcript,
            "timestamps_included": args.timestamps
        }
        output = json.dumps(result, indent=2)
    else:
        output = transcript

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.write_text(output)
        print(f"Transcript saved to: {output_path}")
    else:
        print(output)


if __name__ == '__main__':
    main()

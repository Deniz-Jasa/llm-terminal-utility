#!/usr/bin/env python3
import os
import sys
import argparse
import threading
import time
import json
from google.genai import types
from client import client, MODEL

def spinner(stop_event, label="Generating"):
    symbols = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{symbols[idx % len(symbols)]} {label}...")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write("\r" + " " * (len(label) + 5) + "\r")
    sys.stdout.flush()


def clean_json(text: str) -> str:
    """
    Strip Markdown fences and any non-JSON prefix/suffix, returning the raw JSON object.
    """
    # If fenced code block, remove the first and last fence lines
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    cleaned = "\n".join(lines).strip()

    # As a fallback, extract from first '{' to last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start : end + 1]
    return cleaned


def create(instruction: str):
    prompt = (
        "You are a file‑generation assistant. Given a natural language instruction, "
        "return ONLY a JSON object with keys:\n"
        "  filename: the name of the file (with extension)\n"
        "  content: the full text to write into the file\n\n"
        f"Instruction: {instruction}"
    )
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        max_output_tokens=1024,
        temperature=0.0,
    )

    stop_event = threading.Event()
    spin_thread = threading.Thread(
        target=spinner, args=(stop_event, "Generating"), daemon=True
    )
    spin_thread.start()

    first = True
    response_text = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=contents, config=config
        ):
            if first:
                stop_event.set()
                spin_thread.join()
                first = False
            response_text += chunk.text

        # Clean out any fences or extra text
        json_text = clean_json(response_text)
        data = json.loads(json_text)

        filename = data.get("filename")
        content = data.get("content", "")
        if not filename:
            print("❌ LLM did not return a filename. Full response:\n", response_text)
            return

        # Write the file
        with open(filename, "w") as f:
            f.write(content)
        print(f"✅ Created file '{filename}'.")
    except json.JSONDecodeError:
        print("\n\n❌ Failed to parse JSON. Raw response:\n", response_text)
    except Exception as e:
        print("\n\n❌ Error during creation:", e)


def main():
    parser = argparse.ArgumentParser(
        description="Create a file via natural‑language instruction."
    )
    parser.add_argument(
        "instruction", nargs="+", help="E.g. create a README for a clock app"
    )
    args = parser.parse_args()
    create(" ".join(args.instruction))


if __name__ == "__main__":
    main()

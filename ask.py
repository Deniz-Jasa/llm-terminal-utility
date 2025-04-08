#!/usr/bin/env python3
import sys
import argparse
import threading
import time
from google.genai import types
from client import client, MODEL

def spinner(stop_event, label="Thinking"):
    symbols = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{symbols[idx % len(symbols)]} {label}...')
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write('\r' + ' ' * (len(label)+5) + '\r')
    sys.stdout.flush()

def ask(question: str):
    prompt = (
        "You are a terminal assistant. Provide concise, focused answers.\n\n"
        f"Question: {question}"
    )
    contents = [ types.Content(role="user", parts=[types.Part.from_text(text=prompt)]) ]
    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        max_output_tokens=200,
        temperature=0.2,
        top_p=0.9,
    )

    stop_event  = threading.Event()
    spin_thread = threading.Thread(target=spinner, args=(stop_event,"Thinking"), daemon=True)
    spin_thread.start()

    first = True
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=contents, config=config
        ):
            if first:
                stop_event.set()
                spin_thread.join()
                first = False
            print(chunk.text, end="")
        print()
    except Exception as e:
        stop_event.set()
        spin_thread.join()
        print("\n\nError during generation:", e)

def main():
    parser = argparse.ArgumentParser(description="Ask a question to Gemini 2.0 Flash.")
    parser.add_argument("question", nargs="+", help="Your question (no quotes needed).")
    args = parser.parse_args()
    ask(" ".join(args.question))

if __name__ == "__main__":
    main()
